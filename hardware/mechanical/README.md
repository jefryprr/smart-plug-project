# Mechanical CAD — REV_A_PROVISIONAL

**Status:** `PROVISIONAL` / `UNVERIFIED_DIMENSIONS`
**Tool:** CadQuery 2.8.0 + OCP, Python 3.11 (`.venv`)
**Source of truth:** `source/enclosure.py`, `source/components.py`, `source/assembly.py`, `parameters.yaml`.

## Build

```powershell
# from repo root
.venv\Scripts\python.exe hardware\mechanical\source\enclosure.py --preset both
.venv\Scripts\python.exe hardware\mechanical\source\render.py
```

## Outputs

| Artifact | Status |
|---|---|
| `export/body_bottom_provisional.step/.stl` | generated |
| `export/body_top_provisional.step/.stl` | generated |
| `export/assembly_provisional.step` | generated |
| `export/*_recommended.*` | generated |
| `render/isometric.png`, `front.png`, `back.png`, `top.png`, `bottom.png`, `exploded.png`, `cutaway.png` | generated from actual STL |
| `drawings/dimensions.svg`, `mounting_plan.svg`, `service_access.svg`, `assembly.pdf` | generated |
| `FIT_ANALYSIS.md`, `CLASH_REPORT.json` | generated |
| `MECHANICAL_BOM.csv` | generated |
| `ENCLOSURE_MATERIAL_REVIEW.md`, `PRINT_PROTOTYPE_GUIDE.md` | manual |

## Important limitations

- Module dimensions are **APPROXIMATE** envelopes, not measured samples.
- Fit analysis is a coarse AABB check; no tolerance stack, cable bend, thermal expansion, or assembly tool access is modeled.
- The 150×100×70 (Q06=B) preset passes the coarse check only after approximate placement; physical fit is unverified.
- The recommended 180×120×70 preset exists if the target is too tight after measurements (Q06=C requires approval).
- The enclosure is a mechanical concept. It is **not** a certified electrical enclosure and must not be used for mains until material, clearance, PE, and thermal review are complete.
- `cutaway.png` is an approximate transparent render, not a true section view.

## Review gates

1. Incoming inspection measures all modules.
2. Update `components.py` and `parameters.yaml` with measured values.
3. Re-run fit check and render.
4. Engineer reviews barrier, PE, cable, and service access.
5. Thermal/impact tests.
6. Only then consider a fabrication release.
