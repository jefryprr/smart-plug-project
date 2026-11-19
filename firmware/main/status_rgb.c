#include "status_rgb.h"

#include "driver/gpio.h"
#include "esp_cpu.h"
#include "esp_rom_sys.h"
#include "freertos/FreeRTOS.h"

#include "board_config.h"

/*
 * Onboard WS2812 of the ESP32-S3-DevKitC-1 v1.0 (GPIO48).
 *
 * Bit-banged prototype driver: 800 kHz, GRB order, 24 bits, >=50 us reset.
 * It is intentionally small and has no external LED dependency. Timing is
 * not calibrated; visual status only, not a safety indicator.
 */
static portMUX_TYPE s_lock = portMUX_INITIALIZER_UNLOCKED;

static inline void wait_cycles(uint32_t cycles) {
    uint32_t start = esp_cpu_get_cycle_count();
    while ((esp_cpu_get_cycle_count() - start) < cycles) {
        /* busy wait: WS2812 timing is cycle-sensitive */
    }
}

static void send_bit(bool one) {
    /* 240 MHz: T0H ~0.4 us (96 cyc), T0L ~0.8 us (192 cyc);
     * T1H ~0.8 us, T1L ~0.45 us (108 cyc). */
    gpio_set_level(PIN_STATUS_RGB, 1);
    wait_cycles(one ? 192u : 96u);
    gpio_set_level(PIN_STATUS_RGB, 0);
    wait_cycles(one ? 108u : 192u);
}

static void send_byte(uint8_t value) {
    for (int bit = 7; bit >= 0; --bit) {
        send_bit((value & (1u << bit)) != 0);
    }
}

static void send_color(uint8_t red, uint8_t green, uint8_t blue) {
    portENTER_CRITICAL(&s_lock);
    send_byte(green);
    send_byte(red);
    send_byte(blue);
    esp_rom_delay_us(60);
    portEXIT_CRITICAL(&s_lock);
}

void status_rgb_init(void) {
    gpio_config_t config = {
        .pin_bit_mask = (1ULL << PIN_STATUS_RGB),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    (void)gpio_config(&config);
    (void)gpio_set_level(PIN_STATUS_RGB, 0);
    send_color(0, 0, 0);
}

void status_rgb_set(status_rgb_pattern_t pattern) {
    switch (pattern) {
        case STATUS_RGB_BOOT:
            send_color(0, 0, 48);       /* blue */
            break;
        case STATUS_RGB_WIFI_CONNECTING:
            send_color(48, 32, 0);      /* amber */
            break;
        case STATUS_RGB_TIME_INVALID:
            send_color(48, 0, 48);      /* magenta */
            break;
        case STATUS_RGB_NORMAL:
            send_color(0, 24, 0);       /* dim green */
            break;
        case STATUS_RGB_FAULT:
            send_color(48, 0, 0);       /* red */
            break;
        default:
            send_color(0, 0, 0);
            break;
    }
}
