#include "time_service.h"

#include <string.h>
#include <sys/time.h>
#include <time.h>

#include "esp_log.h"
#include "esp_sntp.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "nvs.h"

#include "board_config.h"

static const char *TAG = "time_service";
static const char *NVS_NAMESPACE = "time";
static const char *DEFAULT_TZ = TIME_DEFAULT_TIMEZONE;

static sp_time_status_t s_status;
static bool s_sntp_started = false;
static int64_t s_last_resync_ms = 0;

static int64_t now_ms(void) {
    return esp_timer_get_time() / 1000;
}

static bool plausible_utc_ms(int64_t utc_ms) {
    /* 2020-01-01 .. 2100-01-01. Reject epoch/zero and absurd values. */
    return utc_ms > 1577836800000LL && utc_ms < 4102444800000LL;
}

static void nvs_save(void) {
    nvs_handle_t handle;
    if (nvs_open(NVS_NAMESPACE, NVS_READWRITE, &handle) != ESP_OK) {
        return;
    }
    (void)nvs_set_i64(handle, "last_utc", s_status.last_known_utc_ms);
    (void)nvs_set_i64(handle, "last_sync", s_status.last_sync_ms);
    (void)nvs_set_u8(handle, "source", (uint8_t)s_status.source);
    (void)nvs_set_str(handle, "tz", s_status.timezone);
    (void)nvs_commit(handle);
    nvs_close(handle);
}

static void nvs_load(void) {
    nvs_handle_t handle;
    if (nvs_open(NVS_NAMESPACE, NVS_READONLY, &handle) != ESP_OK) {
        return;
    }
    int64_t value = 0;
    if (nvs_get_i64(handle, "last_utc", &value) == ESP_OK) {
        s_status.last_known_utc_ms = value;
    }
    /*
     * Deliberately do not restore last_sync as a valid sync. The persisted
     * last-known time is for display/log only. A new trusted sync is required
     * after every boot.
     */
    uint8_t source = 0;
    if (nvs_get_u8(handle, "source", &source) == ESP_OK && source <= SP_TIME_SOURCE_MANUAL) {
        s_status.source = (sp_time_source_t)source;
    }
    size_t length = sizeof(s_status.timezone);
    if (nvs_get_str(handle, "tz", s_status.timezone, &length) != ESP_OK) {
        strncpy(s_status.timezone, DEFAULT_TZ, sizeof(s_status.timezone) - 1);
    }
    nvs_close(handle);
}

static void apply_system_time(int64_t utc_ms) {
    struct timeval tv;
    tv.tv_sec = (time_t)(utc_ms / 1000);
    tv.tv_usec = (suseconds_t)((utc_ms % 1000) * 1000);
    (void)settimeofday(&tv, NULL);
}

static bool note_sync(sp_time_source_t source, int64_t utc_ms, const char *timezone) {
    if (!plausible_utc_ms(utc_ms)) {
        ESP_LOGW(TAG, "reject implausible sync source=%s", sp_time_source_name(source));
        return false;
    }
    s_status.valid = true;
    s_status.source = source;
    s_status.last_sync_ms = now_ms();
    s_status.last_known_utc_ms = utc_ms;
    if (timezone != NULL && timezone[0] != '\0') {
        strncpy(s_status.timezone, timezone, sizeof(s_status.timezone) - 1);
        s_status.timezone[sizeof(s_status.timezone) - 1] = '\0';
    }
    apply_system_time(utc_ms);
    nvs_save();
    ESP_LOGI(TAG, "time valid source=%s utc_ms=%lld tz=%s",
             sp_time_source_name(source), (long long)utc_ms, s_status.timezone);
    return true;
}

static void sntp_sync_cb(struct timeval *tv) {
    if (tv == NULL) {
        return;
    }
    int64_t utc_ms = (int64_t)tv->tv_sec * 1000LL + tv->tv_usec / 1000;
    (void)note_sync(SP_TIME_SOURCE_SNTP, utc_ms, s_status.timezone);
}

void time_service_init(void) {
    memset(&s_status, 0, sizeof(s_status));
    s_status.valid = false;
    s_status.source = SP_TIME_SOURCE_NONE;
    strncpy(s_status.timezone, DEFAULT_TZ, sizeof(s_status.timezone) - 1);
    nvs_load();
    /* Loaded value is display-only; keep valid=false and source=none. */
    s_status.valid = false;
    s_status.source = SP_TIME_SOURCE_NONE;
    s_status.last_sync_ms = 0;
    ESP_LOGW(TAG, "time invalid at boot; last_known=%lld (display only)",
             (long long)s_status.last_known_utc_ms);
}

void time_service_on_wifi_connected(void) {
    if (!s_sntp_started) {
        esp_sntp_setoperatingmode(ESP_SNTP_OPMODE_POLL);
        esp_sntp_setservername(0, TIME_SNTP_SERVER_1);
        esp_sntp_setservername(1, TIME_SNTP_SERVER_2);
        esp_sntp_set_time_sync_notification_cb(sntp_sync_cb);
        esp_sntp_set_sync_interval((uint32_t)TIME_SNTP_RESYNC_SECONDS * 1000u);
        esp_sntp_init();
        s_sntp_started = true;
        s_last_resync_ms = now_ms();
        ESP_LOGI(TAG, "SNTP started; resync interval %d s", TIME_SNTP_RESYNC_SECONDS);
        return;
    }
    /* Wi-Fi reconnect: force a fresh poll without trusting old time. */
    esp_sntp_stop();
    esp_sntp_init();
    s_last_resync_ms = now_ms();
    ESP_LOGI(TAG, "SNTP restarted after Wi-Fi reconnect");
}

void time_service_tick(int64_t now_value_ms) {
    if (s_status.valid && s_status.last_sync_ms > 0) {
        int64_t age = now_value_ms - s_status.last_sync_ms;
        if (age < 0 || age > (int64_t)TIME_MAX_AGE_SECONDS * 1000LL) {
            s_status.valid = false;
            s_status.source = SP_TIME_SOURCE_NONE;
            s_status.last_sync_ms = 0;
            ESP_LOGW(TAG, "time expired; schedule blocked");
        }
    }
    if (s_sntp_started && s_last_resync_ms > 0 &&
        now_value_ms - s_last_resync_ms > (int64_t)TIME_SNTP_RESYNC_SECONDS * 1000LL) {
        esp_sntp_stop();
        esp_sntp_init();
        s_last_resync_ms = now_value_ms;
    }
}

bool time_service_set_manual(int64_t utc_ms, const char *timezone) {
    return note_sync(SP_TIME_SOURCE_MANUAL, utc_ms, timezone);
}

bool time_service_set_from_api(int64_t utc_ms, const char *timezone) {
    return note_sync(SP_TIME_SOURCE_API, utc_ms, timezone);
}

bool time_service_set_from_mqtt(int64_t utc_ms) {
    return note_sync(SP_TIME_SOURCE_MQTT, utc_ms, s_status.timezone);
}

bool time_service_is_valid(int64_t now_value_ms) {
    if (!s_status.valid || s_status.last_sync_ms <= 0) {
        return false;
    }
    int64_t age = now_value_ms - s_status.last_sync_ms;
    return age >= 0 && age <= (int64_t)TIME_MAX_AGE_SECONDS * 1000LL;
}

sp_time_status_t time_service_status(int64_t now_value_ms) {
    sp_time_status_t copy = s_status;
    copy.valid = time_service_is_valid(now_value_ms);
    if (!copy.valid) {
        copy.source = SP_TIME_SOURCE_NONE;
    }
    return copy;
}

const char *time_service_timezone(void) {
    return s_status.timezone;
}
