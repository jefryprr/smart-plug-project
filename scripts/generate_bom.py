#!/usr/bin/env python3
"""Generate BOM artifacts from a single structured source.

Prices are intentionally empty: no verified, dated Indonesian prices were
obtained. The PRD forbids Rp0 placeholders for unknown prices.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOM = ROOT / "bom"
BOM.mkdir(parents=True, exist_ok=True)

FIELDS = [
    "item_id",
    "reference_designators",
    "category",
    "description",
    "manufacturer",
    "manufacturer_part_number",
    "module_revision",
    "qty_per_unit",
    "unit",
    "price_idr_per_unit",
    "tax_shipment_included",
    "total_idr",
    "price_checked_at",
    "seller",
    "seller_url",
    "datasheet_url",
    "datasheet_revision",
    "approved_status",
    "alternative_mpn",
    "footprint_id",
    "mechanical_model",
    "supplier_stock_status",
    "rating_verified",
    "notes",
    "source_evidence",
]


def row(
    item_id: str,
    refs: str,
    category: str,
    description: str,
    manufacturer: str,
    mpn: str,
    *,
    revision: str = "-",
    qty: float = 1,
    unit: str = "pcs",
    datasheet: str = "",
    status: str = "PENDING_APPROVAL",
    alt: str = "",
    footprint: str = "TBD",
    mech: str = "TBD",
    notes: str = "",
    evidence: str = "",
) -> dict:
    return {
        "item_id": item_id,
        "reference_designators": refs,
        "category": category,
        "description": description,
        "manufacturer": manufacturer,
        "manufacturer_part_number": mpn,
        "module_revision": revision,
        "qty_per_unit": qty,
        "unit": unit,
        "price_idr_per_unit": "",
        "tax_shipment_included": "FALSE",
        "total_idr": "",
        "price_checked_at": "",
        "seller": "",
        "seller_url": "",
        "datasheet_url": datasheet,
        "datasheet_revision": "UNKNOWN",
        "approved_status": status,
        "alternative_mpn": alt,
        "footprint_id": footprint,
        "mechanical_model": mech,
        "supplier_stock_status": "UNKNOWN",
        "rating_verified": "FALSE",
        "notes": notes,
        "source_evidence": evidence,
    }


ROWS = [
    row(
        "E-001", "U1", "MCU", "ESP32-S3 DevKitC-1, N16R8 (16 MB flash, 8 MB PSRAM), v1.0",
        "Espressif", "ESP32-S3-DevKitC-1-N16R8", revision="v1.0 (user-confirmed)",
        datasheet="https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html",
        status="PENDING_APPROVAL", alt="ESP32-S3-DevKitC-1-N8R8; third-party clone (not preferred)",
        footprint="ESP32-S3-DevKitC-1_2x22", mech="esp32s3_devkitc1_approx",
        notes="User-confirmed v1.0; onboard RGB = GPIO48 (not v1.1 GPIO38). Firmware locks BOARD_DEVKITC1_REV=10 and PIN_STATUS_RGB=48. If the unit is a clone/compatible board, record Q08=B and do not claim official Espressif origin. N16R8 uses octal PSRAM; avoid GPIO33-37.",
        evidence="User statement 2026-11-19; Espressif v1.0 user guide. Physical marking/photo still recommended."
    ),
    row(
        "E-002", "U2", "Metering", "PZEM-004T V4 AC energy meter, 100 A split/open CT, TTL/Modbus",
        "Peacefair", "PZEM-004T-V4-100A-SPLIT", revision="V4 (unverified batch)",
        datasheet="https://github.com/im-0/pzem-004t-original-docs",
        status="DOCUMENTATION_DEFICIENT", alt="ADE7953 + CT + isolation; HLW8032 + shunt (not preferred)",
        footprint="OFF_BOARD_MODULE", mech="pzem004t_v4_approx",
        notes="Off-board module with dedicated enclosure bracket; not on the low-voltage PCB. Official Peacefair V4 datasheet for the exact batch is not verified. UART level, isolation, terminal rating, and CT ratio must be measured. Do not confuse CT rating with output current rating.",
        evidence="PRD retailer references are availability evidence only, not datasheet. Archive is historical and may not match the purchased V4."
    ),
    row(
        "E-003", "PS1", "Power", "AC/DC 5 V 1 A isolated power module, 5 W, 90-264 VAC input (on REV_D_CORE_ONLY PSU board)",
        "Hi-Link", "HLK-5M05", datasheet="https://www.hlktech.net/index.php?id=1243",
        status="PENDING_APPROVAL", alt="Mean Well IRM-05-5 (better documentation/certification, larger); Recom RAC01-05SC (too low current)",
        footprint="HLK_5M05_CUSTOM", mech="hlk_5m05_approx",
        notes="Selected by user. 38x23x18 mm, 4 pins (AC/AC/-Vo/+Vo), 5 V 1 A, 5 W. Datasheet claims 2500 VAC input-output isolation and UL/CE design compliance, but the exact batch certificate/isolation/creepage are unverified. Efficiency is only ~70% at 220 V full load, so ~2.1 W heat; thermal test is mandatory. Fuse/MOV/TCO are on the same REV_D_CORE_ONLY PSU board upstream. Do not touch AC pins; keep mains creepage and barrier.",
        evidence="Distributor copy of Hi-Link HLK-5M05 datasheet (3 pages) with dimension drawing; official product page; exact batch/certification must be verified."
    ),
    row(
        "E-005", "U5", "Sensing", "I2C real-time clock with integrated crystal, 3.3 V",
        "Analog Devices", "DS3231MZ+", datasheet="https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231M.pdf",
        status="DEFERRED_CORE_ONLY", alt="None in REV_D; SNTP/NVS/API/MQTT/manual time only",
        footprint="SO-16W", mech="DS3231_approx",
        notes="Battery/supercap holder and drift budget must be selected. Invalid clock blocks automatic ON.",
        evidence="Analog Devices DS3231M datasheet; RTC drift and backup runtime require measurement."
    ),
    row(
        "E-008", "Q1", "Switching", "N-channel MOSFET relay driver, logic-level, SOT-23",
        "Alpha & Omega Semiconductor", "AO3400A", datasheet="https://www.aosmd.com/res/data_sheets/AO3400A.pdf",
        status="PENDING_APPROVAL", alt="2N7002 (lower current); ULN2003 (module driver)",
        footprint="SOT-23", mech="AO3400_approx",
        notes="Low-side switch pulls both active-LOW module inputs down. Gate pulldown 100k and series 1k are mandatory for boot-safe OFF. No carrier flyback diode: the module has its own coil drivers. Verify total input current (~15-20 mA per channel), thermal, and module pinout.",
        evidence="AOS datasheet; boot waveform must be measured on a low-voltage fixture."
    ),
    row(
        "E-009", "U9", "UI/Level shift", "Quad buffer/level shifter, 5 V powered, DIP-14, for PZEM TX only",
        "Texas Instruments", "SN74HCT125N", datasheet="https://www.ti.com/lit/ds/symlink/sn74hct125.pdf",
        status="PENDING_APPROVAL", alt="74HCT125 (any vendor); SN74AHCT1G125 for one channel",
        footprint="DIP-14_W7.62mm", mech="DIP14_approx",
        notes="Converts ESP32 3.3 V logic to 5 V for PZEM RX only. 74HCT input threshold is TTL-compatible. Unused gates: inputs/OE tied to GND, outputs open; add 100 nF at VCC. Do not use for galvanic isolation.",
        evidence="TI SN74HCT125 datasheet; verify 5 V output levels and PZEM input current."
    ),
    row(
        "E-010", "K1", "Switching", "2-channel 5 V optocoupler relay module, 10 A class claim, off-board, active-low input",
        "Generic module (TBD)", "2CH-5V-OPTO-10A", revision="TBD batch",
        datasheet="https://www.handsontec.com/dataspecs/module/2Ch-relay.pdf",
        status="DOCUMENTATION_DEFICIENT", alt="TE RT2 DPST-NO 8A PCB relay (earlier concept); 2P 16A contactor (larger)",
        footprint="OFF_BOARD_MODULE", mech="relay_module_2ch_approx",
        notes="User-selected common 2-channel module, off-board, mounted in enclosure. Two independent SPDT channels (L/N); NOT mechanically linked DPST. 10A is a vendor claim, not validated continuous rating. Final 8A/1840W. Active-LOW input; verify JD-VCC/pinout. Do not claim safety-rated two-pole.",
        evidence="Handsontec 2Ch relay datasheet; DigiKey TS0010D; verify exact batch/pinout/rating on arrival."
    ),
    row(
        "E-010A", "BRK1", "Mechanical", "Relay module mounting bracket/standoffs, flame-retardant, M3",
        "TBD", "BRACKET-2CH-RELAY", status="PROVISIONAL", footprint="OFF_BOARD", mech="relay_bracket_approx",
        notes="Off-board module must be mechanically retained; no load on header/wires. Keep in mains zone, away from SELV carrier.",
        evidence="To be designed/printed; not certified."
    ),
    row(
        "E-010B", "BRK2", "Mechanical", "PZEM-004T mounting bracket/standoffs, flame-retardant, M3",
        "TBD", "BRACKET-PZEM-V4", status="PROVISIONAL", footprint="OFF_BOARD", mech="pzem_bracket_approx",
        notes="PZEM stands off the PCB in the mains zone; CT and voltage terminals accessible. Do not mount on SELV carrier.",
        evidence="To be designed/printed; dimensions approximate until sample measured."
    ),
    row(
        "E-011", "F1", "Protection", "Fuse, 5x20 mm, 10 A, 250 VAC, time-lag",
        "Littelfuse", "0215010.MXP", datasheet="https://www.littelfuse.com/assetdocs/215-series-datasheet?assetguid=...",
        status="PENDING_APPROVAL", alt="Schurter 0001.2510; Bel Fuse 5TT 10",
        footprint="FUSE_5x20_HOLDER", mech="fuse_5x20_approx",
        notes="Fuse is backup protection, not the only overcurrent protection. Breaking capacity, time-current curve, holder rating, and coordination must be reviewed. Provisional continuous load may be limited to 8 A.",
        evidence="Littelfuse 215 series; exact datasheet URL/revision to be captured. Do not use a random glass fuse."
    ),
    row(
        "E-012", "FH1", "Protection", "PCB fuse clips for 5x20 mm fuse, 10 A / 250 V, 2 pcs",
        "Littelfuse", "01110506Z",
        datasheet="https://www.littelfuse.com/products/fuses-overcurrent-protection/fuse-holders-fuse-blocks-accessories/fuse-accessories/fuse-clips/111/111505",
        status="PENDING_APPROVAL", alt="Schurter 0031.8201 closed holder (different footprint); Littelfuse 01110501Z",
        footprint="Fuseholder_Clip-5x20mm_Littelfuse_111", mech="fuse_clip_approx",
        notes="Two clips per fuse; matches the routed PSU board. Not a closed/touch-proof holder; fuse access requires opening the screwed lid. Clip rating 10 A/250 V is marginal at 8 A continuous; thermal test required. Tool-access and service procedure required.",
        evidence="Littelfuse 111 series product page: 5x20 mm clip, 250 V, 10 A."
    ),
    row(
        "E-013", "MOV1", "Protection", "Metal-oxide varistor, 275 VAC, 10 mm, surge coordination study required",
        "EPCOS (TDK)", "B72210S0271K101", datasheet="https://www.tdk-electronics.tdk.com/inf/70/db/varistors/leaded_sio_v_series.pdf",
        status="PENDING_APPROVAL", alt="Littelfuse V275LA10P; Bourns MOV-10D271K",
        footprint="MOV_10MM", mech="mov_10mm_approx",
        notes="MOV alone is not a complete surge protection design. End-of-life failure mode, thermal fuse coordination, and standard applicability must be reviewed. Do not claim surge suppression until tested.",
        evidence="TDK/EPCOS SIOV series; exact part rating to be verified."
    ),
    row(
        "E-014", "TF1", "Protection", "One-shot thermal cutoff, 99 C rated functioning temperature, 10 A / 250 VAC",
        "Sefuse", "SF96E", datasheet="https://docs.rs-online.com/68de/0900766b81546f0c.pdf",
        status="PROVISIONAL", alt="Therm-O-Disc one-shot 99 C; KSD301 / Bourns LC auto-reset are NOT equivalent",
        footprint="TCO_AXIAL", mech="tco_approx",
        notes="SF96E rated functioning temperature 99 C (marked 96 C), holding temperature 84 C, 10 A resistive / 250 VAC. NOT SF169E (172 C). Must be mechanically clamped to the hottest terminal/HLK/PCB spot and be independent of firmware; normal-operation hotspot must stay below 84 C with margin. Batch certificate and trip test still required.",
        evidence="SEFUSE SF/E series datasheet (RS mirror), accessed 2026-11-16: ratings table lists SF96E 99 C, 10 A; SF169E is 172 C."
    ),
    row(
        "E-015", "D1", "Passives", "Flyback diode for relay coil, 1 A / 1000 V",
        "Vishay", "1N4007-E3/54", datasheet="https://www.vishay.com/docs/88503/1n4001.pdf",
        status="PROVISIONAL", alt="SS34 Schottky; 1N4148 for small coils",
        footprint="DO-41", mech="DO41_approx",
        notes="Cathode to +5 V, anode to coil low side. Verify coil current and reverse voltage.",
        evidence="Vishay 1N400x datasheet."
    ),
    row(
        "E-016", "R1", "Passives", "Gate series resistor, 1 kohm, 1%, 0805", "Yageo", "RC0805FR-071KL",
        datasheet="https://www.yageo.com/upload/media/product/productsearch/datasheet/rchip/RC0805FR-071KL.pdf",
        status="PROVISIONAL", footprint="R_0805_2012Metric", mech="R0805_approx", notes="Relay driver gate.", evidence="Yageo datasheet."
    ),
    row(
        "E-017", "R2", "Passives", "Gate pulldown resistor, 100 kohm, 1%, 0805", "Yageo", "RC0805FR-07100KL",
        datasheet="https://www.yageo.com/", status="PROVISIONAL", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="Mandatory to keep relay driver OFF while MCU pin floats at boot.", evidence="Yageo datasheet."
    ),
    row(
        "E-018", "R3", "Passives", "WS2812 data series resistor, 330 ohm, 0805", "Yageo", "RC0805FR-07330RL",
        datasheet="https://www.yageo.com/", status="DEFERRED_CORE_ONLY", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="Place close to LED data input.", evidence="Yageo datasheet."
    ),
    row(
        "E-050", "F2", "Protection", "Resettable PTC fuse, 1.1 A hold, 1206, 5 V rail", "Littelfuse", "1206L110THYR",
        status="PROVISIONAL", footprint="Fuse_1206_3216Metric", mech="fuse_1206_approx",
        notes="Protects the PSU board total 5 V output (J5/J6/J7) and wiring. Hold current 1.1 A; verify trip time and voltage drop. Not a substitute for the mains fuse. The carrier has no PTC.",
        evidence="Littelfuse 1206L series datasheet; exact batch to be verified."
    ),
    row(
        "E-051", "D1", "Protection", "TVS diode, 5 V standoff, 400 W, SMB", "Littelfuse", "SMBJ5.0A",
        status="PROVISIONAL", footprint="D_SMB", mech="smb_approx",
        notes="Clamps the PSU board total 5 V rail (J5/J6/J7) against HLK/cable transients. Cathode to +5V, anode to GND. The carrier has no TVS. Verify standoff/clamping and layout.",
        evidence="Littelfuse SMBJ series datasheet; exact batch to be verified."
    ),
    row(
        "E-052", "PSU_PCB", "PCB", "Mains-entry PSU PCB, 2-layer FR4, 1.6 mm, 2 oz Cu target, 50 x 65 mm, routed", "TBD", "PCB-PSU-REV-D",
        status="PROVISIONAL", footprint="PCB_PSU_REV_D", mech="pcb_psu_50x65",
        notes="REV_D_CORE_ONLY PSU board: TB1/TB2, F1, MOV1, TF1, HLK-5M05, F2/D1, 3x JST. Mains isolation notch; creepage/hipot unverified. NOT_FOR_FABRICATION.",
        evidence="KiCad psu_rev_d.kicad_pcb; Gerber/drill/POS provisional; DRC 0/0."
    ),
    row(
        "E-053", "J5,J6,J7", "Connectors", "JST-XH 2-pin PCB connector for 5 V outputs, 3 pcs", "JST", "B2B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B2B-XH-A", mech="jst_xh_2_approx",
        notes="Three keyed 5 V outputs: J5 carrier, J6 relay, J7 PZEM conditional. Verify 3 A rating and keying.",
        evidence="JST datasheet; exact batch to be verified."
    ),
    row(
        "E-054", "W5V1,W5V2,W5V3", "Connectors", "JST-XH 2-pin cable for 5 V outputs, 3 pcs, 0.2 m", "JST", "B2B-XH-A cable",
        status="PROVISIONAL", footprint="OFF_BOARD_CABLE", mech="jst_xh_2_cable",
        notes="Carrier, relay, PZEM. Color-code/label; do not swap outputs.",
        evidence="Estimated cable assembly."
    ),
    row(
        "E-055", "TB2", "Connectors", "Mains output terminal block, 2-pin, 5.08 mm, 17.5 A / 250 V, screw clamp", "Phoenix Contact", "MKDS 1,5/2-5,08",
        status="PROVISIONAL", alt="MKDS 3/2-5,08 (320 V, needs new footprint); Degson DG308-5.08-2P",
        footprint="TERMINAL_5.08_2P", mech="terminal_5.08_2p_approx",
        notes="PSU TB2 L/N output to relay/socket. 250 VAC < user's >=300 V target; upgrade path MKDS 3/2-5,08. Verify torque, 1.5 mm2 wire/ferrule, and creepage. Full 8 A passes through this block.",
        evidence="Phoenix MKDS 1,5 series: 5.08 mm, 17.5 A, 250 V; order code 1715721."
    ),
    row(
        "E-019", "C1", "Passives", "Bulk capacitor, 100 uF, 10 V, low ESR, 6.3x5.4 mm", "Nichicon", "UWT1A101MCL1GS",
        datasheet="https://www.nichicon.co.jp/english/products/pdfs/e-uwt.pdf", status="PROVISIONAL",
        footprint="CP_6.3x5.4", mech="cap_6.3_approx", notes="5 V rail decoupling near relay/PSU.", evidence="Nichicon datasheet."
    ),
    row(
        "E-020", "C2", "Passives", "Decoupling capacitor, 100 nF, 50 V, 0603", "Murata", "GRM188R71H104KA93D",
        datasheet="https://www.murata.com/", status="PROVISIONAL", footprint="C_0603_1608Metric", mech="C0603_approx",
        notes="Place at each IC supply pin.", evidence="Murata datasheet."
    ),
    row(
        "E-020A", "C3", "Passives", "Decoupling capacitor, 100 nF, 50 V, 0603, at 74HCT125 VCC", "Murata", "GRM188R71H104KA93D",
        datasheet="https://www.murata.com/", status="PROVISIONAL", footprint="C_0603_1608Metric", mech="C0603_approx",
        notes="Place within 5 mm of U9 VCC/GND. Required for clean 5V level-shift edges.", evidence="Murata datasheet."
    ),
    row(
        "E-018A", "R4", "Passives", "PZEM TX divider top resistor, 10 kohm, 1%, 0805", "Yageo", "RC0805FR-0710KL",
        datasheet="https://www.yageo.com/", status="PROVISIONAL", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="PZEM TX (5V) -> R4 -> ESP32 RX; R5 20k to GND gives ~3.33V. Verify PZEM TX high level.", evidence="Divider calculation; Yageo datasheet."
    ),
    row(
        "E-018B", "R5", "Passives", "PZEM TX divider bottom resistor, 20 kohm, 1%, 0805", "Yageo", "RC0805FR-0720KL",
        datasheet="https://www.yageo.com/", status="PROVISIONAL", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="Divider bottom; add 100 nF at ESP32 RX if noise is observed.", evidence="Divider calculation; Yageo datasheet."
    ),
    row(
        "E-018C", "R6", "Passives", "I2C SDA pullup, 4.7 kohm, 1%, 0805", "Yageo", "RC0805FR-074K7L",
        datasheet="https://www.yageo.com/", status="DEFERRED_CORE_ONLY", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="To 3.3V; OLED + RTC only. Verify bus capacitance and address conflicts.", evidence="Yageo datasheet."
    ),
    row(
        "E-018D", "R7", "Passives", "I2C SCL pullup, 4.7 kohm, 1%, 0805", "Yageo", "RC0805FR-074K7L",
        datasheet="https://www.yageo.com/", status="DEFERRED_CORE_ONLY", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="To 3.3V; keep I2C <=400 kHz for prototype.", evidence="Yageo datasheet."
    ),
    row(
        "E-018E", "R8", "Passives", "Button pullup, 10 kohm, 1%, 0805", "Yageo", "RC0805FR-0710KL",
        datasheet="https://www.yageo.com/", status="PROVISIONAL", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="Button to GND; external pullup in addition to MCU internal pullup.", evidence="Yageo datasheet."
    ),
    row(
        "E-021", "DS1", "UI", "OLED 0.96 inch, 128x64, SSD1306, I2C, 3.3 V module", "TBD", "OLED-096-SSD1306-I2C",
        status="DEFERRED_CORE_ONLY", alt="Deferred to FULL; not fitted in REV_D",
        footprint="OFF_BOARD_MODULE", mech="oled096_approx",
        notes="Verify controller, address, and 3.3 V operation. Do not assume SH1106 is SSD1306-compatible.",
        evidence="Generic module; no traceable manufacturer datasheet yet."
    ),
    row(
        "E-022", "LED1", "UI", "Addressable RGB LED, WS2812B, 5050, 5 V", "Worldsemi", "WS2812B-5050",
        datasheet="https://www.worldsemi.com/", status="DEFERRED_CORE_ONLY", footprint="LED_WS2812B_5050",
        mech="ws2812b_approx", notes="External panel indicator; built-in DevKitC-1 RGB may be hidden. Level shift data.",
        evidence="Worldsemi datasheet; exact bin/revision to be verified."
    ),
    row(
        "E-023", "SW1", "UI", "Tactile pushbutton, 6x6 mm, through-hole, panel cap", "Omron", "B3F-1000",
        datasheet="https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3f.pdf", status="PENDING_APPROVAL",
        footprint="SW_PUSH_6mm", mech="b3f_approx", notes="Debounce in firmware; long-press reset separated from short press. Button must remain reachable without mains access.",
        evidence="Omron B3F datasheet."
    ),
    row(
        "E-024", "J1A,J1B", "Connectors", "2 pcs 1x22 female header strips (one 2x22 strip split into two rows), 2.54 mm, 22.86 mm row spacing for DevKitC-1", "TBD", "HDR-1X22-2.54-F",
        status="PROVISIONAL", footprint="PinSocket_1x22_P2.54mm", mech="header_1x22_approx",
        notes="DevKitC-1 has two separate 1x22 headers (J1/J3), 22.86 mm apart. Do NOT use a 2x22 socket: its rows are only 2.54 mm apart and cannot accept the board. Mark pin 1 and USB end; key or block reverse insertion.",
        evidence="Espressif DevKitC-1 v1.1 user guide header tables."
    ),
    row(
        "E-025", "J2", "Connectors", "JST-XH 4-pin connector for PZEM TTL (5V, RX, TX, GND)", "JST", "B4B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B4B-XH-A", mech="jst_xh_4_approx",
        notes="PZEM TTL side is SELV via the module's internal optocouplers. Pin order must match the purchased V4 batch; never assume colors.",
        evidence="PZEM V4 pinout; verify batch."
    ),
    row(
        "E-026", "J3", "Connectors", "JST-XH 4-pin connector for relay module (5V, GND, IN1, IN2)", "JST", "B4B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B4B-XH-A", mech="jst_xh_4_approx",
        notes="Active-LOW module inputs; both driven by one AO3400. JD-VCC jumper on module. Keep coil current off the carrier ground return? Use short 5V/GND pair.",
        evidence="Relay module pinout; verify batch."
    ),
    row(
        "E-027", "J4", "Connectors", "JST-XH 4-pin connector for OLED (3.3V, GND, SDA, SCL)", "JST", "B4B-XH-A",
        status="DEFERRED_CORE_ONLY", footprint="JST_XH_B4B-XH-A", mech="jst_xh_4_approx", notes="Keyed low-voltage connector.",
        evidence="JST datasheet."
    ),
    row(
        "E-028", "J5", "Connectors", "JST-XH 6-pin connector for RTC (3.3V, GND, SDA, SCL, INT, 32K)", "JST", "B6B-XH-A",
        status="DEFERRED_CORE_ONLY", footprint="JST_XH_B6B-XH-A", mech="jst_xh_6_approx",
        notes="DS3231 module; 32K may be left unconnected. INT to GPIO7.", evidence="JST datasheet."
    ),
    row(
        "E-047", "J6", "Connectors", "JST-XH 2-pin connector for button (BUTTON, GND)", "JST", "B2B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B2B-XH-A", mech="jst_xh_2_approx",
        notes="Button to GND; 10k external pullup on carrier. Debounce in firmware.", evidence="JST datasheet."
    ),
    row(
        "E-048", "J7", "Connectors", "JST-XH 3-pin connector for RGB (5V, GND, DATA)", "JST", "B3B-XH-A",
        status="DEFERRED_CORE_ONLY", footprint="JST_XH_B3B-XH-A", mech="jst_xh_3_approx",
        notes="Data from 74HCT125 through 330R. 5V power for WS2812.", evidence="JST datasheet."
    ),
    row(
        "E-049", "J8", "Connectors", "JST-XH 2-pin connector for 5V input from HLK-5M05", "JST", "B2B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B2B-XH-A", mech="jst_xh_2_approx",
        notes="5V/GND from HLK. Add 100uF bulk and 100nF at carrier entry. Keep away from mains wiring.", evidence="JST datasheet."
    ),
    row(
        "E-029", "TB1", "Connectors", "Mains input terminal block, 2-pin, 5.08 mm, 17.5 A / 250 V, screw clamp", "Phoenix Contact", "MKDS 1,5/2-5,08",
        status="PROVISIONAL", alt="MKDS 3/2-5,08 (320 V, needs new footprint); Degson DG308-5.08-2P",
        footprint="TERMINAL_5.08_2P", mech="terminal_5.08_2p_approx",
        notes="PSU TB1 input L/N. 250 VAC rating meets 230 VAC nominal but is below the user's >=300 V target; conservative upgrade is MKDS 3/2-5,08 with a new footprint. 17.5 A > 10 A fuse. Verify torque, 1.5 mm2 wire/ferrule, and creepage.",
        evidence="Phoenix MKDS 1,5 series: 5.08 mm, 17.5 A, 250 V; order code 1715721 (MKDS 1,5/2-5,08)."
    ),
    row(
        "E-030", "TB_PE", "Connectors", "Protective earth terminal/stud, screw-clamp, tool-access", "TBD", "PE-TERMINAL-TBD",
        status="BLOCKED", footprint="PE_STUD_TBD", mech="pe_stud_approx",
        notes="PE must be continuous, not switched or fused. Dedicated mechanical bond with lock washer and test point. Exact part is safety-critical and not approved.",
        evidence="No approved part yet; engineer must select and verify."
    ),
    row(
        "E-034", "X1", "Connectors", "Type F (Schuko) panel socket, 16 A / 250 V, 2P+E", "TBD", "SOCKET-TYPE-F-16A-TBD",
        status="DOCUMENTATION_DEFICIENT", alt="Type E/F combo socket (Q02=B lean); other Indonesian standard",
        footprint="OFF_BOARD_MODULE", mech="type_f_socket_approx",
        notes="Product identity, certification, contact material, retention, and PE continuity are unverified. Do not use a universal socket without traceability. Q02 remains an analysis decision.",
        evidence="No approved MPN. Retailer photos are not a datasheet."
    ),
    row(
        "E-035", "P1", "Connectors", "Type F (Schuko) cord plug, 16 A / 250 V, 3-core", "TBD", "PLUG-TYPE-F-16A-TBD",
        status="DOCUMENTATION_DEFICIENT", alt="Type E/F compatible plug; local standard plug",
        footprint="OFF_BOARD_MODULE", mech="type_f_plug_approx",
        notes="Mating, cable clamp, PE contact, and orientation must be verified. Cable 3x1.5 mm2 H05VV-F provisional.",
        evidence="No approved MPN."
    ),
    row(
        "E-036", "CG1", "Mechanical", "Cable gland, M16, IP68, PA66, UL94 V-0", "TBD", "GLAND-M16-TBD",
        status="PROVISIONAL", footprint="OFF_BOARD", mech="gland_m16_approx",
        notes="Strain relief must anchor the cable to the enclosure, not the PCB. Verify thread and sealing.",
        evidence="Generic part; exact datasheet pending."
    ),
    row(
        "E-037", "ENC1", "Mechanical", "Enclosure, ABS/PC, 220 x 120 x 70 mm confirmed, flame-retardant grade", "TBD", "ENCLOSURE-220X120X70-TBD",
        status="BLOCKED", alt="Hammond 1555/1591 series; polycarbonate enclosure with UL94 V-0",
        footprint="OFF_BOARD", mech="enclosure_220x120x70_confirmed",
        notes="Confirmed 220x120x70 enclosure (Q06=C, 2026-11-15) because 150x100 and 180x120 fail clearance review with off-board PZEM + 2-channel relay. 3D printed enclosure is prototype-only and not certified for mains. Physical fit, material flammability, impact, thermal aging, and wall thickness must be validated.",
        evidence="No approved enclosure. CAD is parametric/provisional."
    ),
    row(
        "E-038", "PE1", "Mechanical", "PE bonding hardware: screw, lock washer, nut, dedicated stud", "TBD", "PE-HARDWARE-TBD",
        status="BLOCKED", footprint="OFF_BOARD", mech="pe_hardware_approx",
        notes="Must not be reused for other functions; verify continuity and vibration resistance. PE path must not rely on solder mask or anodized surfaces.",
        evidence="No approved part; safety-critical."
    ),
    row(
        "E-039", "W1", "Cable", "Mains cord, H05VV-F 3x1.5 mm2, 0.5 m provisional, brown/blue/green-yellow", "TBD", "H05VV-F-3G1.5",
        status="PROVISIONAL", unit="m", qty=0.5, footprint="OFF_BOARD", mech="cable_3g1.5_approx",
        notes="Length/current/derating to be calculated. Color is not proof of function; verify continuity and PE. Ferrules and strain relief required.",
        evidence="Cable standard reference; exact manufacturer not selected."
    ),
    row(
        "E-040", "W2", "Cable", "Low-voltage hookup wire assortment, 0.25 mm2, 300 V", "TBD", "HOOKUP-0.25MM2",
        status="PROVISIONAL", unit="m", qty=3, footprint="OFF_BOARD", mech="hv_wire_approx",
        notes="SELV only. Keep away from mains barrier.", evidence="Generic."
    ),
    row(
        "E-041", "PCB1", "PCB", "SELV CORE-only carrier PCB, 2-layer FR4, 1.6 mm, 1 oz Cu, 100 x 70 mm, routed (19 footprints incl. 3 fiducials, 11 named nets)", "TBD", "PCB-CARRIER-REV-D",
        status="PROVISIONAL", footprint="PCB_CARRIER_REV_D", mech="pcb_carrier_100x70",
        notes="Mains modules off-board. Carrier handles 5V/3.3V, PZEM 5V-to-3.3V level shift, relay driver, I2C OLED/RTC, button, RGB. Routed with DRC 0 but still engineering-review-required; not a certified mains assembly.",
        evidence="KiCad REV_D_CORE_ONLY routed carrier; Gerber/drill exported; physical test not performed."
    ),
    row(
        "E-042", "LAB1", "Labels", "Safety/rating label set: rated voltage/current, warnings, serial/QR placeholder", "TBD", "LABEL-SET-REV-A",
        status="BLOCKED", footprint="OFF_BOARD", mech="label_set_approx",
        notes="Rating must be derived from verified chain, not target. QR must not expose a reusable secret. Final label requires regulatory review.",
        evidence="No approved label content yet."
    ),
    row(
        "E-043", "HS1", "Consumables", "Heat-shrink tubing assortment, flame-retardant", "TBD", "HEATSHRINK-ASSORT",
        status="PROVISIONAL", unit="set", qty=1, footprint="OFF_BOARD", mech="consumable",
        notes="Mains joints require appropriate insulation and strain relief.", evidence="Generic."
    ),
    row(
        "E-044", "SC1", "Mechanical", "M3x8 machine screws, nylon washers", "TBD", "M3X8-SCREW",
        status="PROVISIONAL", qty=8, footprint="OFF_BOARD", mech="m3_screw",
        notes="Do not create conductive paths or reduce isolation distances.", evidence="Generic."
    ),
    row(
        "E-045", "INS1", "Mechanical", "M3 heat-set inserts for enclosure", "TBD", "M3-INSERT",
        status="PROVISIONAL", qty=4, footprint="OFF_BOARD", mech="m3_insert",
        notes="Insert depth and wall thickness must be verified in CAD.", evidence="Generic."
    ),
    row(
        "E-046", "ST1", "Mechanical", "M3 nylon standoff set for carrier PCB", "TBD", "M3-STANDOFF",
        status="PROVISIONAL", qty=4, footprint="OFF_BOARD", mech="m3_standoff",
        notes="Nylon avoids unintended conductive paths; verify thermal rating.", evidence="Generic."
    ),
]

# Tools are not part of the product BOM; they are listed separately.
TOOLS = [
    row("T-001", "LAB", "Test equipment", "True-RMS multimeter with CAT III rating appropriate to the measurement", "TBD", "DMM-CATIII-TBD", status="NOT_PURCHASED", notes="Q26=A: not owned. Physical verification BLOCKED.", evidence="User answer Q26."),
    row("T-002", "LAB", "Test equipment", "Isolated adjustable DC power supply, 0-30 V / 3 A", "TBD", "PSU-BENCH-TBD", status="NOT_PURCHASED", notes="For low-voltage bench tests only.", evidence="Q26."),
    row("T-003", "LAB", "Test equipment", "Low-voltage test fixture with relay/load simulator, fuses, and emergency stop", "TBD", "FIXTURE-LV-TBD", status="NOT_PURCHASED", notes="No mains. Must be built and reviewed before HIL.", evidence="PRD T-HW-014."),
    row("T-004", "LAB", "Test equipment", "USB power meter / current logger", "TBD", "USB-METER-TBD", status="NOT_PURCHASED", notes="For board current and boot behavior.", evidence="Q26."),
    row("T-005", "LAB", "Test equipment", "Thermocouple/k-type thermometer or calibrated temp logger", "TBD", "TEMP-LOGGER-TBD", status="NOT_PURCHASED", notes="Thermal tests require qualified lab.", evidence="Q26."),
    row("T-006", "LAB", "Test equipment", "Insulation resistance / hipot tester with qualified operator", "TBD", "HIPOT-TBD", status="NOT_PURCHASED", notes="Mains safety test; not for hobby use. BLOCKED.", evidence="PRD 27.3."),
]

CONSUMABLES = [
    row("C-001", "-", "Consumables", "Lead-free solder, SAC305, 0.5 mm", "TBD", "SOLDER-SAC305", status="PROVISIONAL", unit="roll", qty=1, notes="Low-voltage assembly only for beginners.", evidence="Generic."),
    row("C-002", "-", "Consumables", "No-clean flux pen", "TBD", "FLUX-PEN", status="PROVISIONAL", qty=1, notes="Clean residue per assembly procedure.", evidence="Generic."),
    row("C-003", "-", "Consumables", "Isopropyl alcohol 99% and lint-free swabs", "TBD", "IPA-99", status="PROVISIONAL", qty=1, notes="Flux cleaning and inspection.", evidence="Generic."),
    row("C-004", "-", "Consumables", "Ferrules and crimp tool for 1.5 mm2 and 0.25 mm2", "TBD", "FERRULE-KIT", status="PROVISIONAL", qty=1, notes="Proper crimp required; solder-only stranded wire is not acceptable for mains terminals.", evidence="Generic."),
    row("C-005", "-", "Consumables", "Kapton/polyimide tape and thermal pad", "TBD", "THERMAL-TAPE", status="PROVISIONAL", qty=1, notes="Do not rely on tape for insulation barriers.", evidence="Generic."),
]

# ---------------------------------------------------------------------------
# Indonesian prototype procurement matrix (dated 2026-11-15).
#
# This is deliberately separate from the engineering BOM. The engineering BOM
# names the preferred part; the procurement row names what can actually be
# bought in Indonesia today, at a dated listing price. A price is not an
# approval and a listing is not a datasheet.
# ---------------------------------------------------------------------------

PROCUREMENT = [
    {
        "line_id": "E-001", "stage": "CORE",
        "selected": "ESP32-S3 DevKitC-1 N16R8 compatible board, dual USB-C",
        "qty": 1, "unit_price": 139968,
        "seller": "Shopee / ALFA ELECTRONICS",
        "url": "https://shopee.co.id/product/18800073/40152181733",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Compatible N16R8 board, not confirmed official Espressif. This is an explicit deviation from Q08=B; official EasyWare listing is Rp103,500 but out of stock. Verify N16R8 marking, RGB GPIO (v1.0=48, v1.1=38), regulator, USB, and pinout before use.",
    },
    {
        "line_id": "E-002", "stage": "CORE",
        "selected": "PZEM-004T V4.0 100 A CT, closed CT, no casing",
        "qty": 1, "unit_price": 150000,
        "seller": "Shopee / ALFA ELECTRONICS",
        "url": "https://shopee.co.id/product/18800073/41719667847",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Closed CT is functionally non-invasive like split CT; only installation differs. EasyWare close-CT 100 A was Rp135,000 and open-CT Rp180,000, both out of stock. Verify V4 batch, CT ratio, UART levels, terminal rating, and voltage-input construction.",
    },
    {
        "line_id": "E-003", "stage": "CORE",
        "selected": "Hi-Link HLK-5M05, 5 V 1 A, 5 W",
        "qty": 1, "unit_price": 49000,
        "seller": "Shopee / Marnov Electronic",
        "url": "https://shopee.co.id/product/29614947/7316405255",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Datasheet efficiency is only ~70% at 220 V full load. Batch certificate, isolation, creepage, and counterfeit status are unverified. CNC Store Bandung Rp63,300 was out of stock. Reject unmarked modules and require ripple/thermal/hipot tests.",
    },
    {
        "line_id": "E-005", "stage": "DEFERRED",
        "selected": "DS3231SN RTC module with battery",
        "qty": 1, "unit_price": 49500,
        "seller": "EasyWare Store",
        "url": "https://store.easyware.id/produk/modul-rtc-ds3231-real-time-clock-i2c-eeprom-at24c32-jam-presisi-arduino-esp32-baterai-cadangan/",
        "stock": "IN_STOCK", "verification": "VERIFIED_STORE_PAGE",
        "notes": "Shopee clones start around Rp53,000. Battery holder, crystal, and charge circuit quality vary. RTC drift and backup runtime require test. Deferred in the CORE build; SNTP-only operation must block ON when time is invalid.",
    },
    {
        "line_id": "E-008", "stage": "CORE",
        "selected": "AO3400A SOT-23 N-channel MOSFET",
        "qty": 1, "unit_price": 1500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/57575514/14466280329",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Boot-safe low-side driver for active-LOW relay inputs. 100 kOhm pulldown and 1 kOhm gate resistor are mandatory. Verify pinout/marking.",
    },
    {
        "line_id": "E-009", "stage": "CORE",
        "selected": "SN74HCT125N quad buffer, DIP-14",
        "qty": 1, "unit_price": 8750,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/30000367/29506172697",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Level-shifts ESP32 3.3V TX to PZEM 5V RX and RGB data to 5V. DIP-14 for hand assembly; tie unused inputs to GND, add 100nF at VCC. PZEM RX is not 5V-tolerant, so the RX divider is mandatory.",
    },
    {
        "line_id": "E-010", "stage": "CORE",
        "selected": "2-channel 5 V optocoupler relay module, 10 A class",
        "qty": 1, "unit_price": 16650,
        "seller": "Shopee / AIFRobotic",
        "url": "https://shopee.co.id/product/214108565/5414791883",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Two independent SPDT channels, NOT mechanically linked. 10 A is a vendor claim; relay brand, batch, contact rating, and lifecycle are unverified. Final rating is 8 A only after thermal/lifecycle test. Verify active-LOW input and JD-VCC jumper.",
    },
    {
        "line_id": "E-010A", "stage": "CORE",
        "selected": "3D-printed relay bracket and standoffs, ABS/PC",
        "qty": 1, "unit_price": 5000,
        "seller": "In-house 3D print (filament + insert cost)",
        "url": "",
        "stock": "MADE", "verification": "ESTIMATED",
        "notes": "Cost estimate only; not a certified part. Printed-material flame rating is unverified. Retain the module mechanically and keep it in the mains zone behind a barrier.",
    },
    {
        "line_id": "E-010B", "stage": "CORE",
        "selected": "3D-printed PZEM bracket and standoffs, ABS/PC",
        "qty": 1, "unit_price": 5000,
        "seller": "In-house 3D print (filament + insert cost)",
        "url": "",
        "stock": "MADE", "verification": "ESTIMATED",
        "notes": "Cost estimate only; dimensions must be measured from the purchased PZEM batch. Keep PZEM in the mains zone, with CT and voltage terminals accessible only during service.",
    },
    {
        "line_id": "E-011", "stage": "CORE",
        "selected": "Littelfuse 5x20 mm 10 A 250 VAC slow-blow ceramic fuse",
        "qty": 1, "unit_price": 18300,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/88911101/12944617615",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Listing says Littelfuse slow-blow; verify exact MPN/marking and breaking capacity. A 10 A fuse is backup protection, not the only overcurrent protection. 8 A continuous coordination and time-current curve still require review.",
    },
    {
        "line_id": "E-012", "stage": "CORE",
        "selected": "PCB fuse clips for 5x20 mm, 2 pcs (estimated)",
        "qty": 2, "unit_price": 2500,
        "seller": "Shopee (estimated)", "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Matches the PSU board clip footprint. Not a closed holder; verify 10 A/250 V clip rating and retention. No dated listing; Schurter 0031.8201 is a closed-holder alternate but needs a footprint change.",
    },
    {
        "line_id": "E-013", "stage": "CORE",
        "selected": "MOV 10D271K, 275 VAC class, 10 mm",
        "qty": 1, "unit_price": 7500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/1400052865/45311419818",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Generic MOV; EPCOS S10K275 remains preferred. End-of-life failure mode and thermal-fuse coordination are unverified. This is not a complete surge-protection design.",
    },
    {
        "line_id": "E-014", "stage": "CORE",
        "selected": "TF thermal fuse 99 C, 10 A / 250 V",
        "qty": 1, "unit_price": 4995,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/15326449/25743012041",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Listing is a generic 99 C TCO, not confirmed SF96E. Verify the delivered marking/part is SEFUSE SF96E (marked 96 C, RFT 99 C, holding 84 C) or an equivalent with a datasheet. Reject SF169E (172 C). Must be clamped to the hottest terminal/HLK/PCB spot. One-shot and independent of firmware.",
    },
    {
        "line_id": "E-015", "stage": "CORE",
        "selected": "1N4007 diode, 10 pcs pack",
        "qty": 1, "unit_price": 3900,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/66424740/14150584885",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Flyback diode only if a discrete coil driver is used; the relay module may already include one. Verify before fitting.",
    },
    {
        "line_id": "E-016", "stage": "CORE",
        "selected": "1 kOhm 0805 resistor (small pack)",
        "qty": 1, "unit_price": 1000,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Gate series resistor. Unit price is an allocated pack cost.",
    },
    {
        "line_id": "E-017", "stage": "CORE",
        "selected": "100 kOhm 0805 resistor (small pack)",
        "qty": 1, "unit_price": 1000,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/44140220/4697369971",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Mandatory gate pulldown for boot-safe OFF. Unit price is an allocated pack cost.",
    },
    {
        "line_id": "E-018", "stage": "DEFERRED",
        "selected": "330 Ohm 0805 resistor (small pack)",
        "qty": 1, "unit_price": 1000,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "WS2812 series resistor; deferred with the external RGB option.",
    },
    {
        "line_id": "E-050", "stage": "CORE",
        "selected": "PTC resettable fuse 1.1 A, 1206 (estimated)",
        "qty": 1, "unit_price": 2000,
        "seller": "Shopee (estimated)", "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "5 V rail protection. Exact MPN/hold current to be verified; allocated estimate.",
    },
    {
        "line_id": "E-051", "stage": "CORE",
        "selected": "SMBJ5.0A TVS diode (estimated)",
        "qty": 1, "unit_price": 3000,
        "seller": "Shopee (estimated)", "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "5 V rail transient clamp. Exact marking/standoff to be verified; allocated estimate.",
    },
    {
        "line_id": "E-052", "stage": "CORE",
        "selected": "REV_D_CORE_ONLY PSU PCB 50 x 65 mm, 2 oz target (5 pcs share, estimated)",
        "qty": 1, "unit_price": 15000,
        "seller": "PCB fab (estimate)", "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Not a quote. 2 oz/creepage capability must be confirmed; not fabricated.",
    },
    {
        "line_id": "E-053", "stage": "CORE",
        "selected": "JST-XH 2-pin PCB connector, 3 pcs (estimated)",
        "qty": 3, "unit_price": 1500,
        "seller": "Shopee (estimated)", "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "5 V outputs J5/J6/J7; verify 3 A rating.",
    },
    {
        "line_id": "E-054", "stage": "CORE",
        "selected": "JST-XH 2-pin cable, 0.2 m, 3 pcs (estimated)",
        "qty": 3, "unit_price": 3000,
        "seller": "Shopee (estimated)", "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Carrier/relay/PZEM 5 V cables; label both ends.",
    },
    {
        "line_id": "E-055", "stage": "CORE",
        "selected": "5.08 mm 2-pin mains output terminal block",
        "qty": 1, "unit_price": 2450,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/27499686/47805816021",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Listing is a generic 5.08 mm terminal, not confirmed Phoenix. Verify MKDS 1,5/2-5,08 or equivalent, 17.5 A/250 V. 250 V is below the >=300 V target; engineer review or MKDS 3 upgrade. Full 8 A passes here.",
    },
    {
        "line_id": "E-019", "stage": "CORE",
        "selected": "100 uF 10 V electrolytic capacitor",
        "qty": 1, "unit_price": 350,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/783130973/57809969353",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "5 V bulk near relay/PSU. Verify low-ESR/ripple rating; generic part.",
    },
    {
        "line_id": "E-020", "stage": "CORE",
        "selected": "100 nF 50 V MLCC (small pack)",
        "qty": 1, "unit_price": 360,
        "seller": "EasyWare Store",
        "url": "https://store.easyware.id/produk/20-pcs-kapasitor-smd-0603-yageo-original-50v-np0-x7r-22pf-470pf-560pf-1nf-10nf-mlcc/",
        "stock": "IN_STOCK", "verification": "VERIFIED_STORE_PAGE",
        "notes": "Decoupling; allocated pack cost. Verify voltage rating and dielectric.",
    },
    {
        "line_id": "E-020A", "stage": "CORE",
        "selected": "100 nF 50 V MLCC at 74HCT125 (small pack)",
        "qty": 1, "unit_price": 360,
        "seller": "EasyWare Store",
        "url": "https://store.easyware.id/produk/20-pcs-kapasitor-smd-0603-yageo-original-50v-np0-x7r-22pf-470pf-560pf-1nf-10nf-mlcc/",
        "stock": "IN_STOCK", "verification": "VERIFIED_STORE_PAGE",
        "notes": "Allocated pack cost; place at U9 VCC/GND.",
    },
    {
        "line_id": "E-018A", "stage": "CORE",
        "selected": "10 kOhm 0805 resistor (divider top)",
        "qty": 1, "unit_price": 500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Allocated pack cost. PZEM TX divider top.",
    },
    {
        "line_id": "E-018B", "stage": "CORE",
        "selected": "20 kOhm 0805 resistor (divider bottom)",
        "qty": 1, "unit_price": 500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Allocated pack cost. PZEM TX divider bottom; output ~3.33V.",
    },
    {
        "line_id": "E-018C", "stage": "DEFERRED",
        "selected": "4.7 kOhm 0805 resistor (I2C SDA pullup)",
        "qty": 1, "unit_price": 500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Allocated pack cost.",
    },
    {
        "line_id": "E-018D", "stage": "DEFERRED",
        "selected": "4.7 kOhm 0805 resistor (I2C SCL pullup)",
        "qty": 1, "unit_price": 500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Allocated pack cost.",
    },
    {
        "line_id": "E-018E", "stage": "CORE",
        "selected": "10 kOhm 0805 resistor (button pullup)",
        "qty": 1, "unit_price": 500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/52086903/6035376903",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Allocated pack cost.",
    },
    {
        "line_id": "E-047", "stage": "CORE",
        "selected": "JST-XH 2-pin cable for button",
        "qty": 1, "unit_price": 5000,
        "seller": "Shopee (similar listing)",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Can be soldered directly; exact listing not captured.",
    },
    {
        "line_id": "E-048", "stage": "DEFERRED",
        "selected": "JST-XH 3-pin cable for RGB",
        "qty": 1, "unit_price": 5000,
        "seller": "Shopee (similar listing)",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Deferred with RGB; exact listing not captured.",
    },
    {
        "line_id": "E-049", "stage": "CORE",
        "selected": "JST-XH 2-pin cable for 5V input",
        "qty": 1, "unit_price": 5000,
        "seller": "Shopee (similar listing)",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Or direct solder to J8; exact listing not captured.",
    },
    {
        "line_id": "E-021", "stage": "DEFERRED",
        "selected": "OLED 0.96 inch 128x64 SSD1306 I2C",
        "qty": 1, "unit_price": 33300,
        "seller": "EasyWare Store",
        "url": "https://store.easyware.id/produk/oled-0-96-inch-128x64-ssd1306/",
        "stock": "IN_STOCK", "verification": "VERIFIED_STORE_PAGE",
        "notes": "Verify controller (SSD1306 vs SH1106), address, and 3.3 V operation. Deferred in the CORE build; the web UI/serial console remains the fallback.",
    },
    {
        "line_id": "E-022", "stage": "DEFERRED",
        "selected": "CJMCU-2812-8 WS2812B module",
        "qty": 1, "unit_price": 8500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/65450634/10815777005",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "External indicator; the DevKit onboard RGB can substitute at zero extra cost. Level shift is required if the external LED is used.",
    },
    {
        "line_id": "E-023", "stage": "CORE",
        "selected": "6x6x5 mm tactile switch, 10 pcs",
        "qty": 1, "unit_price": 7000,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/153780012/27155035831",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Panel cap/extension required. Debounce in firmware; long-press reset must remain reachable without mains access.",
    },
    {
        "line_id": "E-024", "stage": "CORE",
        "selected": "2x22 female header strip, split into two 1x22 rows",
        "qty": 1, "unit_price": 3250,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/1484861284/29479551658",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "DevKitC-1 has two 1x22 headers (J1/J3) 22.86 mm apart. Split the 2x22 strip into two rows or buy two 1x22 strips. Mark pin 1/USB end; prevent reverse insertion.",
    },
    {
        "line_id": "E-025", "stage": "CORE",
        "selected": "JST-XH 4-pin cable for PZEM TTL",
        "qty": 1, "unit_price": 12300,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/15316646/522424401",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "PZEM TTL connector; pin order must match the V4 batch. Can be soldered directly if the cable is not available.",
    },
    {
        "line_id": "E-026", "stage": "CORE",
        "selected": "JST-XH 4-pin cable for relay module",
        "qty": 1, "unit_price": 12300,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/15316646/522424401",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Relay module connector; 5V/GND/IN1/IN2. Verify module pinout.",
    },
    {
        "line_id": "E-027", "stage": "DEFERRED",
        "selected": "JST-XH 4-pin cable for OLED",
        "qty": 1, "unit_price": 12300,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/15316646/522424401",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "OLED connector; deferred with OLED.",
    },
    {
        "line_id": "E-028", "stage": "DEFERRED",
        "selected": "JST-XH 6-pin cable for RTC",
        "qty": 1, "unit_price": 8000,
        "seller": "Shopee (similar listing)",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "DS3231 connector; 32K may be left unconnected. No exact listing captured.",
    },
    {
        "line_id": "E-029", "stage": "CORE",
        "selected": "5.08 mm 2-pin PCB terminal block",
        "qty": 1, "unit_price": 2450,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/27499686/47805816021",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Listing is a generic 5.08 mm terminal, not confirmed Phoenix. Verify MKDS 1,5/2-5,08 or equivalent, 17.5 A/250 V. 250 V is below the >=300 V target; engineer review or MKDS 3 upgrade. Verify torque, ferrules, and creepage.",
    },
    {
        "line_id": "E-030", "stage": "CORE",
        "selected": "DIN-rail PE terminal block, 6 mm2",
        "qty": 1, "unit_price": 10250,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/1308489298/27474313332",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "PE must be continuous, not switched or fused. Dedicated mechanical bond, lock washer, and test point. Exact PE path remains BLOCKED for engineer review.",
    },
    {
        "line_id": "E-034", "stage": "CORE",
        "selected": "Simon Schuko panel socket, 16 A / 250 V",
        "qty": 1, "unit_price": 25026,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/1393930173/24138502361",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Brand Simon; exact model, certification, contact material, retention, and PE continuity are unverified. Live parts must be inaccessible. Q02 socket standard remains an analysis decision.",
    },
    {
        "line_id": "E-035", "stage": "CORE",
        "selected": "BOSS BP16 Schuko plug, 16 A",
        "qty": 1, "unit_price": 14044,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/37155877/41075654392",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Verify PE contact, cable clamp, 3x1.5 mm2 fit, and certification. 16 A class, but assembly quality is unverified.",
    },
    {
        "line_id": "E-036", "stage": "CORE",
        "selected": "M16 cable gland, IP68, PA66",
        "qty": 1, "unit_price": 2400,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/83275056/4659955289",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Strain relief must anchor the cable to the enclosure, not the PCB. Verify thread, seal, and flammability.",
    },
    {
        "line_id": "E-037", "stage": "CORE",
        "selected": "MG Duradus 220x120x70 ABS junction box, IP65",
        "qty": 1, "unit_price": 99684,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/115758056/5491049261",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Exact confirmed size, ABS/IP65. Flame-retardant grade is not verified; ABS may not be UL94 V-0. Enclosure remains BLOCKED pending material, fit, thermal, impact, and PE review.",
    },
    {
        "line_id": "E-038", "stage": "CORE",
        "selected": "PE stud/screw/lock washer/nut kit (estimated)",
        "qty": 1, "unit_price": 5000,
        "seller": "Local hardware",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Dedicated PE bond; do not rely on solder mask or anodized surfaces. Engineer must approve the exact stack.",
    },
    {
        "line_id": "E-039", "stage": "CORE",
        "selected": "NYYHY 3x1.5 mm2 flexible cable, 0.5 m",
        "qty": 0.5, "unit_price": 29000,
        "seller": "Blibli / Supreme",
        "url": "https://www.blibli.com/p/kabel-listrik-serabut-nyyhy-3x1-5-supreme-meteran/is--GUL-70047-00870-00001",
        "stock": "IN_STOCK", "verification": "VERIFIED_STORE_PAGE",
        "notes": "NYYHY 3x1.5 flexible cable, not H05VV-F. 8 A / 0.5 m is provisional. Verify conductor size, PE continuity, ferrules, and bend radius.",
    },
    {
        "line_id": "E-040", "stage": "CORE",
        "selected": "0.25 mm2 hookup wire assortment, 3 m",
        "qty": 1, "unit_price": 5000,
        "seller": "Local/Shopee",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "SELV only. Keep away from the mains barrier.",
    },
    {
        "line_id": "E-041", "stage": "CORE",
        "selected": "100 x 70 mm routed 2-layer carrier PCB (5 pcs batch share)",
        "qty": 1, "unit_price": 15000,
        "seller": "PCB fab (JLCPCB/PCBWay/local, estimate)",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Estimated per-board share for 5 pcs plus shipping; not a quote. Gerber/drill generated locally, but fabrication and electrical test not performed.",
    },
    {
        "line_id": "E-042", "stage": "CORE",
        "selected": "Label tape / printed safety labels (estimated)",
        "qty": 1, "unit_price": 2000,
        "seller": "Local/stationery",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Rating/warning content is not approved. Do not print CE/SNI/UL marks. Use 'PROTOTYPE - NOT FOR USE' and the verified rating only after tests.",
    },
    {
        "line_id": "E-043", "stage": "CORE",
        "selected": "Heat-shrink tubing 5 mm, 2 m",
        "qty": 1, "unit_price": 5000,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/50487634/7301288986",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Flame-retardant grade unverified. Mains joints require insulation and strain relief.",
    },
    {
        "line_id": "E-044", "stage": "CORE",
        "selected": "M3x8 screws, 10 pcs",
        "qty": 1, "unit_price": 2300,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/351001905/9007630331",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Use nylon washers; do not create conductive paths or reduce isolation distances.",
    },
    {
        "line_id": "E-045", "stage": "CORE",
        "selected": "M3 heat-set inserts, 10 pcs (estimated)",
        "qty": 1, "unit_price": 5000,
        "seller": "Shopee/local",
        "url": "",
        "stock": "ESTIMATED", "verification": "ESTIMATED",
        "notes": "Insert depth and wall thickness must be verified in the purchased enclosure.",
    },
    {
        "line_id": "E-046", "stage": "CORE",
        "selected": "M3 nylon standoff, 12 mm, 10 pcs",
        "qty": 1, "unit_price": 7500,
        "seller": "Shopee",
        "url": "https://shopee.co.id/product/46014019/1449079299",
        "stock": "LISTED", "verification": "VERIFIED_AGGREGATOR",
        "notes": "Nylon avoids unintended conductive paths; verify thermal rating.",
    },
]

CORE_RESTOCK_SAVINGS = {
    "E-001": 139968 - 103500,
    "E-002": 150000 - 135000,
}
SHIPPING_ESTIMATE_IDR = 40000
BUDGET_CAP_IDR = 750000
MECH_ADDENDUM_IDR = 28000

# Selected prototype/procurement variant overrides. These keep the engineering
# BOM aligned with what is actually being bought, without pretending that a
# listing price is an approval.
PROCUREMENT_OVERRIDES = {
    "E-001": {
        "description": "ESP32-S3 DevKitC-1, N16R8 (official preferred; compatible board allowed only as a documented deviation)",
        "manufacturer": "Espressif / documented compatible",
        "alternative_mpn": "Official Espressif ESP32-S3-DevKitC-1-N16R8 (preferred); N8R8",
        "notes": "Q08=B remains the official ESP32-S3-DevKitC-1 N16R8 baseline. Official local stock is unconfirmed; the priced prototype board is a compatible N16R8 at Rp139,968. This is an explicit, not silent, deviation. Verify N16R8 marking, RGB GPIO (v1.0=48, v1.1=38), regulator, USB, and pinout.",
    },
    "E-002": {
        "description": "PZEM-004T V4 AC energy meter, 100 A CT (closed or split), TTL/Modbus",
        "manufacturer_part_number": "PZEM-004T-V4-100A-CT",
        "notes": "Off-board module. The priced prototype uses a closed 100 A CT; a split CT is electrically equivalent for non-invasive sensing and easier to install. Official Peacefair V4 datasheet for the exact batch is not verified. UART level, isolation, terminal rating, and CT ratio must be measured. Do not confuse CT rating with output current rating.",
    },
    "E-010": {
        "manufacturer": "Generic module (Songle-class relay)",
        "notes": "User-selected common 2-channel module, off-board. Two independent SPDT channels (L/N), NOT mechanically linked DPST. 10 A is a vendor claim, not a validated continuous rating. Final 8 A/1840 W. Active-LOW input; verify JD-VCC/pinout. Priced module is a generic optocoupler board; relay brand/batch/rating/lifecycle are unverified.",
    },
    "E-021": {
        "manufacturer": "Generic (SSD1306)",
        "notes": "Priced EasyWare module is 0.96 inch 128x64 SSD1306 I2C. Verify controller, address, and 3.3 V operation. Do not assume SH1106 is SSD1306-compatible. Deferred in the CORE build.",
    },
    "E-034": {
        "manufacturer": "Simon",
        "manufacturer_part_number": "SIMON-SCHUKO-16A",
        "approved_status": "DOCUMENTATION_DEFICIENT",
        "notes": "Priced Simon Schuko panel socket, 16 A/250 V. Exact model, certification, contact material, retention, and PE continuity are unverified. Live parts must be inaccessible. Q02 socket standard remains an analysis decision.",
    },
    "E-035": {
        "manufacturer": "BOSS",
        "manufacturer_part_number": "BP16",
        "approved_status": "DOCUMENTATION_DEFICIENT",
        "notes": "Priced BOSS BP16 Schuko plug, 16 A. Verify PE contact, cable clamp, 3x1.5 mm2 fit, and certification. Assembly quality is unverified.",
    },
    "E-037": {
        "manufacturer": "MG Duradus",
        "manufacturer_part_number": "MG-220X120X70-ABS",
        "notes": "Priced exact-size 220x120x70 ABS/IP65 junction box. Flame-retardant grade is not verified; ABS may not be UL94 V-0. Enclosure remains BLOCKED pending material, fit, thermal, impact, and PE review. 3D printed enclosure is prototype-only and not certified for mains.",
    },
    "E-041": {
        "description": "SELV CORE-only carrier PCB, 2-layer FR4, 1.6 mm, 1 oz Cu, 100 x 70 mm, routed (19 footprints incl. 3 fiducials, 11 named nets)",
        "manufacturer": "Generic",
        "manufacturer_part_number": "PCB-CARRIER-REV-D",
        "footprint_id": "PCB_CARRIER_REV_D",
        "notes": "REV_D_CORE_ONLY routed SELV carrier with two 1x22 DevKit sockets at 22.86 mm spacing, PZEM 5V/3.3V level shift, relay driver, button, and 5V input from PSU J5. No mains, no OLED/RTC/external RGB, no PTC/TVS. DRC 0 but engineering review/physical test still required.",
    },
    "E-042": {
        "description": "Safety/rating label set: rated voltage/current, warnings, serial/QR placeholder (prototype label tape)",
        "notes": "Rating must be derived from a verified chain, not the target. Do not print CE/SNI/UL marks. Use 'PROTOTYPE - NOT FOR USE'. QR must not expose a reusable secret. Final label requires regulatory review.",
    },
    "E-043": {
        "manufacturer": "Generic",
        "manufacturer_part_number": "HEATSHRINK-5MM",
    },
    "E-044": {
        "manufacturer": "Generic",
        "manufacturer_part_number": "M3X8-SCREW",
    },
    "E-045": {
        "manufacturer": "Generic",
        "manufacturer_part_number": "M3-INSERT",
    },
    "E-046": {
        "manufacturer": "Generic",
        "manufacturer_part_number": "M3-STANDOFF-12-NYLON",
    },
}

for _item in ROWS:
    if _item["item_id"] in PROCUREMENT_OVERRIDES:
        _item.update(PROCUREMENT_OVERRIDES[_item["item_id"]])


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def procurement_rows() -> list[dict]:
    """Join the dated procurement matrix to the engineering BOM rows."""
    by_id = {item["item_id"]: item for item in ROWS}
    rows = []
    for entry in PROCUREMENT:
        if entry.get("stage") == "DEFERRED":
            continue
        item = by_id.get(entry["line_id"])
        if item is None:
            raise KeyError(f"procurement row {entry['line_id']} has no BOM row")
        extended = round(float(entry["qty"]) * float(entry["unit_price"]))
        rows.append(
            {
                "line_id": entry["line_id"],
                "stage": entry["stage"],
                "reference_designators": item["reference_designators"],
                "category": item["category"],
                "item": item["description"],
                "selected_part": entry["selected"],
                "qty": entry["qty"],
                "unit": item["unit"],
                "unit_price_idr": entry["unit_price"],
                "extended_idr": extended,
                "seller": entry["seller"],
                "source_url": entry["url"],
                "price_date": "2026-11-15",
                "stock_status": entry["stock"],
                "price_verification": entry["verification"],
                "safety_status": item["approved_status"],
                "notes": entry["notes"],
            }
        )
    return rows


def procurement_markdown(rows: list[dict], totals: dict) -> str:
    lines = [
        "# BOM Procurement — Indonesia (2026-11-16)",
        "",
        "> **Harga listing, bukan kutipan resmi.** Ini adalah daftar belanja prototipe, bukan persetujuan komponen.",
        "> Harga dapat berubah; stok marketplace tidak stabil. Tidak ada harga rekaan: baris tanpa listing ditandai `ESTIMATED`.",
        "",
        f"- Budget cap: **Rp{BUDGET_CAP_IDR:,}**",
        f"- Baris: **{sum(1 for r in rows if r['stage']=='CORE')} CORE; FULL deferred**; "
        f"{sum(1 for r in rows if r['price_verification'].startswith('VERIFIED'))} listing-verified, "
        f"{sum(1 for r in rows if r['price_verification']=='ESTIMATED')} `ESTIMATED`.",
        f"- CORE subtotal: **Rp{totals['core_subtotal_idr']:,}**",
        f"- CORE dengan harga restock EasyWare: **Rp{totals['core_restock_subtotal_idr']:,}**",
        f"- FULL add-ons: DEFERRED (CORE-only build)",
        f"- FULL subtotal: DEFERRED",
        f"- Estimasi ongkir: **Rp{totals['shipping_estimate_idr']:,}** (belum termasuk pajak/impor)",
        "",
        "## CORE — safety/function minimum",
        "",
        "| Line | Part | Qty | Harga | Seller | Verifikasi |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in rows:
        if row["stage"] != "CORE":
            continue
        lines.append(
            f"| {row['line_id']} | {row['selected_part']} | {row['qty']:g} {row['unit']} | "
            f"Rp{row['extended_idr']:,} | {row['seller']} | {row['price_verification']} |"
        )
    lines += [
        "",
        "## FULL add-ons — DEFERRED in REV_D_CORE_ONLY",
        "",
        "| Line | Part | Qty | Harga | Seller | Verifikasi |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in rows:
        if row["stage"] != "FULL":
            continue
        lines.append(
            f"| {row['line_id']} | {row['selected_part']} | {row['qty']:g} {row['unit']} | "
            f"Rp{row['extended_idr']:,} | {row['seller']} | {row['price_verification']} |"
        )
    lines += [
        "",
        "## Budget verdict",
        "",
        f"- CORE + ongkir: **Rp{totals['core_all_in_idr']:,}**.",
        f"- CORE restock + ongkir: **Rp{totals['core_restock_all_in_idr']:,}**.",
        f"- FULL + ongkir: **Rp{totals['full_all_in_idr']:,}**.",
        f"- Mechanical addendum (gasket/vent/printed cover-key/PSU bracket/thermal pad): **Rp{totals['mechanical_addendum_estimate_idr']:,}** estimated, not in line items.",
        f"- CORE + addendum + ongkir: **Rp{totals['core_with_addendum_all_in_idr']:,}**.",
        f"- CORE restock + addendum + ongkir: **Rp{totals['core_restock_with_addendum_all_in_idr']:,}**.",
        f"- FULL + addendum + ongkir: **Rp{totals['full_with_addendum_all_in_idr']:,}**.",
        f"- Status: `{totals['verdict']}`.",
        "",
        "CORE electronics (Rp716.087) is about Rp6.087 over Rp750.000 with Rp40.000 shipping (Rp756.087).",
        "The mechanical addendum (~Rp28.000) pushes the marketplace CORE to about Rp784.087 all-in;",
        "EasyWare restock brings it to about Rp732.619 all-in, under the cap. FULL UI is deferred.",
        "",
        "Jangan menurunkan fuse, MOV, TCO, terminal, PE, enclosure, atau barrier isolasi",
        "untuk mengejar budget. Lihat `research/PROCUREMENT_INDONESIA.md` untuk risiko stok.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    write_csv(BOM / "BOM_MASTER.csv", ROWS)
    write_csv(BOM / "BOM_ELECTRICAL.csv", [r for r in ROWS if r["category"] not in {"Mechanical", "Cable", "Labels", "Consumables", "PCB"}])
    write_csv(BOM / "BOM_MECHANICAL.csv", [r for r in ROWS if r["category"] in {"Mechanical", "Cable", "Labels"}])
    write_csv(BOM / "BOM_TOOLS_AND_TEST.csv", TOOLS)
    write_csv(BOM / "BOM_CONSUMABLES.csv", CONSUMABLES)

    proc = procurement_rows()
    proc_fields = [
        "line_id", "stage", "reference_designators", "category", "item", "selected_part",
        "qty", "unit", "unit_price_idr", "extended_idr", "seller", "source_url",
        "price_date", "stock_status", "price_verification", "safety_status", "notes",
    ]
    with (BOM / "BOM_PROCUREMENT.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=proc_fields)
        writer.writeheader()
        writer.writerows(proc)

    core_subtotal = sum(r["extended_idr"] for r in proc if r["stage"] == "CORE")
    full_addons = sum(r["extended_idr"] for r in proc if r["stage"] == "FULL")
    core_restock = core_subtotal - sum(CORE_RESTOCK_SAVINGS.values())
    totals = {
        "core_subtotal_idr": core_subtotal,
        "core_restock_subtotal_idr": core_restock,
        "full_addons_idr": full_addons,
        "full_subtotal_idr": core_subtotal + full_addons,
        "shipping_estimate_idr": SHIPPING_ESTIMATE_IDR,
        "core_all_in_idr": core_subtotal + SHIPPING_ESTIMATE_IDR,
        "core_restock_all_in_idr": core_restock + SHIPPING_ESTIMATE_IDR,
        "full_all_in_idr": core_subtotal + full_addons + SHIPPING_ESTIMATE_IDR,
        "mechanical_addendum_estimate_idr": MECH_ADDENDUM_IDR,
        "core_with_addendum_all_in_idr": core_subtotal + SHIPPING_ESTIMATE_IDR + MECH_ADDENDUM_IDR,
        "core_restock_with_addendum_all_in_idr": core_restock + SHIPPING_ESTIMATE_IDR + MECH_ADDENDUM_IDR,
        "full_with_addendum_all_in_idr": core_subtotal + full_addons + SHIPPING_ESTIMATE_IDR + MECH_ADDENDUM_IDR,
        "verdict": "CORE_OVER_750K_MARKETPLACE; RESTOCK_WITH_MECH_FITS; FULL_DEFERRED",
    }
    (BOM / "BOM_PROCUREMENT.md").write_text(procurement_markdown(proc, totals), encoding="utf-8")

    with (BOM / "BOM_MASTER.yaml").open("w", encoding="utf-8") as handle:
        import yaml
        yaml.safe_dump({"project": "esp32-s3-iot-smart-plug", "design_revision": "REV_D_CORE_ONLY", "generated_at": now, "items": ROWS}, handle, sort_keys=False, allow_unicode=True)

    summary = {
        "project": "esp32-s3-iot-smart-plug",
        "design_revision": "REV_D_CORE_ONLY",
        "currency": "IDR",
        "generated_at": now,
        "pricing_status": "PROCUREMENT_PRICED_2026-11-16",
        "design_bom_pricing_status": "UNPRICED",
        "procurement_matrix": "bom/BOM_PROCUREMENT.csv",
        "procurement_report": "research/PROCUREMENT_INDONESIA.md",
        "procurement_lines": len(proc),
        "procurement_verified_lines": sum(1 for r in proc if r["price_verification"].startswith("VERIFIED")),
        "procurement_estimated_lines": sum(1 for r in proc if r["price_verification"] == "ESTIMATED"),
        "subtotal_idr": None,
        "prototype_1_unit": {
            "core_subtotal_idr": core_subtotal,
            "core_restock_subtotal_idr": core_restock,
            "full_addons_idr": full_addons,
            "full_subtotal_idr": core_subtotal + full_addons,
            "core_all_in_idr": core_subtotal + SHIPPING_ESTIMATE_IDR,
            "core_restock_all_in_idr": core_restock + SHIPPING_ESTIMATE_IDR,
            "full_all_in_idr": core_subtotal + full_addons + SHIPPING_ESTIMATE_IDR,
            "mechanical_addendum_estimate_idr": MECH_ADDENDUM_IDR,
            "core_with_addendum_all_in_idr": core_subtotal + SHIPPING_ESTIMATE_IDR + MECH_ADDENDUM_IDR,
            "core_restock_with_addendum_all_in_idr": core_restock + SHIPPING_ESTIMATE_IDR + MECH_ADDENDUM_IDR,
            "full_with_addendum_all_in_idr": core_subtotal + full_addons + SHIPPING_ESTIMATE_IDR + MECH_ADDENDUM_IDR,
            "status": totals["verdict"],
        },
        "budget_cap_idr": BUDGET_CAP_IDR,
        "shipping_estimate_idr": SHIPPING_ESTIMATE_IDR,
        "batch_10_units": {"subtotal_idr": None, "status": "NOT_QUOTED"},
        "owned_components": {"market_cost_idr": None, "cash_out_cost_idr": None, "note": "Q28=B: none owned."},
        "notes": [
            "Engineering BOM is still unpriced; dated prototype buy list is bom/BOM_PROCUREMENT.csv.",
            "Prices are listing prices, not supplier quotes. Shipping/tax are separate estimates.",
            "REV_D is CORE-only. OLED, RTC, external RGB, their connectors, 330R, and I2C pullups are DEFERRED and excluded from procurement.",
            "CORE electronics is Rp716.087 (Rp756.087 all-in) at marketplace prices; the mechanical addendum (~Rp28.000) makes it about Rp784.087 all-in. EasyWare restock gives about Rp732.619 all-in with the addendum, under the cap. FULL UI is deferred in REV_D. Do not downgrade safety.",
            "FULL UI/time add-ons are deferred; do not downgrade fuse, MOV, TCO, PE, terminal, enclosure, or isolation to meet budget.",
            "Final rating is 8 A / about 1.840 W (user amendment), limited to electronics/SMPS loads; thermal/lifecycle tests are still required.",
            "Batch 10-unit pricing cannot be quoted without actual supplier quotes.",
        ],
    }
    (BOM / "BOM_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# BOM Master — REV_D_CORE_ONLY",
        "",
        f"**Generated:** {now}",
        "",
        "> **DESIGN BOM (UNPRICED) / NOT APPROVED.** Ini adalah BOM rekayasa, bukan daftar belanja.",
        "> Harga, stok, dan tautan pembelian ada di `BOM_PROCUREMENT.md` / `BOM_PROCUREMENT.csv`.",
        "> Status safety-critical: lihat `COMPONENT_APPROVALS.yaml`.",
        "",
        "| Item | Ref | Category | Description | MPN | Qty | Status |",
        "|---|---|---|---|---|---:|---|",
    ]
    for item in ROWS:
        md.append(
            f"| {item['item_id']} | {item['reference_designators']} | {item['category']} | {item['description']} | {item['manufacturer_part_number']} | {item['qty_per_unit']:g} {item['unit']} | {item['approved_status']} |"
        )
    md += [
        "",
        "## Catatan",
        "",
        "- BOM ini tidak memuat harga; daftar belanja bertanggal ada di `BOM_PROCUREMENT.md`.",
        "- Komponen mains (socket, plug, relay, fuse, PSU, PE, enclosure) belum disetujui.",
        "- `qty_per_unit` adalah kebutuhan prototipe 1 unit; batch 10 unit belum dihitung.",
        "- Lihat `research/COMPONENT_RESEARCH.md`, `research/PROCUREMENT_INDONESIA.md`, `research/UNKNOWN_SPECIFICATIONS.md`, dan `bom/COMPONENT_APPROVALS.yaml`.",
    ]
    (BOM / "BOM_MASTER.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    approvals = {
        "project": "esp32-s3-iot-smart-plug",
        "design_revision": "REV_D_CORE_ONLY",
        "generated_at": now,
        "approval_policy": "User approved the research direction, not final MPNs. No component is approved for fabrication.",
        "approved_by": None,
        "safety_reviewer": None,
        "items": [
            {
                "item_id": item["item_id"],
                "mpn": item["manufacturer_part_number"],
                "status": item["approved_status"],
                "approved_for_purchase": False,
                "approved_for_fabrication": False,
                "blocking_reason": item["notes"][:240]
            }
            for item in ROWS
        ]
    }
    (BOM / "COMPONENT_APPROVALS.yaml").write_text(
        __import__("yaml").safe_dump(approvals, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    links = [
        {"item_id": item["item_id"], "type": "datasheet", "url": item["datasheet_url"], "status": "UNVERIFIED" if item["datasheet_url"] else "MISSING"}
        for item in ROWS if item["datasheet_url"]
    ]
    links += [
        {"item_id": r["line_id"], "type": "purchase", "url": r["source_url"], "status": r["price_verification"]}
        for r in proc if r["source_url"]
    ]
    with (BOM / "PROCUREMENT_LINKS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item_id", "type", "url", "status"])
        writer.writeheader()
        writer.writerows(links)

    print(f"Wrote {len(ROWS)} master rows, {len(TOOLS)} tools, {len(CONSUMABLES)} consumables.")
    print(f"Procurement: {len(proc)} lines; CORE Rp{core_subtotal:,}; FULL add-ons Rp{full_addons:,}; verdict {totals['verdict']}.")


if __name__ == "__main__":
    main()
