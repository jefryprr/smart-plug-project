# Failure Mode and Effects Analysis (FMEA) — REV_B

**Status:** `DRAFT`
**Skala:** Severity/Probability/Detection = High/Medium/Low (kualitatif). Tidak ada RPN numerik palsu.

| ID | Failure mode | Efek | Severity | Probability | Detection | Mitigasi | Residual risk |
|---|---|---|---|---|---|---|---|
| FM-01 | Relay contact weld (one channel) | Beban tetap ON walau commanded OFF, atau satu konduktor tetap terhubung | High | Medium | Low tanpa feedback | Module rated, fuse/thermal backup, optional feedback, label, manual disconnect, two-channel review | High; physical test required |
| FM-02 | Relay fails open (one channel) | Beban tidak menyala atau hanya satu kutub terbuka | Medium | Medium | Medium (state/telemetry) | Detect no current when commanded ON; alert; inspect both channels | Medium |
| FM-03 | Relay coil driver stuck ON | Relay tidak bisa OFF | High | Low | Low | Gate pulldown, watchdog, independent cutoff, boot-safe test | Medium |
| FM-04 | Fuse opens | Beban mati | Medium | Medium | Medium | Correct fuse, spare, service procedure | Low |
| FM-05 | Fuse holder overheats | Melting/fire | High | Medium | Medium (thermal) | Rated holder, torque, thermal cutoff, test | Medium |
| FM-06 | MOV short at end-of-life | Fuse opens or fire | High | Low | Low | Thermal fuse coordination, rated MOV, test | Medium |
| FM-07 | PSU failure | SELV off; relay drops | Medium | Medium | High | Isolated PSU, fuse, watchdog, safe OFF | Low/medium |
| FM-08 | PSU isolation failure (HLK-5M05) | Mains reaches SELV/USB | High | Low | Low | Verified-isolation PSU, barrier, hipot/leakage test; batch certificate | High until tested |
| FM-09 | PZEM internal optocoupler isolation failure | Mains reaches ESP32/carrier | High | Low | Low | PZEM batch inspection, creepage, hipot/leakage; no external barrier | High until tested |
| FM-10 | PZEM UART CRC/timeout | Wrong/stale reading | Medium | High | High | CRC, timeout, invalid state, no stale live | Low |
| FM-11 | CT on wrong conductor | Wrong current/PF | Medium | Medium | Medium | Label, single-conductor guide, direction arrow, test | Medium |
| FM-12 | No temperature sensor installed (REV_B) | Firmware cannot detect overheat; only fuse/TCO respond | High | Medium | Low | Independent one-shot TCO, fuse, thermal test, label, load limits | High until tested |
| FM-13 | MCU hang | No control/telemetry | Medium | Medium | High | Watchdog, relay default OFF, independent protection | Medium |
| FM-14 | Boot GPIO float → relay ON | Unintended ON | High | Low | Medium | Pulldown, boot-safe test, relay driver default | Low after test |
| FM-15 | OTA bad image | Boot loop/recovery loss | High | Medium | Medium | Dual OTA, rollback, signed image, default OFF | Medium |
| FM-16 | Wi-Fi/cloud down | No remote control | Low | High | High | Local button/schedule, offline UI | Low |
| FM-17 | Clock invalid | Schedule ON blocked | Medium | Medium | High | RTC/SNTP validity, no auto ON | Low |
| FM-18 | NVS corruption | Config loss | Medium | Low | Medium | Versioned config, defaults OFF, backup | Low |
| FM-19 | PE discontinuity | Shock hazard | High | Low | Low | Dedicated PE, no relay/fuse, continuity test | High until tested |
| FM-20 | Socket/terminal loose | Overheat/fire | High | Medium | Medium | Rated parts, torque, strain relief, thermal test | High until tested |
| FM-21 | USB connected while mains | Shock/damage | High | Medium | Low | Service cover, label, procedure, isolation | High until tested |
| FM-22 | Enclosure material ignition | Fire spread | High | Low | Low | Flame-retardant rated material, thermal test | High until selected |
| FM-23 | Command replay | Unintended ON | High | Medium | High | command_id, sequence, TTL, dedup | Low |
| FM-24 | Cloud/API compromise | Unauthorized ON | High | Medium | Medium | Auth, RBAC, TLS, audit, local lockout | Medium |
| FM-25 | Two module channels not mechanically linked | One channel opens/welds while the other stays; false two-pole assumption | High | Medium | Low | Do not claim DPST; thermal/fuse backup; test each channel; consider contactors | High until tested |
| FM-26 | Firmware allows ON with no thermal monitoring | Overheat not detected until TCO opens | High | Medium | Low | Treat as accepted prototype risk; TCO/fuse mandatory; thermal test; do not claim production safety | High until tested |

## Prioritas

1. FM-01, FM-08, FM-09, FM-19, FM-20, FM-21, FM-22 — keselamatan fisik; `BLOCKED` sampai uji/review.
2. FM-03, FM-12, FM-14, FM-15 — firmware/safety; unit test/low-voltage fixture.
3. FM-23, FM-24 — software/security; integration/negative tests.

## Catatan

- FMEA ini belum ditandatangani engineer.
- Mitigasi firmware tidak menggantikan proteksi independen.
- Setiap perubahan relay/PSU/fuse/PE/enclosure memicu revisi FMEA.
