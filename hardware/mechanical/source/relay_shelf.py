#!/usr/bin/env python3
"""Printable cantilever shelf for the off-board relay module (REV_C)."""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"
EXPORT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # Plate above the PSU board; two legs land on the enclosure right wall.
    plate = cq.Workplane("XY").box(55, 28, 3).translate((79.5, -3, 40.5))
    leg_a = cq.Workplane("XY").box(3, 3, 12).translate((108.5, -15.5, 34.5))
    leg_b = cq.Workplane("XY").box(3, 3, 12).translate((108.5, 9.5, 34.5))
    shelf = plate.union(leg_a).union(leg_b)
    # M3 clearance holes through the legs (along X) and two module holes.
    for y in (-15.5, 9.5):
        hole = cq.Solid.makeCylinder(1.7, 5, cq.Vector(106.5, y, 34.5), cq.Vector(1, 0, 0))
        shelf = shelf.cut(cq.Workplane(obj=hole))
    for x in (62, 97):
        hole = cq.Solid.makeCylinder(1.7, 5, cq.Vector(x, -3, 39), cq.Vector(0, 0, 1))
        shelf = shelf.cut(cq.Workplane(obj=hole))
    cq.exporters.export(shelf, str(EXPORT / "relay_shelf.step"), exportType="STEP")
    cq.exporters.export(shelf, str(EXPORT / "relay_shelf.stl"), exportType="STL", tolerance=0.05)
    print("wrote relay_shelf.step/.stl")


if __name__ == "__main__":
    main()
