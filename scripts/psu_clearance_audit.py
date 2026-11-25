#!/usr/bin/env python3
"""Provisional copper-clearance audit for the PSU board.

This is a geometric screen only. It does NOT replace IEC 60664-1 creepage
calculation, insulation review, or hipot testing.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware" / "kicad" / "psu_rev_d.kicad_pcb"
OUT = ROOT / "reports" / "psu_clearance_audit_20261124.json"

MAINS = {"L_IN", "N_MAINS", "L_FUSED", "L_LOAD"}
SELV = {"+5V", "+5V_PRE", "GND"}
LN = {"L_IN", "L_FUSED", "L_LOAD"}


def seg_point_dist(ax, ay, bx, by, px, py):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def seg_seg_dist(a, b, c, d):
    # Minimum distance between two 2D segments.
    def ccw(p, q, r):
        return (r[1] - p[1]) * (q[0] - p[0]) - (q[1] - p[1]) * (r[0] - p[0])
    d1 = ccw(a, b, c)
    d2 = ccw(a, b, d)
    d3 = ccw(c, d, a)
    d4 = ccw(c, d, b)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
        return 0.0
    return min(
        seg_point_dist(a[0], a[1], b[0], b[1], c[0], c[1]),
        seg_point_dist(a[0], a[1], b[0], b[1], d[0], d[1]),
        seg_point_dist(c[0], c[1], d[0], d[1], a[0], a[1]),
        seg_point_dist(c[0], c[1], d[0], d[1], b[0], b[1]),
    )


def item_shapes(board):
    """Return list of (net, layer, kind, geometry, half_width)."""
    shapes = []
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            net = pad.GetNetname()
            if not net:
                continue
            pos = pad.GetPosition()
            size = pad.GetSize()
            r = max(pcbnew.ToMM(size.x), pcbnew.ToMM(size.y)) / 2.0
            shapes.append((net, "PAD", "pad", (pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)), r))
    for t in board.GetTracks():
        net = t.GetNetname()
        if not net:
            continue
        if isinstance(t, pcbnew.PCB_VIA):
            pos = t.GetPosition()
            width = t.GetWidth(pcbnew.F_Cu)
            shapes.append((net, "VIA", "pad", (pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)), pcbnew.ToMM(width) / 2.0))
        else:
            s, e = t.GetStart(), t.GetEnd()
            layer = t.GetLayerName()
            shapes.append((net, layer, "seg", ((pcbnew.ToMM(s.x), pcbnew.ToMM(s.y)), (pcbnew.ToMM(e.x), pcbnew.ToMM(e.y))), pcbnew.ToMM(t.GetWidth()) / 2.0))
    return shapes


def dist(a, b):
    ka, ga, wa = a[2], a[3], a[4]
    kb, gb, wb = b[2], b[3], b[4]
    if ka == "pad" and kb == "pad":
        return max(0.0, math.dist(ga, gb) - wa - wb)
    if ka == "pad" and kb == "seg":
        return max(0.0, seg_point_dist(gb[0][0], gb[0][1], gb[1][0], gb[1][1], ga[0], ga[1]) - wa - wb)
    if ka == "seg" and kb == "pad":
        return max(0.0, seg_point_dist(ga[0][0], ga[0][1], ga[1][0], ga[1][1], gb[0], gb[1]) - wa - wb)
    return max(0.0, seg_seg_dist(ga[0], ga[1], gb[0], gb[1]) - wa - wb)


def min_between(shapes, nets_a, nets_b):
    best = None
    for a in shapes:
        if a[0] not in nets_a:
            continue
        for b in shapes:
            if b[0] not in nets_b:
                continue
            if a[0] == b[0]:
                continue
            # Two tracks on different copper layers do not share copper.
            if a[2] == "seg" and b[2] == "seg" and a[1] != b[1]:
                continue
            d = dist(a, b)
            if best is None or d < best["distance_mm"]:
                best = {
                    "distance_mm": round(d, 3),
                    "a": {"net": a[0], "layer": a[1], "kind": a[2], "geom": a[3], "half_width": a[4]},
                    "b": {"net": b[0], "layer": b[1], "kind": b[2], "geom": b[3], "half_width": b[4]},
                }
    return best


def main():
    board = pcbnew.LoadBoard(str(PCB))
    shapes = item_shapes(board)
    result = {
        "board": str(PCB.relative_to(ROOT)),
        "status": "UNVERIFIED / NOT A SAFETY PROOF",
        "note": "Geometric copper clearance screen only; IEC 60664-1 creepage/clearance, coating, barrier continuity, and hipot are still open.",
        "mains_to_selv": min_between(shapes, MAINS, SELV),
        "line_to_neutral": min_between(shapes, LN, {"N_MAINS"}),
        "mains_to_pe": None,
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
