# Firmware Build — ESP-IDF v6.1 / ESP32-S3

**Status:** `PASS` (target build only)
**Date:** 2026-11-15
**Design revision:** `REV_A_PROVISIONAL`

## Result

| Item | Value |
|---|---|
| Framework | ESP-IDF v6.1 |
| Target | esp32s3 |
| Toolchain | xtensa-esp-elf 15.2.0 (GCC 15.2.0) |
| CMake | 4.0.3 |
| Ninja | 1.12.1 |
| Python env | ESP-IDF Python 3.11.15 |
| Command | `powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1` |
| Exit code | 0 |
| Binary | `firmware/build/smartplug.bin` (mirror: `D:\AI INSTALLS\artifacts\smartplug.bin`) |
| Size | 192,464 bytes (0x2EFD0) |
| SHA-256 | `4949EEEFE73526AC99E79AC8F8E97EB1E0790551D80ED922F32034C8F0321134` |
| Log | `reports/logs/firmware-idf-build.log` |
| Partition free | 0x5D1030 of 0x600000 bytes (97%) |
| Bootloader free | 0x2D30 of 0x8000 bytes (35%) |

**Reproducibility note:** the hash is per-build, not a byte-for-byte reproducibility
claim. ESP-IDF embeds build/version metadata, so a rebuild of identical source can
produce a different hash at the same size. Use the current hash only to identify
this artifact; do not treat it as a deterministic source hash.

The build log ends with:

```text
Project build complete. To flash, run:
 idf.py flash
```

## What this proves

- The portable core (`firmware/core`) compiles as an ESP-IDF component.
- The minimal app (`firmware/main/app_main.c`) compiles and links for ESP32-S3.
- The dual-OTA partition table and `sdkconfig.defaults` are accepted.
- A real `.bin` exists with the hash above.

## What this does **not** prove

- No board was flashed.
- No boot waveform, relay timing, or boot-safe GPIO behavior was measured.
- PZEM, OLED, RGB, RTC, Wi-Fi, MQTT, OTA, and provisioning are not integrated.
- No thermal, isolation, PE, or mains test was performed.
- The binary is **not** released for use or fabrication.

## Build warnings accepted

ESP-IDF v6.1 emits Kconfig warnings from its own components (NimBLE
`BT_NIMBLE_MESH_PROVISIONER`, FATFS print options, hex-literal deprecations).
They are not errors and do not fail the build. The project-specific
`sdkconfig.defaults` was corrected to use `CONFIG_ESP_TASK_WDT_INIT` and to
remove obsolete `CONFIG_ESP_HTTPS_OTA_CHECK_CERT`.

## Reproduce

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1
```

The environment helper `scripts/idf_env.ps1` expects ESP-IDF under
`tools/esp-idf/v6.1/esp-idf` and tools under `C:\Espressif` (overridable with
`IDF_TOOLS_PATH`). It adds the Xtensa toolchain, CMake, Ninja, and ccache to
`PATH` without requiring the full `export.ps1` tool set.

**Safety:** build PASS is digital evidence only. Do not energize mains or flash a
prototype without the low-voltage bench procedure and a qualified engineer.
