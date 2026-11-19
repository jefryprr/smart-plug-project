# ADR-004 — Firmware Stack

**Status:** Accepted (Q23=A)
**Date:** 2026-11-15

## Context
The device needs OTA rollback, partition control, provisioning, watchdog, and a safety state machine. Arduino-ESP32 is simpler but the user chose ESP-IDF.

## Decision
- Use **ESP-IDF v6.1** (installed 2026-11-15) for ESP32-S3.
- Keep safety/domain logic in a **portable C core** (`firmware/core`) with host tests.
- Use dual OTA partitions, rollback config, HTTPS-only OTA, watchdog.
- Do not enable secure boot/flash encryption/eFuse without explicit approval and a recovery plan.
- Host tests use Zig `cc`; this tests the portable core, not the target build.
- The ESP-IDF v6.1 `esp32s3` target build is a separate gate (`T-HW-017`).

## Consequences
- ESP-IDF v6.1 target build produces `firmware/build/smartplug.bin`; this is a build artifact, not a hardware test.
- Core logic is testable without hardware (88 checks pass).
- ESP-IDF integration components (PZEM, Wi-Fi, MQTT, OTA, SNTP/NVS time) remain incomplete/partial. OLED/RTC/external RGB are deferred in REV_D_CORE_ONLY.
- Pin/board revision must be verified before final GPIO; flashing/boot-waveform tests remain `BLOCKED`.

## Alternatives
- Arduino-ESP32: rejected for rollback/security/provisioning control.
- MicroPython: rejected for safety-critical deterministic control.
