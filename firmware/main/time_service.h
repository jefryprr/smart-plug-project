#ifndef TIME_SERVICE_H
#define TIME_SERVICE_H

#include <stdbool.h>
#include <stdint.h>

#include "smartplug_core.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Time service for the CORE-only build.
 *
 * UTC is the internal reference. Asia/Jakarta is the display timezone
 * (UTC+7, no DST). SNTP is the primary source; API/MQTT/manual are fallbacks.
 * `valid` is only true after a trusted sync and while age <= 12 h.
 *
 * NVS stores last-known UTC/source/timezone for display/log only. It never
 * authorizes a schedule after boot.
 */
void time_service_init(void);
void time_service_on_wifi_connected(void);
void time_service_tick(int64_t now_ms);
bool time_service_set_manual(int64_t utc_ms, const char *timezone);
bool time_service_set_from_api(int64_t utc_ms, const char *timezone);
bool time_service_set_from_mqtt(int64_t utc_ms);
bool time_service_is_valid(int64_t now_ms);
sp_time_status_t time_service_status(int64_t now_ms);
const char *time_service_timezone(void);

#ifdef __cplusplus
}
#endif

#endif /* TIME_SERVICE_H */
