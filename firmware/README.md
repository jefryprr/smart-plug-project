# Firmware ESP32-S3 — REV_A_PROVISIONAL

**Host core tests:** `PASS` — 74 checks, 0 failures (compiled with Zig 0.17.1 `zig cc`).
**ESP-IDF build:** `BLOCKED: ESP_IDF_NOT_INSTALLED` — no binary is claimed.
**Target:** ESP32-S3-DevKitC-1 N16R8, revision unverified.
**Framework decision:** ESP-IDF (ADR-004), version to pin when installed.

## What is implemented

- `core/smartplug_core.c` — portable C state machine, command priority, TTL/replay/sequence checks, lockout, measurement validation, energy delta, weekly schedule evaluation, CRC16 Modbus, telemetry JSON formatting.
- `test/host/test_core.c` — 74 host assertions covering safe/unsafe command paths, sensor failures, energy reset/gap, schedule, CRC, and JSON NaN handling.
- `main/app_main.c` — minimal boot-safe local app: relay GPIO forced OFF, debounced button, core state machine, ON refused while meter/temperature are not valid.
- `main/board_config.h` — provisional GPIO profile; **not final** until board revision is verified.
- `partitions.csv`, `sdkconfig.defaults` — dual OTA partitions, 16 MB flash, rollback enabled, HTTPS OTA only.

## What is not implemented / blocked

| Area | Status | Note |
|---|---|---|
| PZEM UART driver | `NOT_IMPLEMENTED` | Isolation barrier and exact V4 protocol unverified |
| OLED/RGB UI | `NOT_IMPLEMENTED` | UI table exists in docs, firmware rendering pending |
| RTC/time service | `NOT_IMPLEMENTED` | Schedule core exists; time validity integration pending |
| Wi-Fi/provisioning/MQTT | `NOT_IMPLEMENTED` | Phase 2; transport contract exists in `packages/mqtt-contract` |
| OTA service | `NOT_IMPLEMENTED` | Partition/rollback config only |
| NVS config/diagnostics | `NOT_IMPLEMENTED` | Planned components |
| ESP-IDF build | `BLOCKED` | Toolchain not installed; no `.bin` artifact |
| Physical bench test | `BLOCKED` | No hardware/lab (Q26=A) |

## Host test

```powershell
powershell -ExecutionPolicy Bypass -File firmware/test/host/run_tests.ps1
```

The script uses the portable Zig compiler in `tools/zig/` and writes a log to `reports/logs/firmware-host-test.log`.

## ESP-IDF build (when toolchain is available)

```powershell
# Install ESP-IDF vX.Y.Z (pin the exact version), target esp32s3
idf.py set-target esp32s3
idf.py build
idf.py -p COMx flash monitor
```

Do not flash/energize mains. First bench test must be low-voltage with the relay coil/load simulator and a qualified procedure.

## Safety rules encoded

1. Relay GPIO is forced LOW before the main loop; external 100 kΩ pulldown is still required.
2. `BOOT_SAFE` never accepts ON.
3. Lockout/fault rejects ON; OFF remains accepted.
4. Auto ON requires valid clock.
5. ON requires valid meter and temperature; missing sensors default to invalid.
6. Command replay, stale sequence, wrong device, expiry, and future timestamps are rejected.
7. OTA/rollback config defaults to OFF; no eFuse/secure boot action is automated.
