#!/usr/bin/env python3
"""Export carrier netlist, placement, PCBA BOM and POSITION from the routed board.

Run with the KiCad Python:
  tools\\kicad\\bin\\python.exe scripts\\export_carrier_artifacts.py
"""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware" / "kicad" / "smartplug.kicad_pcb"
OUT = ROOT / "hardware" / "carrier"
PROV = ROOT / "hardware" / "manufacturing" / "provisional"
KICAD = ROOT / "tools" / "kicad" / "bin" / "kicad-cli.exe"


def main() -> None:
    board = pcbnew.LoadBoard(str(PCB))
    pads: list[dict[str, object]] = []
    placement: list[dict[str, object]] = []
    for fp in board.GetFootprints():
        ref = str(fp.GetReference())
        value = str(fp.GetValue())
        pos = fp.GetPosition()
        placement.append({
            "ref": ref,
            "value": value,
            "footprint": f"{fp.GetFPID().GetLibNickname()}:{fp.GetFPID().GetLibItemName()}",
            "x": round(pcbnew.ToMM(pos.x), 3),
            "y": round(pcbnew.ToMM(pos.y), 3),
            "rot": fp.GetOrientationDegrees(),
        })
        for pad in fp.Pads():
            p = pad.GetPosition()
            pads.append({
                "ref": ref,
                "value": value,
                "pad": str(pad.GetNumber()),
                "net": str(pad.GetNetname()),
                "x_mm": round(pcbnew.ToMM(p.x), 3),
                "y_mm": round(pcbnew.ToMM(p.y), 3),
                "layer": (
                    "F.Cu" if pad.IsOnLayer(pcbnew.F_Cu) and not pad.IsOnLayer(pcbnew.B_Cu)
                    else "B.Cu" if pad.IsOnLayer(pcbnew.B_Cu) and not pad.IsOnLayer(pcbnew.F_Cu)
                    else "THT"
                ),
            })
    pads.sort(key=lambda r: (str(r["ref"]), int(str(r["pad"])) if str(r["pad"]).isdigit() else 999))
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "netlist.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ref", "value", "pad", "net", "x_mm", "y_mm", "layer"])
        writer.writeheader()
        writer.writerows(pads)
    (OUT / "placement.json").write_text(json.dumps(placement, indent=2), encoding="utf-8")

    pcba = []
    for fp in board.GetFootprints():
        ref = str(fp.GetReference())
        if ref.startswith(("FID", "H")):
            continue
        pcba.append({
            "reference_designators": ref,
            "description": str(fp.GetValue()),
            "manufacturer": "TBD",
            "mpn": "TBD",
            "qty": 1,
            "footprint": str(fp.GetFPID().GetLibItemName()),
            "approved_status": "PROVISIONAL",
            "notes": "REV_C_PSU_BOARD routed SELV carrier; mounting holes and fiducials excluded from assembly BOM",
        })
    pcba.sort(key=lambda r: str(r["reference_designators"]))
    with (PROV / "BOM_PCBA.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["reference_designators", "description", "manufacturer", "mpn", "qty", "footprint", "approved_status", "notes"],
        )
        writer.writeheader()
        writer.writerows(pcba)

    subprocess.run(
        [
            str(KICAD), "pcb", "export", "pos", "-o", str(PROV / "POSITION.csv"),
            "--format", "csv", "--units", "mm", "--side", "both", str(PCB),
        ],
        cwd=ROOT,
        check=True,
    )
    print(f"carrier pads={len(pads)} placement={len(placement)} pcba={len(pcba)}")


if __name__ == "__main__":
    main()
