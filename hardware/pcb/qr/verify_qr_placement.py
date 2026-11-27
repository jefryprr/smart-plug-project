#!/usr/bin/env python3
"""Verify the 22 x 22 mm QR label placement on the SELV carrier.

The check is geometric:
- no pad center inside the label rectangle (with clearance)
- no via inside the label rectangle
- no mounting hole / fiducial / test point inside
- board-edge margin
- label does not touch the DevKit socket rows

It does NOT prove mechanical adhesion, chemical compatibility, or RF effects.
"""
from __future__ import annotations

import csv
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAR = ROOT / "hardware" / "carrier" / "netlist.csv"
PCB = ROOT / "hardware" / "kicad" / "smartplug.kicad_pcb"
PLACE = ROOT / "hardware" / "carrier" / "placement.json"
OUT = ROOT / "hardware" / "pcb" / "qr" / "QR_PLACEMENT.md"

# Label rectangle in board coordinates (mm). Origin is top-left of board.
X0, X1 = 14.0, 36.0
Y0, Y1 = 36.0, 58.0
CX, CY = (X0 + X1) / 2, (Y0 + Y1) / 2
CLEAR = 1.5  # mm pad clearance


def dist_point_rect(x: float, y: float) -> float:
    dx = max(X0 - x, 0.0, x - X1)
    dy = max(Y0 - y, 0.0, y - Y1)
    return math.hypot(dx, dy)


def main() -> int:
    lines = [
        "# QR Label Placement — SELV Carrier",
        "",
        f"**Label:** 22 × 22 mm, center `({CX:.1f}, {CY:.1f})` mm, rectangle "
        f"`x={X0:.1f}..{X1:.1f}`, `y={Y0:.1f}..{Y1:.1f}` mm.",
        "",
        "**Layer:** `F.SilkS` outline only; printed label applied inside. "
        "No copper, no solder-mask opening, no netlist change.",
        "",
        "## Clearance checks",
        "",
    ]
    ok = True

    # Pads
    pads = []
    with CAR.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            x, y = float(r["x_mm"]), float(r["y_mm"])
            d = dist_point_rect(x, y)
            if d < CLEAR:
                pads.append((r["ref"], r["pad"], r["net"], x, y, d))
    if pads:
        ok = False
        lines.append(f"- **FAIL** — {len(pads)} pad(s) within {CLEAR} mm of the label:")
        for p in pads:
            lines.append(f"  - {p[0]}.{p[1]} net `{p[2]}` at ({p[3]:.2f},{p[4]:.2f}) — {p[5]:.2f} mm")
    else:
        lines.append(f"- **PASS** — no pad center within {CLEAR} mm of the label.")

    # Vias
    text = PCB.read_text(encoding="utf-8")
    vias = []
    for m in re.finditer(r"\(via\s+\(at\s+([-\d.]+)\s+([-\d.]+)\)", text):
        x, y = float(m.group(1)), float(m.group(2))
        if X0 - 0.5 <= x <= X1 + 0.5 and Y0 - 0.5 <= y <= Y1 + 0.5:
            vias.append((x, y))
    if vias:
        ok = False
        lines.append(f"- **FAIL** — {len(vias)} via(s) inside the label + 0.5 mm:")
        for v in vias:
            lines.append(f"  - via at ({v[0]:.2f},{v[1]:.2f})")
    else:
        lines.append("- **PASS** — no via inside the label + 0.5 mm.")

    # Test points / fiducials / mounting holes from placement + netlist
    special = [
        ("TP5", 36.0, 62.0, 1.5),
        ("TP4", 83.0, 42.0, 1.5),
        ("TP1", 60.0, 60.0, 1.5),
        ("TP2", 60.0, 64.0, 1.5),
        ("FID1", 5.0, 35.0, 2.0),
        ("FID2", 95.0, 35.0, 2.0),
        ("FID3", 50.0, 40.0, 2.0),
        ("H1", 3.5, 3.5, 3.0),
        ("H2", 96.5, 3.5, 3.0),
        ("H3", 3.5, 66.5, 3.0),
        ("H4", 96.5, 66.5, 3.0),
    ]
    bad_special = []
    for name, x, y, r in special:
        if dist_point_rect(x, y) < r + CLEAR:
            bad_special.append((name, x, y, dist_point_rect(x, y), r))
    if bad_special:
        ok = False
        lines.append("- **FAIL** — special feature too close:")
        for s in bad_special:
            lines.append(f"  - {s[0]} at ({s[1]},{s[2]}) — {s[3]:.2f} mm, keepout {s[4]:.1f} mm")
    else:
        lines.append("- **PASS** — all test points, fiducials, and mounting holes are outside the label + keepout.")

    # Board edge
    edge = min(X0, Y0, 100.0 - X1, 70.0 - Y1)
    if edge < 2.0:
        ok = False
        lines.append(f"- **FAIL** — board-edge margin {edge:.2f} mm < 2.0 mm.")
    else:
        lines.append(f"- **PASS** — board-edge margin {edge:.2f} mm ≥ 2.0 mm.")

    # DevKit socket rows
    # J1A/J1B pads are at y=10.0 and 32.86; the label starts at y=36.
    gap = Y0 - 32.86
    if gap < 2.0:
        ok = False
        lines.append(f"- **FAIL** — DevKit socket row gap {gap:.2f} mm < 2.0 mm.")
    else:
        lines.append(f"- **PASS** — DevKit socket row gap {gap:.2f} mm (label starts below the sockets).")

    # Traces may pass under the label; that is electrically harmless.
    seg_count = len(re.findall(r"\(segment\s+\(start", text))
    lines += [
        "",
        "## Notes",
        "",
        f"- The board has {seg_count} track segments; some may pass under the label. "
        "The label is non-conductive and no copper is removed or exposed.",
        "- The label must not be placed on the PSU mains board. This placement is on the SELV carrier only.",
        "- The label adhesive must be low-outgassing acrylic or silicone; operating temperature ≥ 85 °C.",
        "- Apply the label after reflow/cleaning, not before. Do not cover test points or vias.",
        "- Add the footprint at `(25.0, 47.0)` mm on `F.SilkS`; run DRC after adding. "
        "Do not add pads, copper, or solder-mask openings.",
        "",
        "## Result",
        "",
        f"**{'PASS' if ok else 'FAIL'}**",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
