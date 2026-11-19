# ADR-017 — CORE-only Build and Time Fail-Safe Without RTC

**Status:** Accepted as design input; physical validation `BLOCKED`  
**Date:** 2026-11-19  
**Supersedes:** FULL-stage UI as an active build item (OLED/RTC/external RGB)  
**Related:** ADR-014, ADR-015, ADR-016, `docs/SAFETY.md`

## Context

The project previously carried an OLED, a DS3231 RTC, an external WS2812 LED, I2C pullups, and their connectors. The user has fixed the build to **CORE-only** and the physical board to **ESP32-S3-DevKitC-1 N16R8 v1.0** (onboard RGB GPIO48, not v1.1 GPIO38).

Removing the RTC removes the hardware holdover. The device still needs a safe way to decide whether a schedule may run.

## Decision

1. **Active build is CORE-only.** OLED, RTC, external RGB, JST J4/J5/J7, 330R, 4.7k I2C pullups, and I2C nets are removed. FULL UI is `DEFERRED`, not deleted from the roadmap.
2. **Keep** the button, relay, PZEM, PSU board, fuse/MOV/TCO, PE, enclosure barrier, and all mains safety items.
3. **No replacement RTC hardware.** Time sources are:
   - SNTP (primary),
   - API fallback,
   - MQTT fallback,
   - manual owner/admin set.
4. Internal time is UTC. UI displays Asia/Jakarta (UTC+7, no DST).
5. `time_valid` is true only after a trusted sync and while age ≤ `TIME_MAX_AGE` (default 12 h, configurable). SNTP resyncs at boot, on Wi-Fi reconnect, and every 6 h.
6. NVS stores `last_known_utc`, `last_sync_utc`, `last_sync_source`, and timezone. **Last-known is display/log only and must never authorize a schedule.**
7. At boot `time_valid=false`. Schedules cannot be created/enabled/executed; schedule-origin output is forced OFF; missed events are not replayed. Manual button/web/API control remains allowed unless a separate lockout exists.
8. API/MQTT expose `time_valid`, `time_source`, `last_sync`, `last_known_time`, `time_age_s`. Manual set is owner/admin, authenticated, audited (`TIME_SET_MANUAL`).
9. Onboard RGB GPIO48 is the status indicator: boot, Wi-Fi connecting, time invalid, normal, fault/lockout. It is not a safety indicator.
10. Board profile is `esp32s3_devkitc1_v1.0`; firmware defaults `BOARD_DEVKITC1_REV=10`, `PIN_STATUS_RGB=48`, `BOARD_REVISION_VERIFIED=1`, source `user-confirmed`.

## Consequences

- No RTC holdover. A device that boots offline with no trusted time cannot run schedules until SNTP/API/MQTT/manual sync succeeds.
- SNTP is unauthenticated. API/MQTT cross-check is recommended when online; log conflicts.
- Time jumps must be sanity-checked; implausible values are rejected.
- Web/Android must show the invalid-time banner and disable schedule editing.
- The carrier shrinks; the enclosure loses the OLED/RTC top features and gets a small onboard-RGB window (position provisional).
- FULL UI can return only in a new revision with its own review.

## Alternatives

- Keep RTC: rejected by user; adds battery/holder/drift and another part.
- GPS/radio time: not selected.
- Allow schedules from last-known time: rejected; unsafe after long power loss/clock drift.

## Open items

- Physical verification of onboard RGB GPIO48 and light-pipe/window visibility.
- SNTP/API/MQTT conflict policy and clock-jump thresholds.
- NVS corruption/power-loss behavior.
- Timezone/DST handling outside Asia/Jakarta (fixed UTC+7 for this build).
- API/MQTT authentication and ACLs in production.
