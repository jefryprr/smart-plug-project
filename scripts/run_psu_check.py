#!/usr/bin/env python3
"""Run PSU board DRC and export provisional Gerber/drill/POS."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KICAD = ROOT / "tools" / "kicad" / "bin" / "kicad-cli.exe"
PCB = ROOT / "hardware" / "kicad" / "psu_rev_d.kicad_pcb"
REPORTS = ROOT / "reports" / "kicad"
OUT = ROOT / "hardware" / "manufacturing" / "provisional" / "psu"
DRC = REPORTS / "psu_drc.json"


def run(command: list[str]) -> int:
    print("RUN", " ".join(str(part) for part in command))
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (OUT / "Gerber").mkdir(parents=True, exist_ok=True)
    (OUT / "Drill").mkdir(parents=True, exist_ok=True)
    code = run([str(KICAD), "pcb", "drc", "--format", "json", "--output", str(DRC), str(PCB)])
    if code != 0:
        return code
    data = json.loads(DRC.read_text(encoding="utf-8"))
    violations = len(data.get("violations", []))
    unconnected = len(data.get("unconnected_items", []))
    print(f"PSU DRC violations: {violations}; unconnected: {unconnected}")
    if violations or unconnected:
        return 1
    commands = [
        [str(KICAD), "pcb", "export", "gerbers", "-o", str(OUT / "Gerber"), "-l", "F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts", str(PCB)],
        [str(KICAD), "pcb", "export", "drill", "-o", str(OUT / "Drill"), "--generate-map", "--map-format", "pdf", str(PCB)],
        [str(KICAD), "pcb", "export", "pos", "-o", str(OUT / "POSITION.csv"), "--format", "csv", "--units", "mm", "--side", "both", str(PCB)],
    ]
    for command in commands:
        code = run(command)
        if code != 0:
            return code
    for path in [
        OUT / "Gerber" / "psu_rev_d-F_Cu.gtl",
        OUT / "Drill" / "psu_rev_d.drl",
        OUT / "POSITION.csv",
    ]:
        if not path.exists():
            print(f"MISSING: {path}")
            return 1
    print("PSU Gerber/drill/POS present: True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
