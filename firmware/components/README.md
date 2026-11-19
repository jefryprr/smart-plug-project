# Firmware Components — Status Map

The PRD's component layout is mapped below. Only `smartplug_core` is fully
implemented and host-tested. Other components are planned and must not be
presented as integrated.

| Component | Path | Status | Evidence |
|---|---|---|---|
| Portable core | `core/` + `components/smartplug_core` | `IMPLEMENTED/TESTED` | 88 host checks |
| Platform board / GPIO | `main/board_config.h`, `main/app_main.c` | `PARTIAL` | relay safe init, button debounce; DevKitC-1 v1.0 user-confirmed, not measured |
| Meter service (PZEM) | `components/meter_service` (planned) | `NOT_IMPLEMENTED` | PZEM V4 protocol/isolation unverified |
| Power controller | `core/` | `PARTIAL` | state machine implemented; NVS/config wrapper pending |
| Safety monitor | `core/` | `PARTIAL` | validation/lockout logic implemented; sensor drivers pending |
| Scheduler | `core/` | `PARTIAL` | weekly evaluator + time-validity gate tested; hardware schedule execution blocked |
| Button service | `main/app_main.c` | `PARTIAL` | 50 ms debounce; long-press reset pending |
| Storage service | `components/storage_service` (planned) | `NOT_IMPLEMENTED` | — |
| Time service | `main/time_service.c` | `PARTIAL` | SNTP/NVS/API/MQTT/manual; no RTC; hardware test blocked | — |
| Diagnostics | `components/diagnostics` (planned) | `NOT_IMPLEMENTED` | — |
| Local transport | `components/transport_local` (planned) | `NOT_IMPLEMENTED` | Phase 2 |
| OTA service | `components/ota_service` (planned) | `NOT_IMPLEMENTED` | Partition/rollback config only |

## Build status

- Host core: `PASS` with Zig 0.17.1.
- ESP-IDF v6.1 target build: `PASS` for the minimal app; see `reports/FIRMWARE_BUILD.md`.
- Hardware/flash/boot test: `BLOCKED: NO_BOARD_OR_LAB`.

## Rule

Do not add a component to the "implemented" column without a build/test artifact
and a traceability entry. A directory name is not evidence.
