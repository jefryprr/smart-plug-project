#!/usr/bin/env python3
"""Static checks for the REV_C mains-entry PSU board.

This is a digital consistency check, not a safety proof. It verifies net
membership, the L/N protection order, the 3x 5 V outputs, the PTC/TVS, and
that the carrier has no mains or duplicate 5 V protection.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PSU = ROOT / "hardware" / "kicad" / "psu_rev_c.kicad_pcb"
CARRIER = ROOT / "hardware" / "kicad" / "smartplug.kicad_pcb"
BOM = ROOT / "bom" / "BOM_MASTER.csv"
PCBA_PSU = ROOT / "hardware" / "manufacturing" / "provisional" / "BOM_PCBA_PSU.csv"
VALIDATION = ROOT / "validation"


def pad_nets(board: pcbnew.BOARD) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for fp in board.GetFootprints():
        out[str(fp.GetReference())] = {str(p.GetNumber()): str(p.GetNetname()) for p in fp.Pads()}
    return out


def main() -> int:
    board = pcbnew.LoadBoard(str(PSU))
    pads = pad_nets(board)
    nets = {n.GetNetname() for n in board.GetNetsByName().values() if n.GetNetname()}
    issues: list[str] = []

    expected = {"L_IN", "N_MAINS", "L_FUSED", "L_LOAD", "+5V_PRE", "+5V", "GND"}
    if nets != expected:
        issues.append(f"NET_SET:{sorted(nets)}")
    if "PE" in nets:
        issues.append("PE_NET_ON_PSU_BOARD")

    def check(ref: str, pad: str, net: str) -> None:
        actual = pads.get(ref, {}).get(pad)
        if actual != net:
            issues.append(f"PAD_NET:{ref}.{pad}={actual},expected={net}")

    # Mains order: TB1 L -> F1 -> L_FUSED -> TCO -> L_LOAD -> TB2/HLK.
    check("TB1", "1", "N_MAINS")
    check("TB1", "2", "L_IN")
    check("F1", "1", "L_IN")
    check("F1", "2", "L_FUSED")
    check("MOV1", "1", "L_FUSED")
    check("MOV1", "2", "N_MAINS")
    check("TF1", "1", "L_FUSED")
    check("TF1", "2", "L_LOAD")
    check("PS1", "1", "L_LOAD")
    check("PS1", "2", "N_MAINS")
    check("TB2", "1", "N_MAINS")
    check("TB2", "2", "L_LOAD")

    # HLK DC and 5 V protection.
    check("PS1", "3", "GND")
    check("PS1", "4", "+5V_PRE")
    check("F2", "1", "+5V")
    check("F2", "2", "+5V_PRE")
    check("D1", "1", "+5V")
    check("D1", "2", "GND")
    check("C1", "1", "+5V")
    check("C1", "2", "GND")
    check("C2", "1", "+5V")
    check("C2", "2", "GND")

    # Three 5 V outputs.
    for ref in ("J5", "J6", "J7"):
        check(ref, "1", "+5V")
        check(ref, "2", "GND")

    # Board size and 8 A trace widths.
    edge = board.GetBoardEdgesBoundingBox()
    w = pcbnew.ToMM(edge.GetWidth())
    h = pcbnew.ToMM(edge.GetHeight())
    if not (49.0 <= w <= 51.0 and 64.0 <= h <= 66.0):
        issues.append(f"BOARD_SIZE:{w:.2f}x{h:.2f}")
    widths_by_net: dict[str, list[float]] = {}
    for track in board.GetTracks():
        if isinstance(track, pcbnew.PCB_VIA):
            continue
        widths_by_net.setdefault(str(track.GetNetname()), []).append(pcbnew.ToMM(track.GetWidth()))
    for net in ("L_IN", "N_MAINS", "L_FUSED", "L_LOAD"):
        if max(widths_by_net.get(net, [0.0])) < 3.9:
            issues.append(f"TRACK_WIDTH:{net}<4mm")

    # Carrier must be SELV-only and must not duplicate F2/D1.
    carrier = pcbnew.LoadBoard(str(CARRIER))
    carrier_nets = {n.GetNetname() for n in carrier.GetNetsByName().values() if n.GetNetname()}
    for net in carrier_nets:
        if any(token in net.upper() for token in ("L_IN", "N_MAINS", "L_FUSED", "L_LOAD", "230", "MAINS")):
            issues.append(f"CARRIER_MAINS_NET:{net}")
    carrier_refs = {str(fp.GetReference()) for fp in carrier.GetFootprints()}
    for ref in ("F2", "D1"):
        if ref in carrier_refs:
            issues.append(f"CARRIER_DUPLICATE_PROTECTION:{ref}")

    # BOM crosscheck for the PSU assembly.
    with BOM.open(newline="", encoding="utf-8") as handle:
        master_refs = set()
        for row in csv.DictReader(handle):
            for ref in row["reference_designators"].split(","):
                ref = ref.strip()
                if ref:
                    master_refs.add(ref)
    with PCBA_PSU.open(newline="", encoding="utf-8") as handle:
        pcba_refs = {row["reference_designators"].strip() for row in csv.DictReader(handle)}
    missing = sorted(pcba_refs - master_refs)
    if missing:
        issues.append(f"BOM_MISSING_REFS:{missing}")

    # Gerber/drill/POS presence.
    for path in [
        ROOT / "hardware" / "manufacturing" / "provisional" / "psu" / "Gerber" / "psu_rev_c-F_Cu.gtl",
        ROOT / "hardware" / "manufacturing" / "provisional" / "psu" / "Drill" / "psu_rev_c.drl",
        ROOT / "hardware" / "manufacturing" / "provisional" / "psu" / "POSITION.csv",
    ]:
        if not path.exists():
            issues.append(f"MISSING:{path.relative_to(ROOT)}")

    result = {
        "status": "PASS" if not issues else "FAIL",
        "board": "hardware/kicad/psu_rev_c.kicad_pcb",
        "board_size_mm": [round(w, 2), round(h, 2)],
        "nets": sorted(nets),
        "footprints": len([f for f in board.GetFootprints() if not str(f.GetReference()).startswith(("H", "FID"))]),
        "issues": issues,
        "limitations": [
            "Static net/width check only; DRC does not prove creepage or hipot.",
            "HLK-5M05 footprint is datasheet-derived, not sample-verified.",
            "Fuse/MOV/TCO/terminal/JST ratings are not verified by this script.",
            "No physical mains test was performed.",
        ],
    }
    VALIDATION.mkdir(exist_ok=True)
    (VALIDATION / "PSU_CROSSCHECK.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
