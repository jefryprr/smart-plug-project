# Unit Test Results — REV_C_PSU_BOARD

**Gate:** `PASS` (digital unit tests)
**Generated:** 2026-11-15
**Rule:** A unit test PASS does not imply hardware/HIL/PLN validation.

| Suite | Tests | Result | Command | Log |
|---|---:|---|---|---|
| Domain (`packages/domain`) | 34 | 34 PASS | `npm run test -w @smartplug/domain` | `reports/logs/T-SW-007-*.log` |
| MQTT contract (`packages/mqtt-contract`) | 11 | 11 PASS | `npm run test -w @smartplug/mqtt-contract` | `reports/logs/T-SW-004A-*.log` |
| Device simulator (`apps/device-simulator`) | 4 | 4 PASS | `npm run test -w @smartplug/device-simulator` | `reports/logs/T-SW-004B-*.log` |
| Firmware C core (`firmware/test/host`) | 74 checks | 0 failures | `powershell -File firmware/test/host/run_tests.ps1` | `reports/logs/firmware-host-test.log`, `T-HW-018-*.log` |
| API (`apps/api`) | 38 | 38 PASS | `npm run test -w @smartplug/api` | `reports/logs/T-SW-005-*.log` |

## Domain coverage highlights

- Command priority: lockout > OFF > user OFF > eligible ON.
- Replay, stale sequence, wrong device, expiry, future timestamp, invalid TTL.
- Boot/provisioning/updating/degraded modes block ON.
- Meter/temperature invalid block ON; OFF remains accepted.
- Measurement NaN/out-of-range/invalid quality handling.
- Energy delta: normal, counter reset/rollover, non-monotonic sequence, gap, implausible delta.
- Tariff history: no retroactive rewrite; missing tariff not Rp0.
- Schedule: weekday/window/already-ran.
- Freshness: ONLINE/STALE/OFFLINE/NEVER_SEEN.
- IDR formatting and secret redaction.

## Firmware C core coverage

- 74 assertions covering the same command/safety semantics, measurement validation, energy delta, schedule, CRC16 Modbus (`123456789` → `0x4B37`), and telemetry JSON (`NaN` → `null`).
- Compiled with Zig 0.17.1 `zig cc` on host. This is **not** an ESP-IDF target build.

## What is not covered

- ESP-IDF v6.1 target build (`PASS`; see `reports/FIRMWARE_BUILD.md`). Unit/fault-injection tests on target remain `BLOCKED` without hardware.
- Hardware drivers (PZEM, OLED, RGB, button, RTC, Wi-Fi).
- Physical sensor faults, relay weld, thermal, PE, isolation.
- Android runtime/emulator.
- PostgreSQL adapter.

## Reproduce

```powershell
npm run test
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
```
