# SELV Carrier REV_B — 100 × 70 mm

**Status:** `ROUTED_PROTOTYPE / ENGINEERING_REVIEW_REQUIRED / NOT_FOR_FABRICATION`

## What it is

A 2-layer SELV carrier for:

- ESP32-S3-DevKitC-1 (two 1x22 sockets, 22.86 mm row spacing; pin 1 / USB end marked)
- PZEM-004T V4 TTL: 5V/GND, 5V TX → 10k/20k divider → GPIO18, GPIO17 → 74HCT125 → PZEM RX
- 2-channel relay module: 5V/GND/IN1/IN2; AO3400 pulls both inputs low
- OLED (I2C), DS3231 RTC (I2C + INT), button, WS2812 data via 74HCT125
- 5V input from HLK-5M05

No mains. No TMP102. No ADuM1201/B0505S. PZEM internal optocouplers are the
UART galvanic barrier.

## DevKit header map

| Carrier | DevKit header | Pin | Signal |
|---|---|---|---|
| J1A | J1 | 1, 2 | +3V3 |
| J1A | J1 | 4 | GPIO4 / RELAY_CTRL |
| J1A | J1 | 5 | GPIO5 / BUTTON |
| J1A | J1 | 7 | GPIO7 / RTC_INT |
| J1A | J1 | 10 | GPIO17 / PZEM_TX_3V3 |
| J1A | J1 | 11 | GPIO18 / PZEM_RX_3V3 |
| J1A | J1 | 12 | GPIO8 / SDA |
| J1A | J1 | 15 | GPIO9 / SCL |
| J1A | J1 | 16 | GPIO10 / RGB_DATA_3V3 |
| J1A | J1 | 21 | +5V |
| J1A | J1 | 22 | GND |
| J1B | J3 | 1, 21, 22 | GND |

Row spacing is **22.86 mm**. Pin 1 is at the left end; USB is at the right end.
Do not use a 2x22 IDC socket (2.54 mm rows); it will not fit. See
`docs/decisions/ADR-015-DEVKITC-1-SOCKET.md`.

## Files

- `hardware/kicad/smartplug.kicad_pcb` — routed board
- `hardware/carrier/netlist.csv` — every pad/net/position
- `hardware/carrier/placement.json` — footprint placement
- `hardware/schematic/carrier_schematic.svg/.png` — functional schematic
- `hardware/manufacturing/provisional/` — Gerber/drill/POS, not released

## Digital verification

- DRC: **0 violations / 0 unconnected** at 0.15 mm default clearance
- ERC (block schematic): **0 violations**
- Nets: 18; footprints: 22; board: 100 × 70 mm
- Gerber/drill/POS exported by KiCad 10.0.8

## What is not proven

- Physical fit, connector pinout, and footprint vendor review
- PZEM internal isolation/creepage/hipot
- Thermal/load/relay lifecycle
- PE continuity and enclosure flammability
- Firmware PZEM/UART/OLED/RTC integration

Do not fabricate or energize mains from this design without engineer review and
lab testing.
