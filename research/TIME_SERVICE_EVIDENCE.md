# Time Service Evidence — SNTP, NVS, and DevKitC-1 v1.0 RGB

**Date:** 2026-11-19  
**Scope:** REV_D_CORE_ONLY, no RTC hardware.  
**Status:** design input; no physical test.

| Topic | Value used | Source | URL | Accessed | Confidence | Note |
|---|---|---|---|---|---|---|
| SNTP client | `esp_sntp` legacy API (lwip component), poll mode, servers `pool.ntp.org` / `time.google.com` | Espressif ESP-IDF SNTP docs | https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/network/esp_sntp.html | 2026-11-19 | HIGH | SNTP is **unauthenticated**; cross-check with API/MQTT when online. |
| SNTP resync | boot, Wi-Fi reconnect, every 6 h | Project design; `esp_sntp_set_sync_interval` | same | 2026-11-19 | DESIGN | Value configurable; not measured. |
| NVS | namespace `time`; keys `last_utc`, `last_sync`, `source`, `tz` | Espressif NVS docs | https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/storage/nvs_flash.html | 2026-11-19 | HIGH | Last-known is display/log only; `valid=false` at boot. |
| Time validity | 12 h max age (configurable) | Project decision / ADR-017 | local | 2026-11-19 | DESIGN | No trusted sync → schedules blocked. |
| DevKitC-1 v1.0 onboard RGB | GPIO48 | Espressif v1.0 user guide; user-confirmed board | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html | 2026-11-19 | MEDIUM/HIGH | v1.1 uses GPIO38; do not mix. Physical visibility/window unverified. |
| DevKitC-1 v1.1 difference | GPIO38 | Espressif v1.1 user guide | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html | 2026-11-19 | HIGH | Historical/comparison only; active build locks v1.0. |
| Header geometry | 2 × 1x22, 2.54 mm pitch, 22.86 mm row spacing; v1.0/v1.1 outline same | Espressif user guides/DXF review (user-provided) | same | 2026-11-19 | MEDIUM | Socket footprint unchanged; physical fit still required. |

## Residual risks

- SNTP spoofing or a wrong server can shift schedules. No authentication; API/MQTT cross-check is recommended.
- NVS corruption or power loss during write can lose the last-known value. It must never authorize schedules.
- Onboard RGB GPIO48 and the enclosure window are not physically verified.
- A clone board may differ in RGB pin/regulator; record Q08=B and verify.

## Decisions

- No DS3231/RTC hardware in REV_D.
- `time_valid=false` at boot; schedules blocked and schedule-origin output forced OFF.
- Manual button/web/API control remains allowed.
- Missed schedule events are not replayed.
