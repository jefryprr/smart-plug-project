#!/usr/bin/env python3
"""Generate the candidate comparison table. No prices are invented."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "candidates.csv"
FIELDS = [
    "candidate_id", "function", "manufacturer", "mpn", "description",
    "key_ratings", "dimensions_mm", "interface", "documentation_status",
    "evidence_score_0_5", "price_idr", "price_checked_at", "seller_url",
    "datasheet_url", "risk", "status", "notes",
]


def row(cid, function, manufacturer, mpn, description, ratings="UNKNOWN", dims="UNKNOWN", interface="UNKNOWN", docs="UNVERIFIED", score="1", datasheet="", risk="", status="RESEARCH_ONLY", notes=""):
    return {
        "candidate_id": cid, "function": function, "manufacturer": manufacturer,
        "mpn": mpn, "description": description, "key_ratings": ratings,
        "dimensions_mm": dims, "interface": interface,
        "documentation_status": docs, "evidence_score_0_5": score,
        "price_idr": "", "price_checked_at": "", "seller_url": "",
        "datasheet_url": datasheet, "risk": risk, "status": status, "notes": notes,
    }


ROWS = [
    row("MCU-01", "MCU", "Espressif", "ESP32-S3-DevKitC-1-N16R8", "Official dev board, 16 MB flash, 8 MB PSRAM", "3.3 V I/O; 5 V input; USB; Wi-Fi/BLE", "~68.6 x 25.4 x 10 (approx)", "USB, headers", "OFFICIAL", "4", "https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html", "v1.0 GPIO48, board availability, price", "PENDING_APPROVAL", "User-confirmed v1.0 (GPIO48); clone/Q08=B if not official; photo/marking still recommended."),
    row("MCU-02", "MCU", "Espressif", "ESP32-S3-DevKitC-1-N8R8", "Official dev board, 8 MB flash, 8 MB PSRAM", "3.3 V I/O; USB", "similar", "USB, headers", "OFFICIAL", "3", "https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html", "Less flash; not preferred", "ALTERNATE", "N16R8 requested."),
    row("MCU-03", "MCU", "Third-party", "ESP32-S3 N16R8 clone", "Clone board with N16R8", "UNKNOWN", "UNKNOWN", "USB, headers", "DOCUMENTATION_DEFICIENT", "1", "", "Pinout/RGB/strapping/regulator may differ", "REJECTED_FOR_NOW", "Q08=C would require photos and model verification."),
    row("MCU-04", "MCU", "Espressif", "ESP32-S3-WROOM-1-N16R8", "Bare module for custom PCB", "3.3 V; 16 MB flash/8 MB PSRAM", "~25.5 x 18 x 3.1 (approx)", "SPI/PSRAM/RF", "OFFICIAL", "3", "https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf", "Requires RF/USB/regulator design", "ALTERNATE", "Production path only after prototype."),
    row("METER-01", "Metering", "Peacefair", "PZEM-004T-V4-100A-CT", "Off-board AC energy meter, 100 A CT (closed or split), UART/Modbus", "80-260 VAC; CT 100 A; UART TTL", "~89 x 53 x 24 (approx)", "UART", "DOCUMENTATION_DEFICIENT", "2", "https://github.com/im-0/pzem-004t-original-docs", "Official V4 batch manual/isolation/pinout not verified; closed CT selected for price", "PENDING_APPROVAL", "Off-board with enclosure bracket; isolation barrier mandatory; CT rating is not output rating."),
    row("METER-02", "Metering", "Peacefair", "PZEM-004T-V3-100A", "Older AC energy meter with CT", "80-260 VAC; CT 100 A", "similar", "UART", "PARTIAL_ARCHIVE", "2", "https://github.com/im-0/pzem-004t-original-docs", "Older version; not a substitute for V4 evidence", "ALTERNATE", "Only if V4 documentation remains unavailable and user approves."),
    row("METER-03", "Metering", "Analog Devices", "ADE7953", "Energy metering IC with CT interface", "Per datasheet; needs burden/calibration", "IC + CT + passives", "SPI/I2C", "OFFICIAL", "4", "https://www.analog.com/en/products/ade7953.html", "New design/calibration/space", "ALTERNATE", "Best traceability path if PZEM fails documentation."),
    row("METER-04", "Metering", "TBD", "HLW8032 + shunt", "Low-cost energy meter IC with shunt", "Per datasheet; shunt carries load", "IC + shunt", "UART", "PARTIAL", "2", "", "Shunt thermal/isolation; not ideal for 8 A continuous", "REJECTED_FOR_NOW", "Would require a new thermal design."),
    row("RELAY-01", "Switching", "Generic module (TBD batch)", "2CH-5V-OPTO-10A", "Common 2-channel 5 V optocoupler relay module, off-board, active-LOW", "2x SPDT; AC 250 V / 10 A vendor claim; final 8 A", "~50 x 24 x 18 (approx)", "VCC/GND/IN1/IN2 + COM/NO/NC per channel", "DOCUMENTATION_DEFICIENT", "2", "https://www.handsontec.com/dataspecs/module/2Ch-relay.pdf", "Vendor claim, not batch evidence; channels are not mechanically linked; shared GND defeats galvanic input isolation", "DOCUMENTATION_DEFICIENT", "User-selected off-board module with enclosure bracket. Final 8 A/1.840 W. Test each channel for weld/stuck-closed."),
    row("RELAY-02", "Switching", "Omron", "G2R-2A DC5", "DPST-NO PCB relay, 5 V coil", "5 A / 250 VAC general use", "~29 x 13 x 25.5", "PCB", "OFFICIAL", "3", "https://omronfs.omron.com/en_US/ecb/products/pdf/en-g2r.pdf", "Too low for 8 A continuous", "ALTERNATE", "Would force rating to ~4 A."),
    row("RELAY-03", "Switching", "Schneider Electric", "Acti9 iCT 2P 16 A", "DIN-rail 2-pole contactor", "16 A / 250 VAC class", "DIN module", "DIN rail", "OFFICIAL", "3", "https://www.se.com/ww/en/product-range/642-acti9-ict/", "Too large for the 220x120x70 confirmed enclosure", "ALTERNATE", "Safer rating but major mechanical redesign."),
    row("RELAY-04", "Switching", "Omron", "G5LE-1A DC5", "SPST-NO PCB relay", "10 A / 250 VAC", "~22.5 x 16.5 x 15.5", "PCB", "OFFICIAL", "2", "https://www.farnell.com/datasheets/2182434.pdf", "Two separate relays are not mechanically linked", "ALTERNATE", "Not preferred for two-pole safety."),
    row("RELAY-05", "Switching", "Hongfa", "HF115F-L DPST latching", "Double-pole latching relay", "10 A class (series claim)", "UNKNOWN", "PCB", "DOCUMENTATION_DEFICIENT", "1", "https://easby.com/shop/hf115f-l-double-pole-latching-relay", "Latching may stay ON after power loss", "REJECTED", "Fail-safe policy rejects latching as sole disconnect."),
    row("RELAY-06", "Switching", "TE Connectivity (Schrack)", "RT444005", "RT2 DPST-NO PCB relay, 5 V coil (earlier concept)", "8 A / 250 VAC IEC class; 2 form A", "~29 x 12.7 x 15.7", "PCB coil + 2 NO contacts", "OFFICIAL", "4", "https://www.mouser.com/datasheet/2/418/9/ENG_DS_RT2_3-576697.pdf", "Superseded by user-selected off-board 2-channel module; exact UL/IEC rating still unverified", "SUPERSEDED", "Better mechanical linkage, but no longer the selected architecture."),
    row("PSU-01", "Power", "Hi-Link", "HLK-5M05", "AC/DC 5 V 1 A module, 5 W, user-selected", "90-264 VAC input; 5 V 1 A; ~70% efficiency at 220 V full load", "38 x 23 x 18", "4 pins: AC/AC/-Vo/+Vo", "DISTRIBUTOR_COPY", "3", "https://www.hlktech.net/index.php?id=1243", "Efficiency ~70% -> ~2.1 W heat; batch certification/isolation/creepage unverified; thermal test required", "PENDING_APPROVAL", "Selected by user. Datasheet claims 2500 VAC isolation and UL/CE design compliance, not a batch certificate."),
    row("PSU-02", "Power", "Recom", "RAC01-05SC", "AC/DC 5 V 0.2 A module", "5 V 0.2 A", "small", "PCB", "OFFICIAL", "2", "", "Current too low for Wi-Fi + relay", "REJECTED_FOR_NOW", "Not enough margin."),
    row("PSU-03", "Power", "Hi-Link", "HLK-PM01", "AC/DC 5 V 0.6 A module", "5 V 0.6 A", "small", "PCB", "DOCUMENTATION_DEFICIENT", "2", "", "Batch quality/isolation/creepage", "ALTERNATE", "Only with sample verification."),
    row("PSU-04", "Power", "Mean Well", "IRM-10-5", "AC/DC 5 V 2 A module", "5 V 2 A", "larger", "Screw/PCB pins", "OFFICIAL", "3", "https://www.meanwell.com/", "Size/thermal", "ALTERNATE", "If peak current requires more margin."),
    row("PSU-05", "Power", "Mean Well", "IRM-05-5", "AC/DC 5 V 1 A module (previous selection)", "90-264 VAC input; 5 V 1 A; ~78% efficiency", "~53.5 x 28.5 x 19", "Screw/PCB pins", "OFFICIAL", "4", "https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.PDF", "Larger, higher cost, but better documentation and thermal margin", "ALTERNATE", "Fallback if HLK-5M05 thermal/certification review fails."),
    row("FUSE-01", "Protection", "Littelfuse", "0215010.MXP", "5x20 mm 10 A 250 V time-lag fuse", "10 A / 250 V; breaking capacity UNKNOWN", "5 x 20", "Fuse holder", "PARTIAL", "3", "https://www.littelfuse.com/", "Coordination/breaking capacity", "PENDING_APPROVAL", "Backup protection only."),
    row("FUSE-02", "Protection", "Schurter", "0001.2510", "5x20 mm 10 A fuse", "10 A / 250 V class", "5 x 20", "Fuse holder", "OFFICIAL", "3", "https://www.schurter.com/", "Coordination", "ALTERNATE", "Equivalent class."),
    row("FUSE-03", "Protection", "Bel Fuse", "5TT 10", "5x20 mm 10 A time-lag fuse", "10 A / 250 V class", "5 x 20", "Fuse holder", "OFFICIAL", "3", "https://www.belfuse.com/", "Coordination", "ALTERNATE", "Equivalent class."),
    row("MOV-01", "Protection", "EPCOS (TDK)", "B72210S0271K101", "MOV 275 VAC 10 mm", "275 VAC class; energy UNKNOWN", "10 mm disc", "PCB", "OFFICIAL", "3", "https://www.tdk-electronics.tdk.com/inf/70/db/varistors/leaded_sio_v_series.pdf", "Surge study/thermal fuse coordination", "PENDING_APPROVAL", "Not a complete surge protector."),
    row("MOV-02", "Protection", "Littelfuse", "V275LA10P", "MOV 275 VAC 10 mm", "275 VAC class", "10 mm", "PCB", "OFFICIAL", "3", "https://www.littelfuse.com/", "Same", "ALTERNATE", ""),
    row("TCO-01", "Protection", "Sefuse", "SF96E", "One-shot thermal cutoff 99 C 10 A", "99 C; 10 A / 250 V (claim)", "axial", "Wire", "DOCUMENTATION_DEFICIENT", "2", "https://www.sefuse.com/", "Batch datasheet/approval", "PENDING_APPROVAL", "Must be clamped to hotspot."),
    row("TCO-02", "Protection", "Therm-O-Disc", "TCO one-shot TBD", "One-shot thermal cutoff", "UNKNOWN", "UNKNOWN", "Wire", "UNKNOWN", "1", "", "Part not selected", "OPEN", "Engineer to select."),
    row("TCO-03", "Protection", "TBD", "KSD301 90 C", "Bimetal thermostat, auto-reset", "10 A / 250 V class", "~30 x 15", "Panel", "PARTIAL", "1", "", "Auto-reset is not one-shot cutoff", "REJECTED", "Not sole thermal protection."),
    row("TEMP-01", "Sensing", "Texas Instruments", "TMP102AIDRLR", "I2C temperature sensor", "3.3 V; I2C", "SOT-563", "I2C", "OFFICIAL", "4", "https://www.ti.com/lit/ds/symlink/tmp102.pdf", "Placement/calibration", "REMOVED", "No temperature sensor in REV_D_CORE_ONLY; keep as future safety revision."),
    row("TEMP-02", "Sensing", "Microchip", "MCP9808", "I2C temperature sensor", "3.3 V; I2C", "MSOP-8", "I2C", "OFFICIAL", "4", "https://ww1.microchip.com/", "Cost", "ALTERNATE", ""),
    row("TEMP-03", "Sensing", "Analog Devices", "DS18B20", "1-Wire temperature probe", "3.3 V; 1-Wire", "TO-92/probe", "1-Wire", "OFFICIAL", "3", "https://www.analog.com/", "Slower response, cable", "ALTERNATE", ""),
    row("OLED-01", "UI", "TBD", "OLED-096-SSD1306-I2C", "0.96 inch 128x64 OLED module", "3.3 V; I2C; SSD1306", "~27 x 27 x 4", "I2C", "DOCUMENTATION_DEFICIENT", "3", "", "Controller/address/batch", "DEFERRED_CORE_ONLY", "Deferred in REV_D."),
    row("OLED-02", "UI", "TBD", "OLED-13-SH1106-I2C", "1.3 inch OLED module", "3.3 V; I2C; SH1106", "~35 x 35", "I2C", "DOCUMENTATION_DEFICIENT", "3", "", "Controller differs from SSD1306", "DEFERRED_CORE_ONLY", "Deferred in REV_D."),
    row("SOCKET-01", "Connector", "TBD", "SOCKET-TYPE-F-16A-TBD", "Type F Schuko panel socket 16 A 2P+E", "16 A / 250 V class", "~50 x 50 x 35", "Panel", "DOCUMENTATION_DEFICIENT", "2", "", "Certification/PE/retention", "BLOCKED", "Q02 remains analysis."),
    row("SOCKET-02", "Connector", "TBD", "SOCKET-TYPE-EF-16A-TBD", "Type E/F combo socket 16 A 2P+E", "16 A / 250 V class", "~50 x 50 x 35", "Panel", "DOCUMENTATION_DEFICIENT", "2", "", "Universal sockets may be non-compliant", "ALTERNATE", "Lean B; not approved."),
    row("ENC-01", "Enclosure", "TBD", "ENCLOSURE-220X120X70-TBD", "ABS/PC enclosure, 220x120x70 confirmed (side-by-side mains modules)", "UNKNOWN", "220 x 120 x 70", "Mechanical", "DOCUMENTATION_DEFICIENT", "2", "", "Flammability/impact/thermal; enclosure 220x120x70 confirmed (Q06=C)", "BLOCKED", "Confirmed working enclosure; 3D print prototype only."),
    row("ENC-02", "Enclosure", "Hammond", "1555/1591 series candidate", "Rated ABS enclosure family", "UNKNOWN", "varies", "Mechanical", "OFFICIAL", "3", "https://www.hammondmfg.com/", "Size/material selection", "ALTERNATE", "Exact MPN/dimensions pending."),
    row("ENC-03", "Enclosure", "TBD", "ENCLOSURE-150X100X70-TBD", "Earlier 150x100x70 target", "UNKNOWN", "150 x 100 x 70", "Mechanical", "DOCUMENTATION_DEFICIENT", "1", "", "Coarse fit fails with off-board PZEM + 2-channel module", "REJECTED", "Kept for comparison only."),
    row("ENC-04", "Enclosure", "TBD", "ENCLOSURE-180X120X70-TBD", "Intermediate 180x120x70 candidate", "UNKNOWN", "180 x 120 x 70", "Mechanical", "DOCUMENTATION_DEFICIENT", "1", "", "Clearance review rejects PZEM/relay/socket stacking", "REJECTED", "Superseded by 220x120x70."),
    row("ISO-01", "Isolation", "Analog Devices", "ADuM1201ARZ", "Dual digital isolator", "2.5 kVrms class; 3.3/5 V", "SOIC-8", "UART", "OFFICIAL", "4", "https://www.analog.com/media/en/technical-documentation/data-sheets/ADuM1200_1201.pdf", "Working voltage/creepage review", "REMOVED", "External barrier removed; PZEM internal optocouplers used."),
    row("ISO-02", "Isolation", "Skyworks", "Si8622", "Dual digital isolator", "2.5 kVrms class", "SOIC-8", "UART", "OFFICIAL", "4", "https://www.skyworksinc.com/", "Availability", "ALTERNATE", ""),
    row("ISO-03", "Isolation", "Mornsun", "B0505S-1WR3", "Isolated 5V/5V 1W DC/DC", "1 W; 5 V", "SIP-4", "Power", "OFFICIAL", "4", "https://www.mornsun-power.com/html/pdf/B0505S-1WR3.html", "Filtering/EMI", "REMOVED", "External isolated DC/DC removed with ADuM barrier."),
    row("DRV-01", "Driver", "Alpha & Omega", "AO3400A", "Logic-level N-MOSFET", "30 V; low Rds(on)", "SOT-23", "Gate", "OFFICIAL", "4", "https://www.aosmd.com/res/data_sheets/AO3400A.pdf", "Boot-safe pulldown mandatory", "PENDING_APPROVAL", ""),
    row("DRV-02", "Driver", "Toshiba", "ULN2003A", "Darlington array", "50 V; 500 mA/ch", "DIP/SOIC", "Logic", "OFFICIAL", "3", "https://www.toshiba-semicon-storage.com/", "More drop/heat; module driver", "ALTERNATE", ""),
    row("RTC-01", "Timekeeping", "Analog Devices", "DS3231MZ+", "I2C RTC with TCXO", "3.3 V; I2C", "SO-16", "I2C", "OFFICIAL", "4", "https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231M.pdf", "Battery/supercap, drift", "DEFERRED_CORE_ONLY", "Deferred in REV_D; SNTP/NVS/API/MQTT/manual time."),
    row("RTC-02", "Timekeeping", "NXP", "PCF8523T", "I2C RTC", "3.3 V; I2C", "SO-8", "I2C", "OFFICIAL", "3", "https://www.nxp.com/", "Crystal/drift", "DEFERRED_CORE_ONLY", "Deferred in REV_D."),
]

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(ROWS)

print(f"Wrote {len(ROWS)} candidates to {OUT}")
