# GPIO Map — REV_A_PROVISIONAL

**Board:** ESP32-S3-DevKitC-1-N16R8 (v1.1 (planned, unverified))
**Status:** `UNVERIFIED`

> Nomor GPIO belum final sampai board fisik/revisi diverifikasi. Jangan menganggap GPIO48/38 sebagai kebenaran universal.

| Function | GPIO | Direction | Pull/Boot | Hazard if high | Firmware define |
|---|---:|---|---|---|---|
| relay_control | 4 | output | 100 kΩ pulldown to GND + 1 kΩ series / LOW (external pulldown) | Relay coil energized -> output ON | `PIN_RELAY_CTRL` |
| relay_feedback_optional | 11 | input | 10 kΩ pullup (feedback module open-drain) / HIGH (not populated) | No direct hazard; feedback only | `PIN_RELAY_FEEDBACK` |
| button | 5 | input | 10 kΩ pullup; button to GND / HIGH | No direct hazard; long-press reset must be safe | `PIN_BUTTON` |
| i2c_sda | 8 | bidirectional | 4.7 kΩ to 3.3 V / HIGH (pullup) | No direct hazard; SELV | `PIN_I2C_SDA` |
| i2c_scl | 9 | output | 4.7 kΩ to 3.3 V / HIGH (pullup) | No direct hazard; SELV | `PIN_I2C_SCL` |
| oled_reset | 6 | output | 10 kΩ pullup / HIGH | No direct hazard; SELV | `PIN_OLED_RESET` |
| external_rgb_data | 10 | output | 330 Ω series; no pullup / LOW | No direct hazard; SELV | `PIN_RGB_DATA` |
| pzem_uart_tx | 17 | output | none / HIGH (UART idle) | No direct hazard; SELV via PZEM internal isolation | `PIN_PZEM_TX` |
| pzem_uart_rx | 18 | input | 10 kΩ pullup / HIGH | No direct hazard; SELV via PZEM internal isolation | `PIN_PZEM_RX` |
| rtc_interrupt | 7 | input | 10 kΩ pullup / HIGH | No direct hazard; SELV | `PIN_RTC_INT` |

## Reserved

| Pins | Reason |
|---|---|
| 0, 3, 45, 46 | Strapping pins; avoid for relay/actuator. |
| 19, 20 | Native USB D-/D+; service only. |
| 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37 | Flash/PSRAM; N16R8 octal PSRAM. Do not use. |
| 43, 44 | UART0 console; reserve for debug. |

## Crosscheck

- Firmware header: `firmware/main/board_config.h`
- Schematic: `hardware/kicad/smartplug.kicad_sch`
- Wiring: `hardware/wiring/main_harness.yaml`
- Issues: 10

**Catatan:** tabel ini adalah rencana, bukan bukti pengukuran. Boot-safe waveform dan I2C/UART scan wajib di bench low-voltage.
