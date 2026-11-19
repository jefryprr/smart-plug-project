# SELV Carrier REV_D_CORE_ONLY — 100 × 70 mm

**Status:** `ROUTED_PROTOTYPE / ENGINEERING_REVIEW_REQUIRED / NOT_FOR_FABRICATION`

## What it is

A 2-layer SELV carrier for:

- ESP32-S3-DevKitC-1 (two 1x22 sockets, 22.86 mm row spacing; pin 1 / USB end marked)
- PZEM-004T V4 TTL: 5V/GND, 5V TX → 10k/20k divider → GPIO18, GPIO17 → 74HCT125 → PZEM RX
- 2-channel relay module: 5V/GND/IN1/IN2; AO3400 pulls both inputs low
- Physical button; onboard DevKitC-1 v1.0 RGB GPIO48 (not a carrier net)
- 5V input from the REV_D_CORE_ONLY PSU board J5 (the PTC/TVS are on the PSU board, not the carrier)

No mains. No TMP102. No ADuM1201/B0505S. PZEM internal optocouplers are the
UART galvanic barrier.

## DevKit header map

| Carrier | DevKit header | Pin | Signal |
|---|---|---|---|
| J1A | J1 | 1, 2 | +3V3 |
| J1A | J1 | 4 | GPIO4 / RELAY_CTRL |
| J1A | J1 | 5 | GPIO5 / BUTTON |
| J1A | J1 | 10 | GPIO17 / PZEM_TX_3V3 |
| J1A | J1 | 11 | GPIO18 / PZEM_RX_3V3 |
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
- Nets: 11 named; footprints: 23 total (16 assembled + 3 fiducials + 4 mounting holes); board: 100 x 70 mm
- 5 V input: JST-XH J8 from PSU J5; no PTC/TVS on the carrier; 3 fiducials
- Gerber/drill/POS exported by KiCad 10.0.8

## What is not proven

- Physical fit, connector pinout, and footprint vendor review
- PZEM internal isolation/creepage/hipot
- Thermal/load/relay lifecycle
- PE continuity and enclosure flammability
- Firmware PZEM/UART/time-service/onboard-RGB integration

Do not fabricate or energize mains from this design without engineer review and
lab testing.
