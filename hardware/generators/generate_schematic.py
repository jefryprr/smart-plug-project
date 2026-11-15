#!/usr/bin/env python3
"""Compatibility entry point for the PRD's generate_schematic.py path.

The project does not use Circuit-Synth in this environment (see ADR-008).
This wrapper invokes the native S-expression generator and documents the
deviation instead of pretending Circuit-Synth produced the file.
"""
from __future__ import annotations

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "hardware" / "generators" / "generate_kicad.py"

if __name__ == "__main__":
    print("NOTE: Circuit-Synth is not used; invoking generate_kicad.py (ADR-008).")
    runpy.run_path(str(TARGET), run_name="__main__")
