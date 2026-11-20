"""Printable mounting plates for PZEM, PSU board, and relay module.

Prototype mechanical only. Measure the purchased modules before printing.
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"
EXPORT.mkdir(parents=True, exist_ok=True)


def plate(length: float, width: float, holes: list[tuple[float, float]], name: str) -> None:
    body = cq.Workplane("XY").box(length, width, 2.0, centered=(True, True, False))
    body = body.edges("|Z").fillet(2.0)
    body = (
        body.faces(">Z")
        .workplane()
        .pushPoints(holes)
        .hole(3.2)
    )
    body = body.cut(cq.Workplane("XY").box(3.0, 10.0, 3.0).translate((length / 2 - 4, 0, 1)))
    cq.exporters.export(body, str(EXPORT / f"{name}.step"), exportType="STEP")
    cq.exporters.export(body, str(EXPORT / f"{name}.stl"), exportType="STL", tolerance=0.05)
    print(f"wrote {name}.step/.stl")


def main() -> None:
    # PZEM-004T V4 PCB ~74 x 31 mm; bracket holes 65 x 23 mm (verify sample).
    plate(37, 80, [(-11.5, -32.5), (11.5, -32.5), (-11.5, 32.5), (11.5, 32.5)], "pzem_bracket")
    # PSU board 50 x 65 mm; holes at board (3,3), (47,3), (16,42).
    plate(50, 65, [(-22.0, -29.5), (22.0, -29.5), (-9.0, 9.5)], "psu_bracket")
    # Relay module mounting plate remains optional if the shelf is used.
    plate(52, 26, [(-21.0, -8.0), (21.0, -8.0), (-21.0, 8.0), (21.0, 8.0)], "relay_module_bracket")


if __name__ == "__main__":
    main()
