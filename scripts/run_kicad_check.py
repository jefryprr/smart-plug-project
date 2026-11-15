#!/usr/bin/env python3
"""Run KiCad ERC/DRC/Gerber checks and fail on violations/missing outputs."""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KICAD = ROOT / "tools" / "kicad" / "bin" / "kicad-cli.exe"
SCH = ROOT / "hardware" / "kicad" / "smartplug.kicad_sch"
PCB = ROOT / "hardware" / "kicad" / "smartplug.kicad_pcb"
REPORTS = ROOT / "reports" / "kicad"
GERBER = ROOT / "hardware" / "manufacturing" / "provisional" / "Gerber"
DRILL = ROOT / "hardware" / "manufacturing" / "provisional" / "Drill"


def run(command: list[str]) -> int:
    print("RUN", " ".join(str(part) for part in command))
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout.strip())
    if completed.stderr:
        print(completed.stderr.strip())
    return completed.returncode


def violations(path: Path, label: str) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(rf"Found\s+(\d+)\s+{label}", text)
    if not match:
        raise SystemExit(f"Could not parse {path}")
    return int(match.group(1))


def erc_violations(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r";\s*(?:error|warning)", text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["erc", "drc", "gerber", "all"], default="all")
    args = parser.parse_args()
    if not KICAD.exists():
        raise SystemExit(f"KiCad CLI not found: {KICAD}")
    REPORTS.mkdir(parents=True, exist_ok=True)

    if args.mode in {"erc", "all"}:
        code = run([str(KICAD), "sch", "erc", "--output", str(REPORTS / "erc.json"), str(SCH)])
        if code != 0:
            return code
        count = erc_violations(REPORTS / "erc.json")
        print(f"ERC violations: {count} (block-level text-only schematic; not component connectivity)")
        if count != 0:
            return 1

    if args.mode in {"drc", "all"}:
        code = run([str(KICAD), "pcb", "drc", "--output", str(REPORTS / "drc.json"), str(PCB)])
        if code != 0:
            return code
        count = violations(REPORTS / "drc.json", "DRC violations")
        print(f"DRC violations: {count} (placement-only geometry)")
        if count != 0:
            return 1

    if args.mode in {"gerber", "all"}:
        GERBER.mkdir(parents=True, exist_ok=True)
        DRILL.mkdir(parents=True, exist_ok=True)
        code = run([
            str(KICAD), "pcb", "export", "gerbers", "-o", str(GERBER),
            "-l", "F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts", str(PCB)
        ])
        if code != 0:
            return code
        code = run([
            str(KICAD), "pcb", "export", "drill", "-o", str(DRILL),
            "--generate-map", "--map-format", "pdf", str(PCB)
        ])
        if code != 0:
            return code
        required = [GERBER / "smartplug-Edge_Cuts.gm1", GERBER / "smartplug-job.gbrjob", DRILL / "smartplug.drl"]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
        print("Gerber/drill placement-only files present:", not missing)
        if missing:
            print("MISSING:", missing)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
