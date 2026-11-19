# Mechanical CAD — REV_D_CORE_ONLY (220 × 120 × 70)

**Status:** `MECHANICAL_CONCEPT` / `UNVERIFIED_DIMENSIONS` / `NOT_FOR_MAINS_USE`
**Tool:** CadQuery 2.8.0 + OCP, Python 3.11 (`.venv`)  
**Source of truth:** `source/enclosure.py`, `source/components.py`, `source/brackets.py`, `source/assembly.py`, `parameters.yaml`.

## Build

```powershell
.venv\Scripts\python.exe hardware\mechanical\source\enclosure.py --preset recommended
.venv\Scripts\python.exe hardware\mechanical\source\brackets.py
.venv\Scripts\python.exe hardware\mechanical\source\assembly.py
.venv\Scripts\python.exe hardware\mechanical\source\render.py
```

## Enclosure design

- Outer **220 × 120 × 70 mm**; wall 2.5 mm; corner R4.
- **Deep body 60 mm + shallow lid 10 mm**. The lid joint sits above the socket and most modules.
- 4× M3×16 lid screws into heat-set inserts; flat **1 mm gasket** frame.
- 4× carrier standoffs at the PCB mounting holes; carrier bottom at **8.0 mm** above the floor.
- Printed bosses for PZEM, relay, HLK-5M05, fuse/MOV, terminals, CT, USB cover.
- Mechanical isolation barrier at **x = −4 mm**, height 50 mm, two 10 mm grommet holes.
- Right wall: Type F socket cutout **45 × 45 mm** at y=34, z=35; M16 gland at y=−50, z=18; M12 ePTFE vent at y=−15, z=45.
- Front wall: USB service opening **30 × 20 mm** with a printed cover; mains OFF only.
- Top lid: 12 mm button only. CORE-only removes the OLED window and external RGB light pipe; a small left-wall window is provided for the DevKitC-1 v1.0 onboard RGB (position provisional).
- Printed **DevKit reverse-insertion key** above the antenna end; reverse insertion brings the USB connectors into the key arm.
- Mains zone is right of the barrier; SELV carrier is left. The barrier is mechanical only, not a creepage calculation.

## Outputs

| Artifact | Status |
|---|---|
| `export/body_bottom_recommended.step/.stl` | generated |
| `export/body_top_recommended.step/.stl` | generated |
| `export/gasket.step/.stl` | generated |
| `export/usb_cover.step/.stl` | generated |
| `export/devkit_key.step/.stl` | generated |
| `export/assembly_recommended.step` | generated |
| `export/pzem_bracket.step/.stl` | generated |
| `export/relay_module_bracket.step/.stl` | generated |
| `export/psu_bracket.step/.stl` | generated |
| `render/*.png` | generated from actual STL |
| `drawings/dimensions.svg`, `mounting_plan.svg`, `service_access.svg`, `assembly.pdf` | generated |
| `FIT_ANALYSIS.md`, `CLASH_REPORT.json` | generated |
| `MECHANICAL_BOM.csv`, `MECHANICAL_COST_ESTIMATE.md` | generated/manual |
| `ENCLOSURE_MATERIAL_REVIEW.md`, `PRINT_PROTOTYPE_GUIDE.md` | manual |

## Important limitations

- Module dimensions are **approximate envelopes**, not measured samples.
- Fit analysis is a coarse AABB check; no tolerance stack, cable bend, thermal expansion, or tool access is modeled.
- Only the confirmed **220 × 120 × 70** target is generated; 150 × 100 and 180 × 120 are rejected.
- The enclosure is a mechanical concept. It is **not** a certified electrical enclosure and must not be used for mains until material, clearance, PE, thermal, and impact review are complete.
- `cutaway.png` is an approximate transparent render, not a true section view.
- The gasket, vent, USB cover, and DevKit key are **prototype parts**; their sealing, strength, and flame rating are unverified.

## Review gates

1. Incoming inspection measures all modules and the enclosure.
2. Update `components.py` and `parameters.yaml` with measured values.
3. Re-run fit, render, and bracket exports.
4. Engineer reviews barrier, PE, cable, service access, and reverse-insertion key.
5. Hipot/leakage, thermal, impact, and gasket tests.
6. Only then consider a fabrication release.
