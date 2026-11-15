/*
 * Minimal boot-safe local firmware for the ESP32-S3 smart plug.
 *
 * Scope of this file:
 *   - initialize NVS
 *   - force the relay GPIO to a safe OFF level before anything else
 *   - run the portable smartplug_core state machine
 *   - handle a debounced physical button as a local toggle
 *   - refuse ON while meter/temperature validity is not established
 *
 * This is NOT a complete product firmware: PZEM, OLED, RGB, RTC, Wi-Fi,
 * MQTT, OTA, and provisioning are separate components and are not yet
 * integrated. ESP-IDF build is BLOCKED in this environment.
 */
#include <stdio.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"

#include "board_config.h"
#include "smartplug_core.h"

static const char *TAG = "smartplug";
static sp_state_t g_state;
static uint32_t g_command_sequence = 0;

static void relay_init_safe(void) {
    gpio_config_t config = {
        .pin_bit_mask = (1ULL << PIN_RELAY_CTRL),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    ESP_ERROR_CHECK(gpio_config(&config));
    ESP_ERROR_CHECK(gpio_set_level(PIN_RELAY_CTRL, RELAY_SAFE_LEVEL));
}

static void relay_set(sp_output_t output) {
    int level = output == SP_OUTPUT_ON ? RELAY_ACTIVE_LEVEL : RELAY_SAFE_LEVEL;
    ESP_ERROR_CHECK(gpio_set_level(PIN_RELAY_CTRL, level));
}

static void button_init(void) {
    gpio_config_t config = {
        .pin_bit_mask = (1ULL << PIN_BUTTON),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    ESP_ERROR_CHECK(gpio_config(&config));
}

static bool button_pressed_debounced(void) {
    if (gpio_get_level(PIN_BUTTON) != BUTTON_ACTIVE_LEVEL) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(50));
    return gpio_get_level(PIN_BUTTON) == BUTTON_ACTIVE_LEVEL;
}

static void issue_button_toggle(void) {
    int64_t now_ms = esp_timer_get_time() / 1000;
    sp_command_t command;
    memset(&command, 0, sizeof(command));
    g_command_sequence += 1;
    snprintf(command.command_id, sizeof(command.command_id), "btn-%lld", (long long)now_ms);
    sp_copy_string(command.device_id, sizeof(command.device_id), g_state.device_id);
    command.requested_output = SP_REQ_TOGGLE;
    command.source = SP_SRC_PHYSICAL_BUTTON;
    command.issued_at_ms = now_ms;
    command.expires_at_ms = now_ms + 5000;
    command.sequence = g_command_sequence;

    sp_decision_t decision;
    sp_decide_command(&g_state, &command, now_ms, 30000, &decision);
    if (decision.accepted) {
        sp_apply_decision(&g_state, &command, &decision, now_ms);
        relay_set(g_state.commanded_output);
        ESP_LOGI(TAG, "button: %s (%s)", decision.reason_code, sp_output_name(g_state.commanded_output));
    } else {
        ESP_LOGW(TAG, "button rejected: %s", decision.reason_code);
    }
}

void app_main(void) {
    esp_err_t nvs_result = nvs_flash_init();
    if (nvs_result == ESP_ERR_NVS_NO_FREE_PAGES || nvs_result == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        nvs_result = nvs_flash_init();
    }
    ESP_ERROR_CHECK(nvs_result);

    relay_init_safe();
    button_init();

    int64_t now_ms = esp_timer_get_time() / 1000;
    sp_state_init(&g_state, "dev-esp32-001", now_ms);
    g_state.mode = SP_MODE_BOOT_SAFE;
    g_state.commanded_output = SP_OUTPUT_OFF;
    g_state.clock_valid = false;
    g_state.meter_valid = false;       /* PZEM not integrated yet -> ON rejected */
    g_state.temperature_valid = false; /* TMP102 not integrated yet -> ON rejected */
    g_state.lockout = false;

    ESP_LOGW(TAG, "BOOT_SAFE: relay OFF; meter/temp not valid; ON will be rejected");
    vTaskDelay(pdMS_TO_TICKS(2000));

    /* Only a safe local OFF state is entered automatically. ON remains blocked
     * until meter and temperature services establish validity. */
    g_state.mode = SP_MODE_READY_OFF;

    for (;;) {
        if (button_pressed_debounced()) {
            issue_button_toggle();
            while (gpio_get_level(PIN_BUTTON) == BUTTON_ACTIVE_LEVEL) {
                vTaskDelay(pdMS_TO_TICKS(20));
            }
        }
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
