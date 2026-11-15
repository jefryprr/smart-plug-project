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
        "E-001", "U1", "MCU", "ESP32-S3 DevKitC-1, N16R8 (16 MB flash, 8 MB PSRAM)",
        "Espressif", "ESP32-S3-DevKitC-1-N16R8", revision="v1.1 (planned)",
        datasheet="https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html",
        status="PENDING_APPROVAL", alt="ESP32-S3-DevKitC-1-N8R8; third-party clone (not preferred)",
        footprint="ESP32-S3-DevKitC-1_2x20_P2.54", mech="esp32s3_devkitc1_approx",
        notes="RGB pin differs between v1.0 (GPIO48) and v1.1 (GPIO38); board must be photographed and revision verified. N16R8 uses octal PSRAM; avoid GPIO33-37.",
        evidence="Espressif user guide v1.1; verify exact board marking and USB/strapping pins on arrival."
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
        "E-003", "U3", "Power", "AC/DC 5 V 1 A isolated power module, 90-264 VAC input",
        "Mean Well", "IRM-05-5", datasheet="https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.PDF",
        status="PENDING_APPROVAL", alt="Recom RAC01-05SC; Hi-Link HLK-PM01 (documentation deficient)",
        footprint="OFF_BOARD_MODULE", mech="irm05_approx",
        notes="Isolation withstand, leakage, no-load, thermal derating, and creepage must be reviewed in the final assembly. Fuse and MOV belong upstream.",
        evidence="Mean Well IRM-05 series datasheet; exact revision to be recorded at purchase."
    ),
    row(
        "E-004", "U4", "Sensing", "Digital temperature sensor, I2C, 3.3 V, SOT-563",
        "Texas Instruments", "TMP102AIDRLR",
        datasheet="https://www.ti.com/lit/ds/symlink/tmp102.pdf",
        status="PENDING_APPROVAL", alt="MCP9808; DS18B20 (remote probe)",
        footprint="SOT-563-6", mech="TMP102_approx",
        notes="Place near relay/terminal hotspot. Sensor failure must produce invalid state, not a stale comfortable reading.",
        evidence="TI TMP102 datasheet; accuracy and thermal response to be verified on bench."
    ),
    row(
        "E-005", "U5", "Sensing", "I2C real-time clock with integrated crystal, 3.3 V",
        "Analog Devices", "DS3231MZ+", datasheet="https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231M.pdf",
        status="PENDING_APPROVAL", alt="PCF8523T + 32.768 kHz crystal; SNTP holdover only",
        footprint="SO-16W", mech="DS3231_approx",
        notes="Battery/supercap holder and drift budget must be selected. Invalid clock blocks automatic ON.",
        evidence="Analog Devices DS3231M datasheet; RTC drift and backup runtime require measurement."
    ),
    row(
        "E-006", "U6", "Isolation", "Dual-channel digital isolator for PZEM UART (2.5 kVrms class)",
        "Analog Devices", "ADuM1201ARZ", datasheet="https://www.analog.com/media/en/technical-documentation/data-sheets/ADuM1200_1201.pdf",
        status="PENDING_APPROVAL", alt="Si8622; optocoupler pair (slower, more space)",
        footprint="SOIC-8", mech="ADuM1201_approx",
        notes="Mandatory provisional barrier between PZEM-side UART and SELV MCU. Final working voltage/creepage must be reviewed. Do not connect PZEM GND directly to MCU GND.",
        evidence="ADI ADuM1201 datasheet; isolation rating is component-level, not final assembly proof."
    ),
    row(
        "E-007", "U7", "Isolation", "Isolated 5 V to 5 V DC/DC converter, 1 W, for PZEM barrier",
        "Mornsun", "B0505S-1WR3", datasheet="https://www.mornsun-power.com/html/pdf/B0505S-1WR3.html",
        status="PENDING_APPROVAL", alt="RECOM R1SE-0505; Traco TMR 1-0511",
        footprint="SIP-4", mech="B0505S_approx",
        notes="Provides isolated 5 V to the PZEM side. Output filtering and common-mode path must be reviewed.",
        evidence="Mornsun datasheet; exact revision to be recorded."
    ),
    row(
        "E-008", "U8", "Switching", "N-channel MOSFET relay driver, logic-level, SOT-23",
        "Alpha & Omega Semiconductor", "AO3400A", datasheet="https://www.aosmd.com/res/data_sheets/AO3400A.pdf",
        status="PENDING_APPROVAL", alt="2N7002 (lower current); ULN2003 (module driver)",
        footprint="SOT-23", mech="AO3400_approx",
        notes="Low-side switch pulls both active-LOW module inputs down. Gate pulldown 100k and series 1k are mandatory for boot-safe OFF. No carrier flyback diode: the module has its own coil drivers. Verify total input current (~15-20 mA per channel), thermal, and module pinout.",
        evidence="AOS datasheet; boot waveform must be measured on a low-voltage fixture."
    ),
    row(
        "E-009", "U9", "UI", "Single buffer/level shifter for 3.3 V to 5 V WS2812 data",
        "Texas Instruments", "SN74AHCT1G125DBVR", datasheet="https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf",
        status="PENDING_APPROVAL", alt="74HCT125; power WS2812 at 3.3 V if proven",
        footprint="SOT-23-5", mech="SOT23_5_approx",
        notes="WS2812B high-level threshold at 5 V may exceed 3.3 V logic. Level shift and 330 ohm series resistor.",
        evidence="TI datasheet; verify LED timing and supply decoupling."
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
        "E-012", "FH1", "Protection", "PCB fuse holder, 5x20 mm, 10 A / 250 VAC",
        "Schurter", "0031.8201", datasheet="https://www.schurter.com/en/datasheet/0031.8201",
        status="PENDING_APPROVAL", alt="Littelfuse 03455LF2H; panel holder with touch protection",
        footprint="SCHURTER_0031_8201", mech="fuse_holder_approx",
        notes="Touch-proof, tool-access, and service procedure required. Fuse holder must not be accessible during normal use.",
        evidence="Schurter product page; verify voltage/current ratings and cover."
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
        "E-014", "TF1", "Protection", "One-shot thermal cutoff, 99 C, 10 A / 250 VAC",
        "Sefuse", "SF169E", datasheet="https://www.sefuse.com/",
        status="DOCUMENTATION_DEFICIENT", alt="Therm-O-Disc one-shot TCO; thermostat KSD301 (auto-reset, not preferred)",
        footprint="TCO_AXIAL", mech="tco_approx",
        notes="Must be mechanically clamped to the hottest terminal/relay area and be independent of firmware. Exact trip temperature, holding current, and approval must be verified. A resettable thermostat is not equivalent.",
        evidence="Vendor site only; manufacturer datasheet for exact batch not yet verified."
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
        datasheet="https://www.yageo.com/", status="PROVISIONAL", footprint="R_0805_2012Metric", mech="R0805_approx",
        notes="Place close to LED data input.", evidence="Yageo datasheet."
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
        "E-021", "DS1", "UI", "OLED 0.96 inch, 128x64, SSD1306, I2C, 3.3 V module", "TBD", "OLED-096-SSD1306-I2C",
        status="DOCUMENTATION_DEFICIENT", alt="SH1106 1.3 inch (different controller); bare SSD1306 panel",
        footprint="OFF_BOARD_MODULE", mech="oled096_approx",
        notes="Verify controller, address, and 3.3 V operation. Do not assume SH1106 is SSD1306-compatible.",
        evidence="Generic module; no traceable manufacturer datasheet yet."
    ),
    row(
        "E-022", "LED1", "UI", "Addressable RGB LED, WS2812B, 5050, 5 V", "Worldsemi", "WS2812B-5050",
        datasheet="https://www.worldsemi.com/", status="PENDING_APPROVAL", footprint="LED_WS2812B_5050",
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
        "E-024", "J1", "Connectors", "2x20 pin female header, 2.54 mm, for DevKitC-1", "TBD", "HDR-2X20-2.54-F",
        status="PROVISIONAL", footprint="PinHeader_2x20_P2.54mm", mech="header_2x20_approx",
        notes="Low-voltage module only. Verify DevKitC-1 pin length and orientation. Anti-misinsertion keying recommended.",
        evidence="Generic header; mechanical fit to be checked."
    ),
    row(
        "E-025", "J2", "Connectors", "JST-XH 4-pin connector for OLED (3.3 V, GND, SDA, SCL)", "JST", "B4B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B4B-XH-A", mech="jst_xh_4_approx", notes="Keyed low-voltage connector.",
        evidence="JST datasheet."
    ),
    row(
        "E-026", "J3", "Connectors", "JST-XH 2-pin connector for button", "JST", "B2B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B2B-XH-A", mech="jst_xh_2_approx", notes="Low-voltage only.",
        evidence="JST datasheet."
    ),
    row(
        "E-027", "J4", "Connectors", "JST-XH 3-pin connector for external RGB (5 V, GND, DATA)", "JST", "B3B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B3B-XH-A", mech="jst_xh_3_approx", notes="Low-voltage only.",
        evidence="JST datasheet."
    ),
    row(
        "E-028", "J5", "Connectors", "JST-XH 6-pin connector for temp/RTC/expansion", "JST", "B6B-XH-A",
        status="PROVISIONAL", footprint="JST_XH_B6B-XH-A", mech="jst_xh_6_approx", notes="Low-voltage only.",
        evidence="JST datasheet."
    ),
    row(
        "E-029", "TB1", "Connectors", "Mains terminal block, 2-pin, 5.08 mm, 300 V / 10 A class", "Phoenix Contact", "MKDS 3/2-5.08",
        status="DOCUMENTATION_DEFICIENT", alt="Degson DG308-5.08-2P; Wago 221-413 (lever nut)",
        footprint="TERMINAL_5.08_2P", mech="terminal_5.08_2p_approx",
        notes="Exact order code and rating must be verified. Terminal must not loosen; use ferrules and strain relief. Mains terminal is not a low-voltage header.",
        evidence="Phoenix series page; exact MPN/rating unverified."
    ),
    row(
        "E-030", "TB2", "Connectors", "Protective earth terminal/stud, screw-clamp, tool-access", "TBD", "PE-TERMINAL-TBD",
        status="BLOCKED", footprint="PE_STUD_TBD", mech="pe_stud_approx",
        notes="PE must be continuous, not switched or fused. Dedicated mechanical bond with lock washer and test point. Exact part is safety-critical and not approved.",
        evidence="No approved part yet; engineer must select and verify."
    ),
    row(
        "E-031", "TB3", "Connectors", "Isolated-side PZEM terminal, 5-pin, 5.08 mm", "Phoenix Contact", "MKDS 3/5-5.08",
        status="DOCUMENTATION_DEFICIENT", footprint="TERMINAL_5.08_5P", mech="terminal_5.08_5p_approx",
        notes="Keep on isolated side of barrier. Pinout must match actual PZEM V4 batch. Do not assume colors.",
        evidence="Exact PZEM pinout unverified."
    ),
    row(
        "E-032", "TB4", "Connectors", "Relay coil terminal, 2-pin, 5.08 mm (SELV)", "Phoenix Contact", "MKDS 3/2-5.08",
        status="PROVISIONAL", footprint="TERMINAL_5.08_2P", mech="terminal_5.08_2p_approx",
        notes="SELV coil only; keep away from mains terminals.", evidence="Series datasheet."
    ),
    row(
        "E-033", "TB5", "Connectors", "5 V input terminal, 2-pin, 5.08 mm (SELV)", "Phoenix Contact", "MKDS 3/2-5.08",
        status="PROVISIONAL", footprint="TERMINAL_5.08_2P", mech="terminal_5.08_2p_approx",
        notes="Keyed/color-coded to reduce miswiring.", evidence="Series datasheet."
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
        "E-041", "PCB1", "PCB", "Low-voltage carrier PCB, 2-layer FR4, 1.6 mm, 1 oz Cu, provisional outline", "TBD", "PCB-CARRIER-REV-A",
        status="PROVISIONAL", footprint="PCB_CARRIER_REV_A", mech="pcb_carrier_approx",
        notes="Mains modules off-board; carrier handles 5 V/3.3 V, I2C, UART isolation, relay driver. Stackup/trace width/clearance are provisional and not released.",
        evidence="KiCad placement file generated; ERC/DRC blocked without KiCad CLI."
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


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    write_csv(BOM / "BOM_MASTER.csv", ROWS)
    write_csv(BOM / "BOM_ELECTRICAL.csv", [r for r in ROWS if r["category"] not in {"Mechanical", "Cable", "Labels", "Consumables", "PCB"}])
    write_csv(BOM / "BOM_MECHANICAL.csv", [r for r in ROWS if r["category"] in {"Mechanical", "Cable", "Labels"}])
    write_csv(BOM / "BOM_TOOLS_AND_TEST.csv", TOOLS)
    write_csv(BOM / "BOM_CONSUMABLES.csv", CONSUMABLES)

    with (BOM / "BOM_MASTER.yaml").open("w", encoding="utf-8") as handle:
        import yaml
        yaml.safe_dump({"project": "esp32-s3-iot-smart-plug", "design_revision": "REV_A_PROVISIONAL", "generated_at": now, "items": ROWS}, handle, sort_keys=False, allow_unicode=True)

    summary = {
        "project": "esp32-s3-iot-smart-plug",
        "design_revision": "REV_A_PROVISIONAL",
        "currency": "IDR",
        "generated_at": now,
        "pricing_status": "UNPRICED",
        "priced_lines": 0,
        "unpriced_lines": len(ROWS),
        "subtotal_idr": None,
        "prototype_1_unit": {"subtotal_idr": None, "status": "UNPRICED"},
        "batch_10_units": {"subtotal_idr": None, "status": "NOT_QUOTED"},
        "owned_components": {"market_cost_idr": None, "cash_out_cost_idr": None, "note": "Q28=B: none owned."},
        "notes": [
            "No verified, dated Indonesian prices were obtained; prices are empty, not Rp0.",
            "BOM is not approved for purchase. Safety-critical parts remain PENDING_APPROVAL, DOCUMENTATION_DEFICIENT, or BLOCKED.",
            "Final rating is 8 A / about 1.840 W (user amendment), limited to electronics/SMPS loads; thermal/lifecycle tests are still required.",
            "Batch 10-unit pricing cannot be quoted without actual supplier quotes."
        ]
    }
    (BOM / "BOM_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# BOM Master — REV_A_PROVISIONAL",
        "",
        f"**Generated:** {now}",
        "",
        "> **UNPRICED / NOT APPROVED.** Harga kosong karena belum ada harga terverifikasi. Jangan membeli atau menganggap BOM ini final. Status safety-critical: lihat `COMPONENT_APPROVALS.yaml`.",
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
        "- Semua harga, stok, dan tautan pembelian sengaja kosong sampai ada kutipan nyata dengan tanggal.",
        "- Komponen mains (socket, plug, relay, fuse, PSU, PE, enclosure) belum disetujui.",
        "- `qty_per_unit` adalah kebutuhan prototipe 1 unit; batch 10 unit belum dihitung.",
        "- Lihat `research/COMPONENT_RESEARCH.md`, `research/UNKNOWN_SPECIFICATIONS.md`, dan `bom/ALTERNATES.md`.",
    ]
    (BOM / "BOM_MASTER.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    approvals = {
        "project": "esp32-s3-iot-smart-plug",
        "design_revision": "REV_A_PROVISIONAL",
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
    with (BOM / "PROCUREMENT_LINKS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item_id", "type", "url", "status"])
        writer.writeheader()
        writer.writerows(links)

    print(f"Wrote {len(ROWS)} master rows, {len(TOOLS)} tools, {len(CONSUMABLES)} consumables.")
    print("Pricing status: UNPRICED (no Rp0 placeholders).")


if __name__ == "__main__":
    main()
