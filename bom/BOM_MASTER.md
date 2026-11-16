# BOM Master — REV_C_PSU_BOARD

**Generated:** 2026-11-16T06:14:44.651292+00:00

> **DESIGN BOM (UNPRICED) / NOT APPROVED.** Ini adalah BOM rekayasa, bukan daftar belanja.
> Harga, stok, dan tautan pembelian ada di `BOM_PROCUREMENT.md` / `BOM_PROCUREMENT.csv`.
> Status safety-critical: lihat `COMPONENT_APPROVALS.yaml`.

| Item | Ref | Category | Description | MPN | Qty | Status |
|---|---|---|---|---|---:|---|
| E-001 | U1 | MCU | ESP32-S3 DevKitC-1, N16R8 (official preferred; compatible board allowed only as a documented deviation) | ESP32-S3-DevKitC-1-N16R8 | 1 pcs | PENDING_APPROVAL |
| E-002 | U2 | Metering | PZEM-004T V4 AC energy meter, 100 A CT (closed or split), TTL/Modbus | PZEM-004T-V4-100A-CT | 1 pcs | DOCUMENTATION_DEFICIENT |
| E-003 | PS1 | Power | AC/DC 5 V 1 A isolated power module, 5 W, 90-264 VAC input (on REV_C PSU board) | HLK-5M05 | 1 pcs | PENDING_APPROVAL |
| E-005 | U5 | Sensing | I2C real-time clock with integrated crystal, 3.3 V | DS3231MZ+ | 1 pcs | PENDING_APPROVAL |
| E-008 | Q1 | Switching | N-channel MOSFET relay driver, logic-level, SOT-23 | AO3400A | 1 pcs | PENDING_APPROVAL |
| E-009 | U9 | UI/Level shift | Quad buffer/level shifter, 5 V powered, DIP-14, for PZEM TX and WS2812 data | SN74HCT125N | 1 pcs | PENDING_APPROVAL |
| E-010 | K1 | Switching | 2-channel 5 V optocoupler relay module, 10 A class claim, off-board, active-low input | 2CH-5V-OPTO-10A | 1 pcs | DOCUMENTATION_DEFICIENT |
| E-010A | BRK1 | Mechanical | Relay module mounting bracket/standoffs, flame-retardant, M3 | BRACKET-2CH-RELAY | 1 pcs | PROVISIONAL |
| E-010B | BRK2 | Mechanical | PZEM-004T mounting bracket/standoffs, flame-retardant, M3 | BRACKET-PZEM-V4 | 1 pcs | PROVISIONAL |
| E-011 | F1 | Protection | Fuse, 5x20 mm, 10 A, 250 VAC, time-lag | 0215010.MXP | 1 pcs | PENDING_APPROVAL |
| E-012 | FH1 | Protection | PCB fuse clips for 5x20 mm fuse, 10 A / 250 V, 2 pcs | 01110506Z | 1 pcs | PENDING_APPROVAL |
| E-013 | MOV1 | Protection | Metal-oxide varistor, 275 VAC, 10 mm, surge coordination study required | B72210S0271K101 | 1 pcs | PENDING_APPROVAL |
| E-014 | TF1 | Protection | One-shot thermal cutoff, 99 C rated functioning temperature, 10 A / 250 VAC | SF96E | 1 pcs | PROVISIONAL |
| E-015 | D1 | Passives | Flyback diode for relay coil, 1 A / 1000 V | 1N4007-E3/54 | 1 pcs | PROVISIONAL |
| E-016 | R1 | Passives | Gate series resistor, 1 kohm, 1%, 0805 | RC0805FR-071KL | 1 pcs | PROVISIONAL |
| E-017 | R2 | Passives | Gate pulldown resistor, 100 kohm, 1%, 0805 | RC0805FR-07100KL | 1 pcs | PROVISIONAL |
| E-018 | R3 | Passives | WS2812 data series resistor, 330 ohm, 0805 | RC0805FR-07330RL | 1 pcs | PROVISIONAL |
| E-050 | F2 | Protection | Resettable PTC fuse, 1.1 A hold, 1206, 5 V rail | 1206L110THYR | 1 pcs | PROVISIONAL |
| E-051 | D1 | Protection | TVS diode, 5 V standoff, 400 W, SMB | SMBJ5.0A | 1 pcs | PROVISIONAL |
| E-052 | PSU_PCB | PCB | Mains-entry PSU PCB, 2-layer FR4, 1.6 mm, 2 oz Cu target, 50 x 65 mm, routed | PCB-PSU-REV-C | 1 pcs | PROVISIONAL |
| E-053 | J5,J6,J7 | Connectors | JST-XH 2-pin PCB connector for 5 V outputs, 3 pcs | B2B-XH-A | 1 pcs | PROVISIONAL |
| E-054 | W5V1,W5V2,W5V3 | Connectors | JST-XH 2-pin cable for 5 V outputs, 3 pcs, 0.2 m | B2B-XH-A cable | 1 pcs | PROVISIONAL |
| E-055 | TB2 | Connectors | Mains output terminal block, 2-pin, 5.08 mm, 17.5 A / 250 V, screw clamp | MKDS 1,5/2-5,08 | 1 pcs | PROVISIONAL |
| E-019 | C1 | Passives | Bulk capacitor, 100 uF, 10 V, low ESR, 6.3x5.4 mm | UWT1A101MCL1GS | 1 pcs | PROVISIONAL |
| E-020 | C2 | Passives | Decoupling capacitor, 100 nF, 50 V, 0603 | GRM188R71H104KA93D | 1 pcs | PROVISIONAL |
| E-020A | C3 | Passives | Decoupling capacitor, 100 nF, 50 V, 0603, at 74HCT125 VCC | GRM188R71H104KA93D | 1 pcs | PROVISIONAL |
| E-018A | R4 | Passives | PZEM TX divider top resistor, 10 kohm, 1%, 0805 | RC0805FR-0710KL | 1 pcs | PROVISIONAL |
| E-018B | R5 | Passives | PZEM TX divider bottom resistor, 20 kohm, 1%, 0805 | RC0805FR-0720KL | 1 pcs | PROVISIONAL |
| E-018C | R6 | Passives | I2C SDA pullup, 4.7 kohm, 1%, 0805 | RC0805FR-074K7L | 1 pcs | PROVISIONAL |
| E-018D | R7 | Passives | I2C SCL pullup, 4.7 kohm, 1%, 0805 | RC0805FR-074K7L | 1 pcs | PROVISIONAL |
| E-018E | R8 | Passives | Button pullup, 10 kohm, 1%, 0805 | RC0805FR-0710KL | 1 pcs | PROVISIONAL |
| E-021 | DS1 | UI | OLED 0.96 inch, 128x64, SSD1306, I2C, 3.3 V module | OLED-096-SSD1306-I2C | 1 pcs | DOCUMENTATION_DEFICIENT |
| E-022 | LED1 | UI | Addressable RGB LED, WS2812B, 5050, 5 V | WS2812B-5050 | 1 pcs | PENDING_APPROVAL |
| E-023 | SW1 | UI | Tactile pushbutton, 6x6 mm, through-hole, panel cap | B3F-1000 | 1 pcs | PENDING_APPROVAL |
| E-024 | J1A,J1B | Connectors | 2 pcs 1x22 female header strips (one 2x22 strip split into two rows), 2.54 mm, 22.86 mm row spacing for DevKitC-1 | HDR-1X22-2.54-F | 1 pcs | PROVISIONAL |
| E-025 | J2 | Connectors | JST-XH 4-pin connector for PZEM TTL (5V, RX, TX, GND) | B4B-XH-A | 1 pcs | PROVISIONAL |
| E-026 | J3 | Connectors | JST-XH 4-pin connector for relay module (5V, GND, IN1, IN2) | B4B-XH-A | 1 pcs | PROVISIONAL |
| E-027 | J4 | Connectors | JST-XH 4-pin connector for OLED (3.3V, GND, SDA, SCL) | B4B-XH-A | 1 pcs | PROVISIONAL |
| E-028 | J5 | Connectors | JST-XH 6-pin connector for RTC (3.3V, GND, SDA, SCL, INT, 32K) | B6B-XH-A | 1 pcs | PROVISIONAL |
| E-047 | J6 | Connectors | JST-XH 2-pin connector for button (BUTTON, GND) | B2B-XH-A | 1 pcs | PROVISIONAL |
| E-048 | J7 | Connectors | JST-XH 3-pin connector for RGB (5V, GND, DATA) | B3B-XH-A | 1 pcs | PROVISIONAL |
| E-049 | J8 | Connectors | JST-XH 2-pin connector for 5V input from HLK-5M05 | B2B-XH-A | 1 pcs | PROVISIONAL |
| E-029 | TB1 | Connectors | Mains input terminal block, 2-pin, 5.08 mm, 17.5 A / 250 V, screw clamp | MKDS 1,5/2-5,08 | 1 pcs | PROVISIONAL |
| E-030 | TB_PE | Connectors | Protective earth terminal/stud, screw-clamp, tool-access | PE-TERMINAL-TBD | 1 pcs | BLOCKED |
| E-034 | X1 | Connectors | Type F (Schuko) panel socket, 16 A / 250 V, 2P+E | SIMON-SCHUKO-16A | 1 pcs | DOCUMENTATION_DEFICIENT |
| E-035 | P1 | Connectors | Type F (Schuko) cord plug, 16 A / 250 V, 3-core | BP16 | 1 pcs | DOCUMENTATION_DEFICIENT |
| E-036 | CG1 | Mechanical | Cable gland, M16, IP68, PA66, UL94 V-0 | GLAND-M16-TBD | 1 pcs | PROVISIONAL |
| E-037 | ENC1 | Mechanical | Enclosure, ABS/PC, 220 x 120 x 70 mm confirmed, flame-retardant grade | MG-220X120X70-ABS | 1 pcs | BLOCKED |
| E-038 | PE1 | Mechanical | PE bonding hardware: screw, lock washer, nut, dedicated stud | PE-HARDWARE-TBD | 1 pcs | BLOCKED |
| E-039 | W1 | Cable | Mains cord, H05VV-F 3x1.5 mm2, 0.5 m provisional, brown/blue/green-yellow | H05VV-F-3G1.5 | 0.5 m | PROVISIONAL |
| E-040 | W2 | Cable | Low-voltage hookup wire assortment, 0.25 mm2, 300 V | HOOKUP-0.25MM2 | 3 m | PROVISIONAL |
| E-041 | PCB1 | PCB | SELV carrier PCB, 2-layer FR4, 1.6 mm, 1 oz Cu, 100 x 70 mm, routed | PCB-CARRIER-REV-C | 1 pcs | PROVISIONAL |
| E-042 | LAB1 | Labels | Safety/rating label set: rated voltage/current, warnings, serial/QR placeholder (prototype label tape) | LABEL-SET-REV-A | 1 pcs | BLOCKED |
| E-043 | HS1 | Consumables | Heat-shrink tubing assortment, flame-retardant | HEATSHRINK-5MM | 1 set | PROVISIONAL |
| E-044 | SC1 | Mechanical | M3x8 machine screws, nylon washers | M3X8-SCREW | 8 pcs | PROVISIONAL |
| E-045 | INS1 | Mechanical | M3 heat-set inserts for enclosure | M3-INSERT | 4 pcs | PROVISIONAL |
| E-046 | ST1 | Mechanical | M3 nylon standoff set for carrier PCB | M3-STANDOFF-12-NYLON | 4 pcs | PROVISIONAL |

## Catatan

- BOM ini tidak memuat harga; daftar belanja bertanggal ada di `BOM_PROCUREMENT.md`.
- Komponen mains (socket, plug, relay, fuse, PSU, PE, enclosure) belum disetujui.
- `qty_per_unit` adalah kebutuhan prototipe 1 unit; batch 10 unit belum dihitung.
- Lihat `research/COMPONENT_RESEARCH.md`, `research/PROCUREMENT_INDONESIA.md`, `research/UNKNOWN_SPECIFICATIONS.md`, dan `bom/COMPONENT_APPROVALS.yaml`.
