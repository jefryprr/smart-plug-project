#!/usr/bin/env python3
"""Draw the REV_C mains-entry PSU functional schematic."""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "hardware" / "psu"
OUT.mkdir(parents=True, exist_ok=True)


def box(d, x, y, w, h, title, subtitle="", color="#f4f4f4"):
    d.add(elm.Rect(w=w, h=h).at((x, y)).fill(color).color("#333333"))
    d.add(elm.Label(title, fontsize=10).at((x + w / 2, y + h * 0.62)))
    if subtitle:
        d.add(elm.Label(subtitle, fontsize=7).at((x + w / 2, y + h * 0.30)))


def arrow(d, start, end, label="", color="#333333"):
    d.add(elm.Line().at(start).to(end).color(color))
    if label:
        d.add(elm.Label(label, fontsize=7).at(((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.1)))


def main():
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.0, fontsize=9)

    box(d, 0.0, 5.0, 3.0, 1.4, "TB1 230VAC IN", "L / N terminal 5.08 mm", "#ffe8e8")
    box(d, 3.8, 5.0, 2.4, 1.4, "F1", "10 A 250 VAC\nslow-blow", "#fff4d6")
    box(d, 6.8, 5.0, 2.4, 1.4, "MOV1", "275 VAC\nL-N", "#fff4d6")
    box(d, 9.8, 5.0, 2.4, 1.4, "TF1", "99 C one-shot\n10 A", "#fff4d6")
    box(d, 12.8, 5.0, 2.8, 1.4, "TB2 230VAC OUT", "to relay / socket", "#ffe8e8")

    box(d, 3.8, 1.8, 3.0, 1.8, "HLK-5M05", "230 VAC -> 5 V 1 A\ninternal isolation\nPENDING_APPROVAL", "#fff4d6")
    box(d, 7.6, 1.8, 2.6, 1.8, "PTC F2", "1.1 A hold\n+ TVS D1", "#e8f4ff")
    box(d, 10.8, 3.0, 1.6, 1.2, "OUT1", "carrier", "#e8ffe8")
    box(d, 10.8, 1.8, 1.6, 1.2, "OUT2", "relay", "#e8ffe8")
    box(d, 10.8, 0.6, 1.6, 1.2, "OUT3", "PZEM*", "#e8ffe8")

    arrow(d, (3.0, 5.7), (3.8, 5.7), "L")
    arrow(d, (6.2, 5.7), (6.8, 5.7))
    arrow(d, (9.2, 5.7), (9.8, 5.7))
    arrow(d, (12.2, 5.7), (12.8, 5.7), "L_LOAD")
    arrow(d, (0.8, 5.0), (0.8, 4.2), "N")
    arrow(d, (0.8, 4.2), (15.0, 4.2), "N_MAINS")
    arrow(d, (15.0, 4.2), (15.0, 5.0))
    # HLK AC branch from L_LOAD (after TCO), not from the MOV node.
    arrow(d, (12.8, 5.7), (12.8, 4.75), "L_LOAD")
    arrow(d, (12.8, 4.75), (6.8, 4.75))
    arrow(d, (6.8, 4.75), (6.8, 3.6), "HLK AC L")
    arrow(d, (6.8, 4.2), (6.8, 3.0), "HLK AC N")
    arrow(d, (6.8, 1.8), (7.6, 2.7), "5 V")
    arrow(d, (10.2, 2.7), (10.8, 3.6), "5 V")
    arrow(d, (10.2, 2.7), (10.8, 2.4))
    arrow(d, (10.2, 2.7), (10.8, 1.2))

    d.add(elm.Rect(w=3.4, h=2.2).at((3.6, 1.6)).color("#c00000").linestyle("--"))
    d.add(elm.Label("HLK internal isolation\n(not a certified assembly barrier)", fontsize=7).at((5.4, 4.1)))
    d.add(elm.Label("MAINS", fontsize=8).at((0.2, 6.8)))
    d.add(elm.Label("SELV", fontsize=8).at((0.2, 1.2)))
    d.add(elm.Label("*OUT3 = PZEM 5 V only after batch inspection + hipot/leakage; ADR-016", fontsize=7).at((7.0, -0.3)))
    d.add(elm.Label("PE is a dedicated chassis stud; NOT on this PCB and never switched/fused", fontsize=7).at((7.0, -0.8)))
    d.add(elm.Label("REV_C PSU BOARD — NOT FOR FABRICATION / NOT FOR USE", fontsize=8).at((7.0, 7.6)))

    d.save(str(OUT / "psu_schematic.svg"))
    d.save(str(OUT / "psu_schematic.png"), dpi=200)
    print(f"Wrote {OUT / 'psu_schematic.svg'} and .png")


if __name__ == "__main__":
    main()
