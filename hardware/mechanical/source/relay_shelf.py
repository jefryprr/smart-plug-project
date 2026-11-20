#!/usr/bin/env python3
"""Printable relay shelf for the CORE_ONLY_SHOPEE enclosure.

The plate sits above the PSU board. Two M3x8 screws go through the plate into
internal wall bosses. Prototype only; not a certified electrical enclosure.
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"
EXPORT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    plate = cq.Workplane("XY").box(55, 28, 3).translate((79.5, -3, 41.5))
    # Two screw holes along X into the internal wall bosses.
    for y in (-15.5, 9.5):
        plate = plate.cut(cq.Solid.makeCylinder(1.6, 10, cq.Vector(100, y, 41.5), cq.Vector(1, 0, 0)))
    # Cable-tie / wire-routing slots.
    for x in (58, 98):
        plate = plate.cut(cq.Workplane("XY").box(4, 10, 4).translate((x, -3, 41.5)))
    cq.exporters.export(plate, str(EXPORT / "relay_shelf.step"), exportType="STEP")
    cq.exporters.export(plate, str(EXPORT / "relay_shelf.stl"), exportType="STL", tolerance=0.05)
    print("wrote relay_shelf.step/.stl")


if __name__ == "__main__":
    main()
