# 08 — Baca Schematic dan GPIO

## Schematic

- Root: `hardware/kicad/smartplug.kicad_sch` (9 blok).
- Child: `AC_INPUT_OUTPUT`, `SAFETY_AND_SWITCH`, `AC_DC_POWER`, `PZEM_AND_CT`, `LOW_VOLTAGE_CONTROL`, `ESP32S3_CARRIER`, `DISPLAY_AND_BUTTONS`, `RTC_ONLY`, `SERVICE_AND_DEBUG`.
- Ini **system block schematic**, bukan komponen penuh.

## GPIO

- `hardware/interfaces/gpio_map.yaml/.csv/.md`
- `firmware/main/board_config.h`
- `validation/GPIO_CROSSCHECK.json` — status `UNVERIFIED` karena board revision belum diverifikasi.

## Aturan

- Jangan memakai GPIO0/3/45/46 (strapping), 19/20 (USB), 26–37 (flash/PSRAM).
- Relay control butuh pulldown eksternal.
- Jangan menganggap GPIO48/38 universal untuk RGB.
- Verifikasi board fisik sebelum final.
