#!/usr/bin/env python3
"""Generate a native KiCad project skeleton and a placement-only PCB.

This is a SYSTEM BLOCK schematic, not a component-level production schematic.
It is generated honestly because component MPNs/footprints and clearance values
are not approved. KiCad 10.0.8 CLI runs ERC/DRC and exports placement-only
Gerber/drill, but this is not a functional circuit or fabrication release.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KICAD = ROOT / "hardware" / "kicad"
KICAD.mkdir(parents=True, exist_ok=True)

PROJECT = "smartplug"
REV = "REV_A_PROVISIONAL"
DATE = "2026-11-15"

SHEETS = [
    ("AC_INPUT_OUTPUT", ["AC_L_IN", "AC_N_IN", "PE", "AC_L_FUSED", "AC_N_OUT"], "Plug/socket, fuse, MOV, PE path. MAINS."),
    ("SAFETY_AND_SWITCH", ["AC_L_FUSED", "AC_L_SW", "AC_N_SW", "RELAY_IN1", "RELAY_IN2"], "Off-board 2-channel optocoupler relay module, thermal cutoff, MOSFET driver. MAINS + SELV. 8A final."),
    ("AC_DC_POWER", ["AC_L_FUSED", "AC_N_IN", "+5V", "GND"], "Mean Well IRM-05-5 isolated PSU. MAINS + SELV."),
    ("PZEM_AND_CT", ["PZEM_L", "PZEM_N", "CT_P", "CT_N", "+5V_ISO", "GND_ISO", "PZEM_TX", "PZEM_RX"], "PZEM V4 + CT, off-board module with enclosure bracket, isolated UART side."),
    ("LOW_VOLTAGE_CONTROL", ["+3V3", "GND", "I2C_SDA", "I2C_SCL", "PZEM_TX", "PZEM_RX", "RELAY_CTRL"], "SELV control, level shifting, connectors."),
    ("ESP32S3_CARRIER", ["+5V", "GND", "+3V3", "I2C_SDA", "I2C_SCL", "PZEM_TX", "PZEM_RX", "RELAY_CTRL"], "ESP32-S3-DevKitC-1 carrier. SELV."),
    ("DISPLAY_AND_BUTTONS", ["+3V3", "GND", "I2C_SDA", "I2C_SCL", "BUTTON", "RGB_DATA"], "OLED, button, external RGB. SELV."),
    ("TEMP_SENSING", ["+3V3", "GND", "I2C_SDA", "I2C_SCL", "TEMP_ALERT"], "TMP102 and RTC. SELV."),
    ("SERVICE_AND_DEBUG", ["USB_DP", "USB_DM", "UART0_TX", "UART0_RX", "GND"], "USB/UART service. Restricted while mains energized."),
]


def uid() -> str:
    return str(uuid.uuid4())


def title_block() -> str:
    return (
        f'  (title_block (title "Smart Plug - System Block Schematic - 8A Final - Off-board PZEM/Relay") '
        f'(date "{DATE}") (rev "{REV}") (company "OpenCode Digital Engineering"))\n'
    )


def root_schematic() -> str:
    root_uuid = uid()
    parts = [
        "(kicad_sch (version 20231120) (generator eeschema)\n",
        f'  (uuid "{root_uuid}")\n',
        '  (paper "A2")\n',
        title_block(),
        "  (lib_symbols)\n",
    ]
    positions = [(30, 40), (220, 40), (410, 40), (30, 160), (220, 160), (410, 160), (30, 280), (220, 280), (410, 280)]
    for (name, _nets, _note), (x, y) in zip(SHEETS, positions):
        sheet_uuid = uid()
        parts.append(
            f'  (sheet (at {x} {y}) (size 150 90) (fields_autoplaced yes)\n'
            f'    (stroke (width 0.1524) (type solid))\n'
            f'    (fill (color 0 0 0 0.0000))\n'
            f'    (uuid "{sheet_uuid}")\n'
            f'    (property "Sheetname" "{name}" (at {x} {y - 1} 0) (effects (font (size 1.8 1.8)) (justify left bottom)))\n'
            f'    (property "Sheetfile" "{name}.kicad_sch" (at {x} {y + 91} 0) (effects (font (size 1.2 1.2)) (justify left top)))\n'
            f'    (instances (project "{PROJECT}" (path "/{root_uuid}" (page "{SHEETS.index((name, _nets, _note)) + 2}"))))\n'
            f'  )\n'
        )
    parts.append(f'  (sheet_instances (path "/" (page "1")))\n')
    parts.append(")\n")
    return "".join(parts)


def child_schematic(name: str, nets: list[str], note: str, page: int) -> str:
    parts = [
        "(kicad_sch (version 20231120) (generator eeschema)\n",
        f'  (uuid "{uid()}")\n',
        '  (paper "A4")\n',
        title_block(),
        "  (lib_symbols)\n",
    ]
    texts = [
        f"BLOCK: {name}",
        note,
        "STATUS: PROVISIONAL / SYSTEM BLOCK — NOT A COMPONENT-LEVEL SCHEMATIC.",
        "Full component schematic is BLOCKED pending MPN/footprint/clearance approval.",
    ]
    y = 25
    for text in texts:
        safe = text.replace('"', "'")
        parts.append(
            f'  (text "{safe}" (at 20 {y} 0) (effects (font (size 2.0 2.0)) (justify left top)) (uuid "{uid()}"))\n'
        )
        y += 10
    y = 70
    for net in nets:
        # Text net labels, not global labels: this is a block diagram, not a
        # component-level electrical schematic. Text avoids pretending that
        # unconnected labels are a validated netlist.
        parts.append(
            f'  (text "NET: {net}" (at 30 {y} 0) '
            f'(effects (font (size 1.3 1.3)) (justify left)) (uuid "{uid()}"))\n'
        )
        y += 12
    parts.append(f'  (sheet_instances (path "/" (page "{page}")))\n')
    parts.append(")\n")
    return "".join(parts)


def pcb() -> str:
    # Placement-only low-voltage carrier 75 x 50 mm. No mains, no routing, no nets.
    parts = [
        '(kicad_pcb (version 20231120) (generator pcbnew)\n',
        '  (general (thickness 1.6))\n',
        '  (paper "A4")\n',
        '  (layers\n'
        '    (0 "F.Cu" signal)\n'
        '    (31 "B.Cu" signal)\n'
        '    (36 "B.SilkS" user "B.Silkscreen")\n'
        '    (37 "F.SilkS" user "F.Silkscreen")\n'
        '    (44 "Edge.Cuts" user)\n'
        '    (46 "B.CrtYd" user "B.Courtyard")\n'
        '    (47 "F.CrtYd" user "F.Courtyard")\n'
        '  )\n',
        '  (setup (pad_to_mask_clearance 0))\n',
        '  (net 0 "")\n',
        '  (gr_rect (start 0 0) (end 75 50) (stroke (width 0.15) (type solid)) (fill none) (layer "Edge.Cuts") (uuid "' + uid() + '"))\n',
        '  (gr_text "SMART PLUG - LOW-VOLTAGE CARRIER - PLACEMENT ONLY" (at 37.5 3) (layer "F.SilkS") (uuid "' + uid() + '") (effects (font (size 1.1 1.1) (thickness 0.2))))\n',
        '  (gr_text "REV_A_PROVISIONAL - NO MAINS - NOT FOR FABRICATION" (at 37.5 47.5) (layer "F.SilkS") (uuid "' + uid() + '") (effects (font (size 0.9 0.9) (thickness 0.15))))\n',
    ]
    # Courtyards
    courtyards = [
        (4, 4, 68.6, 25.4, "ESP32-S3-DevKitC-1 (approx)"),
        (2, 31, 24, 15, "OLED/JST area"),
        (28, 31, 13, 15, "Temp/RTC/button"),
        (43, 31, 13, 15, "Relay driver"),
        (58, 31, 15, 13, "PZEM isolated connector"),
    ]
    for x, y, w, h, label in courtyards:
        parts.append(
            f'  (gr_rect (start {x} {y}) (end {x + w} {y + h}) (stroke (width 0.1) (type dash)) (fill none) (layer "F.CrtYd") (uuid "{uid()}"))\n'
        )
        parts.append(
            f'  (gr_text "{label}" (at {x + 0.8} {y + 1.5}) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8)) (justify left)))\n'
        )
    # Mounting holes
    for x, y in [(3, 3), (72, 3), (3, 47), (72, 47)]:
        parts.append(
            f'  (footprint "MountingHole_3.2mm_M3" (layer "F.Cu") (uuid "{uid()}") (at {x} {y})\n'
            f'    (attr exclude_from_pos_files exclude_from_bom)\n'
            f'    (fp_circle (center 0 0) (end 3.2 0) (stroke (width 0.15) (type solid)) (fill none) (layer "F.CrtYd"))\n'
            f'    (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask"))\n'
            f'  )\n'
        )
    parts.append(")\n")
    return "".join(parts)


def project() -> str:
    data = {
        "board": {
            "3dviewports": [],
            "design_settings": {
                "defaults": {},
                "rules": {},
                "track_widths": [],
                "via_dimensions": []
            },
            "layer_presets": [],
            "viewports": []
        },
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{PROJECT}.kicad_pro", "version": 1},
        "net_settings": {
            "classes": [
                {
                    "name": "Default",
                    "clearance": 0.2,
                    "track_width": 0.25,
                    "via_diameter": 0.8,
                    "via_drill": 0.4,
                    "wire_width": 6,
                    "bus_width": 12,
                    "line_style": 0,
                    "priority": 1
                }
            ],
            "meta": {"version": 3}
        },
        "pcbnew": {"last_paths": {"gencad": "", "idf": "", "netlist": "", "specctra_dsn": "", "step": "", "vrml": ""}, "page_layout_descr_file": ""},
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [[uid(), "Root"]] + [[uid(), name] for name, _nets, _note in SHEETS],
        "text_variables": {}
    }
    return json.dumps(data, indent=2)


def main() -> None:
    (KICAD / f"{PROJECT}.kicad_sch").write_text(root_schematic(), encoding="utf-8")
    for index, (name, nets, note) in enumerate(SHEETS, start=2):
        (KICAD / f"{name}.kicad_sch").write_text(child_schematic(name, nets, note, index), encoding="utf-8")
    (KICAD / f"{PROJECT}.kicad_pcb").write_text(pcb(), encoding="utf-8")
    (KICAD / f"{PROJECT}.kicad_pro").write_text(project(), encoding="utf-8")
    print(f"Generated {PROJECT}.kicad_pro/.kicad_sch/.kicad_pcb + {len(SHEETS)} child sheets")
    print("STATUS: SYSTEM_BLOCK_SCHEMATIC_PROVISIONAL; placement-only PCB; component-level circuit still BLOCKED.")


if __name__ == "__main__":
    main()
