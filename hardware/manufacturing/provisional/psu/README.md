# REV_C PSU Board — Provisional Manufacturing Package

**Status:** `ROUTED_PROTOTYPE / ENGINEERING_REVIEW_REQUIRED / NOT_FOR_FABRICATION`  
**Board:** 50 × 65 mm, 2-layer FR4 1.6 mm, 2 oz Cu target, 8 A load path.  
**Files:** `Gerber/psu_rev_c-*`, `Drill/psu_rev_c.drl`, `POSITION.csv`.

## What exists

- Routed F.Cu/B.Cu copper, silkscreen, edge cuts.
- Drilled plated holes and vias.
- Pick-and-place CSV (fiducials/mounting holes excluded).
- DRC **0 violations / 0 unconnected** at 0.5 mm default clearance.

## What is not released

- Creepage/clearance to IEC 60664-1 is **not** verified.
- HLK-5M05 footprint is datasheet-derived, not sample-verified.
- Fuse/MOV/TCO/terminal/JST ratings and breaking capacity are not verified.
- 2 oz copper, 4 mm traces, and 8 A thermal rise are **not** tested.
- No hipot, leakage, PE, thermal, load, or relay test.
- No engineer sign-off or `F4 FABRICATION_RELEASED`.

Do not send this package to a PCB manufacturer for a mains board until an
engineer reviews the schematic, footprint, creepage, assembly, and test plan.
