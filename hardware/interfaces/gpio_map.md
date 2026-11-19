# GPIO Map — REV_D_CORE_ONLY

**Board:** ESP32-S3-DevKitC-1-N16R8 (v1.0 (user-confirmed))
**Status:** `PASS`

> Board v1.0 is user-confirmed; GPIO48 is locked for onboard RGB. This is not a physical measurement. Verify the board marking/photo before claiming official origin; clones are Q08=B.

| Function | GPIO | Direction | Pull/Boot | Hazard if high | Firmware define |
|---|---:|---|---|---|---|
| relay_control | 4 | output | 100 kΩ pulldown to GND + 1 kΩ series / LOW (external pulldown) | Relay coil energized -> output ON | `PIN_RELAY_CTRL` |
| relay_feedback_optional | 11 | input | 10 kΩ pullup (feedback module open-drain) / HIGH (not populated) | No direct hazard; feedback only | `PIN_RELAY_FEEDBACK` |
| button | 5 | input | 10 kΩ pullup; button to GND / HIGH | No direct hazard; long-press reset must be safe | `PIN_BUTTON` |
| pzem_uart_tx | 17 | output | none / HIGH (UART idle) | No direct hazard; SELV via PZEM internal isolation | `PIN_PZEM_TX` |
| pzem_uart_rx | 18 | input | 10 kΩ pullup / HIGH | No direct hazard; SELV via PZEM internal isolation | `PIN_PZEM_RX` |
| status_rgb_onboard | 48 | output | none; onboard / undefined until firmware initializes; do not use as safety indicator alone | No direct hazard; SELV | `PIN_STATUS_RGB` |

## Reserved

| Pins | Reason |
|---|---|
| 0, 3, 45, 46 | Strapping pins; avoid for relay/actuator. |
| 19, 20 | Native USB D-/D+; service only. |
| 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37 | Flash/PSRAM; N16R8 octal PSRAM. Do not use. |
| 43, 44 | UART0 console; reserve for debug. |
| 38 | Onboard RGB on v1.1 only; this project uses v1.0 GPIO48. Do not repurpose. |

## Crosscheck

- Firmware header: `firmware/main/board_config.h`
- Schematic: `hardware/kicad/smartplug.kicad_sch`
- Wiring: `hardware/wiring/main_harness.yaml`
- Issues: 0

**Catatan:** tabel ini adalah rencana, bukan bukti pengukuran. Boot-safe waveform dan I2C/UART scan wajib di bench low-voltage.
