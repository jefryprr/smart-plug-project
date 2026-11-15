"""Build and export the mechanical assembly from parametric sources."""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

from enclosure import build_assembly

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"


def main() -> None:
    assy = build_assembly()
    assy.save(str(EXPORT / "assembly_recommended.step"))
    print("assembly_recommended.step written")


if __name__ == "__main__":
    main()
