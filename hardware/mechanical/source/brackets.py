"""Simple printable mounting plates for off-board PZEM and 2-channel relay module.

Prototype mechanical only. Not a certified electrical enclosure. Dimensions are
provisional; measure the actual modules before printing.
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"
EXPORT.mkdir(parents=True, exist_ok=True)


def plate(length: float, width: float, hole_x: float, hole_y: float, name: str) -> None:
    body = cq.Workplane("XY").box(length, width, 2.0, centered=(True, True, False))
    body = body.edges("|Z").fillet(2.0)
    body = (
        body.faces(">Z")
        .workplane()
        .pushPoints([(-hole_x, -hole_y), (hole_x, -hole_y), (-hole_x, hole_y), (hole_x, hole_y)])
        .hole(3.2)
    )
    # Add a small cable tie slot near one edge.
    body = body.cut(cq.Workplane("XY").box(3.0, 10.0, 3.0).translate((length / 2 - 4, 0, 1)))
    cq.exporters.export(body, str(EXPORT / f"{name}.step"), exportType="STEP")
    cq.exporters.export(body, str(EXPORT / f"{name}.stl"), exportType="STL", tolerance=0.05)
    print(f"wrote {name}.step/.stl")


def main() -> None:
    plate(58, 94, 24, 42, "pzem_bracket")
    plate(55, 26, 22, 8, "relay_module_bracket")
    plate(38, 23, 15, 8, "psu_bracket")


if __name__ == "__main__":
    main()
