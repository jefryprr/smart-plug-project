#!/usr/bin/env python3
"""Generate the provisional BLX-A 5x20 mm fuse-holder footprint.

Source: Tayda A-2584 BLX-A datasheet drawing (body 22 x 9.5 x 10.5 mm,
pin 1.4 x 0.35 x 4 mm) plus seller listing stating 21.5 mm pin spacing.
The exact Shopee sample must be measured before fabrication; this footprint
is marked UNVERIFIED in the PCB report.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "hardware" / "kicad" / "footprints" / "SmartPlug.pretty" / "Fuseholder_BLX-A_5x20mm.kicad_mod"

PITCH = 21.5
BODY_W = 22.0
BODY_D = 9.5
PAD = 2.6
DRILL = 1.6


def line(x1: float, y1: float, x2: float, y2: float, layer: str, width: float = 0.12) -> str:
    return (
        "  (fp_line\n"
        f"    (start {x1:.3f} {y1:.3f})\n"
        f"    (end {x2:.3f} {y2:.3f})\n"
        "    (stroke (width %.3f) (type solid))\n"
        f"    (layer \"{layer}\")\n"
        "  )\n" % width
    )


def main() -> None:
    # Body centred on the two pads: pads at 0 and PITCH, body from -0.25 to 21.75.
    x0 = -0.25
    x1 = x0 + BODY_W
    yd = BODY_D / 2
    cy = 0.6  # courtyard margin
    parts = [
        '(footprint "Fuseholder_BLX-A_5x20mm"\n',
        "  (version 20260206)\n",
        '  (generator "pcbnew")\n',
        '  (generator_version "10.0")\n',
        '  (layer "F.Cu")\n',
        '  (descr "BLX-A PCB fuse holder, 5x20 mm, 2 pins at 21.5 mm, body 22 x 9.5 mm; provisional footprint from Tayda A-2584 drawing + seller pin-spacing measurement")\n',
        '  (tags "fuse holder BLX-A 5x20 THT")\n',
        "  (attr through_hole)\n",
        '  (property "Reference" "REF**"\n',
        f"    (at {PITCH / 2:.3f} {-yd - 2.0:.3f} 0)\n",
        '    (layer "F.SilkS")\n',
        '    (effects (font (size 1 1) (thickness 0.15)))\n',
        "  )\n",
        '  (property "Value" "Fuseholder_BLX-A_5x20mm"\n',
        f"    (at {PITCH / 2:.3f} {yd + 2.0:.3f} 0)\n",
        '    (layer "F.Fab")\n',
        '    (effects (font (size 1 1) (thickness 0.15)))\n',
        "  )\n",
    ]
    # Silkscreen body (open at the fuse window is not modelled; outline only).
    parts += [
        line(x0, -yd, x1, -yd, "F.SilkS"),
        line(x1, -yd, x1, yd, "F.SilkS"),
        line(x1, yd, x0, yd, "F.SilkS"),
        line(x0, yd, x0, -yd, "F.SilkS"),
        # Fab body.
        line(x0, -yd, x1, -yd, "F.Fab", 0.1),
        line(x1, -yd, x1, yd, "F.Fab", 0.1),
        line(x1, yd, x0, yd, "F.Fab", 0.1),
        line(x0, yd, x0, -yd, "F.Fab", 0.1),
        # Courtyard.
        line(x0 - cy, -yd - cy, x1 + cy, -yd - cy, "F.CrtYd", 0.05),
        line(x1 + cy, -yd - cy, x1 + cy, yd + cy, "F.CrtYd", 0.05),
        line(x1 + cy, yd + cy, x0 - cy, yd + cy, "F.CrtYd", 0.05),
        line(x0 - cy, yd + cy, x0 - cy, -yd - cy, "F.CrtYd", 0.05),
    ]
    for number, x in (("1", 0.0), ("2", PITCH)):
        parts += [
            f'  (pad "{number}" thru_hole circle\n',
            f"    (at {x:.3f} 0)\n",
            f"    (size {PAD:.3f} {PAD:.3f})\n",
            f"    (drill {DRILL:.3f})\n",
            '    (layers "*.Cu" "*.Mask")\n',
            "  )\n",
        ]
    parts.append(")\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
