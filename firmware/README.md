# Firmware ESP32-S3 — REV_A_PROVISIONAL

**Host core tests:** `PASS` — 74 checks, 0 failures (compiled with Zig 0.17.1 `zig cc`).
**ESP-IDF build:** `PASS` — ESP-IDF v6.1, target `esp32s3`; `.bin` exists. No board was flashed.
**Target:** ESP32-S3-DevKitC-1 N16R8, revision unverified.
**Load rating:** 8 A / ~1.840 W final (electronics/SMPS only).
**Relay:** off-board common 2-channel 5 V optocoupler module (active-LOW assumed), not a DPST.
**Framework decision:** ESP-IDF v6.1 (ADR-004).

## Build evidence

| Item | Value |
|---|---|
| Command | `powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1` |
| Exit code | 0 |
| Binary | `firmware/build/smartplug.bin` |
| Size | 192,464 bytes (0x2EFD0) |
| SHA-256 | `4949EEEFE73526AC99E79AC8F8E97EB1E0790551D80ED922F32034C8F0321134` |
| Log | `reports/logs/firmware-idf-build.log` |
| Report | `reports/FIRMWARE_BUILD.md` |

This is a target build, not a hardware test. Flashing, boot-waveform, relay timing,
and sensor integration remain `BLOCKED` without a board and lab procedure.

## What is implemented

- `core/smartplug_core.c` — portable C state machine, command priority, TTL/replay/sequence checks, lockout, measurement validation, energy delta, weekly schedule evaluation, CRC16 Modbus, telemetry JSON formatting.
- `test/host/test_core.c` — 74 host assertions covering safe/unsafe command paths, sensor failures, energy reset/gap, schedule, CRC, and JSON NaN handling.
- `main/app_main.c` — minimal boot-safe local app: relay GPIO forced OFF, debounced button, core state machine, ON refused while meter/temperature are not valid.
- `main/board_config.h` — provisional GPIO profile; **not final** until board revision is verified.
- `components/smartplug_core/CMakeLists.txt` — ESP-IDF component wrapper for the portable core.
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
| Flash/boot waveform | `BLOCKED` | No board/scope; build only |
| Physical bench test | `BLOCKED` | No hardware/lab (Q26=A) |

## Host test

```powershell
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
```

The script uses the portable Zig compiler in `tools/zig/` and writes a log to
`reports/logs/firmware-host-test.log`.

## ESP-IDF build

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1
```

`scripts/idf_env.ps1` sets the ESP-IDF v6.1 paths and target toolchain without
the full `export.ps1` set (GDB, RISC-V, and ULP tools are not installed). The
build script performs `set-target esp32s3` and `build`, then verifies that
`firmware/build/smartplug.bin` exists.

Do not flash/energize mains. The first bench test must be low-voltage with a
relay coil/load simulator and a qualified procedure.

## Safety rules encoded

1. Relay GPIO is forced LOW before the main loop; external 100 kΩ pulldown is still required.
2. The GPIO drives a MOSFET that pulls both IN1/IN2 of the off-board active-LOW module; do not connect a floating GPIO directly.
3. `BOOT_SAFE` never accepts ON.
4. Lockout/fault rejects ON; OFF remains accepted.
5. Auto ON requires valid clock.
6. ON requires valid meter and temperature; missing sensors default to invalid.
7. Command replay, stale sequence, wrong device, expiry, and future timestamps are rejected.
8. OTA/rollback config defaults to OFF; no eFuse/secure boot action is automated.

## Build warnings accepted

ESP-IDF v6.1 emits Kconfig warnings from its own components (NimBLE, FATFS,
hex-literal deprecations). They do not fail the build. The build evidence and
warnings are recorded in `reports/FIRMWARE_BUILD.md`.
