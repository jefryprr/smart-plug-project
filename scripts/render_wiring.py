#!/usr/bin/env python3
"""Render all WireViz harnesses to GV/SVG/PNG and convert SVG to PDF.

Requires Graphviz `dot` in PATH (portable tools/graphviz is used if present).
WireViz does not emit PDF directly; svglib+reportlab handles the conversion.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIRING = ROOT / "hardware" / "wiring"
OUT = WIRING / "renders"
GRAPHVIZ_BIN = ROOT / "tools" / "graphviz" / "Graphviz-16.1.1-win64" / "bin"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if GRAPHVIZ_BIN.exists():
        env["PATH"] = f"{GRAPHVIZ_BIN}{os.pathsep}{env.get('PATH', '')}"
    wireviz = ROOT / ".venv" / "Scripts" / "wireviz.exe"
    if not wireviz.exists():
        found = shutil.which("wireviz")
        if not found:
            print("WireViz executable not found", file=sys.stderr)
            return 2
        wireviz = Path(found)
    failures: list[str] = []
    files = sorted(WIRING.glob("*.yaml"))
    for source in files:
        print(f"Rendering {source.name} ...")
        result = subprocess.run(
            [str(wireviz), "-f", "gsp", "-o", str(OUT), str(source)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            failures.append(f"{source.name}: {result.stderr.strip()}")
            continue
        svg = OUT / f"{source.stem}.svg"
        pdf = OUT / f"{source.stem}.pdf"
        if svg.exists():
            try:
                from svglib.svglib import svg2rlg
                from reportlab.graphics import renderPDF

                drawing = svg2rlg(str(svg))
                if drawing is None:
                    failures.append(f"{source.name}: SVG_PARSE_FAILED")
                else:
                    renderPDF.drawToFile(drawing, str(pdf))
                    print(f"  PDF: {pdf.name} ({pdf.stat().st_size} bytes)")
            except Exception as error:  # noqa: BLE001
                failures.append(f"{source.name}: PDF conversion failed: {error}")
        else:
            failures.append(f"{source.name}: SVG missing")

    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"\nRendered {len(files)} harnesses to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
