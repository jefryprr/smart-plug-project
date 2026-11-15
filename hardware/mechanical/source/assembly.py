"""Build and export the mechanical assembly from parametric sources."""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

from enclosure import build_assembly, export_preset

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"


def main() -> None:
    for preset in ("provisional", "recommended"):
        assy = build_assembly(preset)
        assy.save(str(EXPORT / f"assembly_{preset}.step"))
        print(f"assembly_{preset}.step written")


if __name__ == "__main__":
    main()
