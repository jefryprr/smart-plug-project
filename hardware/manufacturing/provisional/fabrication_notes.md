# Fabrication Notes — Provisional Placement-Only

**Status:** `PARTIAL / NOT_FOR_FABRICATION`
**Board:** low-voltage carrier only (SELV). No mains on PCB.
**Outline:** 75 × 50 mm, 2-layer, 1.6 mm FR4, 1 oz Cu (provisional).
**Toolchain:** KiCad 10.0.8 portable (`tools/kicad/bin/kicad-cli.exe`).

## What exists

- `hardware/kicad/smartplug.kicad_pcb` — placement-only outline, courtyards, mounting holes, warnings.
- `hardware/kicad/smartplug.kicad_sch` + 9 child sheets — system block schematic (text only, no electrical symbols).
- `reports/kicad/erc.json` — 0 violations (block/text scope).
- `reports/kicad/drc.json` — 0 violations, 0 unconnected (placement geometry).
- `Gerber/*.gbr` / `*.gtl` etc. — placement-only layers/silkscreen/edge cuts.
- `Drill/smartplug.drl`, `smartplug-drl_map.pdf`.
- `hardware/pcb/render/placement_preview.png/.svg`.
- `bom/BOM_MASTER.csv` — 48 rows, unpriced, unapproved.

## What is missing

| Artifact | Status | Root cause |
|---|---|---|
| Component-level schematic | `BLOCKED` | MPN/footprint/clearance approval incomplete |
| Functional netlist/connectivity | `BLOCKED` | No component symbols/pins |
| Footprints/nets | `BLOCKED` | No approved MPNs; no library mapping |
| Routing | `BLOCKED` | Placement only |
| Functional DRC | `BLOCKED` | No circuit |
| Functional Gerber | `BLOCKED` | No copper/nets |
| POSITION | `NOT_APPLICABLE` | No SMT assembly release |
| Mains clearance review | `BLOCKED` | No approved worksheet values |

## Provisional stackup

| Layer | Material | Thickness |
|---|---|---:|
| F.Cu | Copper 1 oz | 0.035 mm |
| Dielectric | FR4 | 1.53 mm |
| B.Cu | Copper 1 oz | 0.035 mm |

Default prototype stackup, not a production decision.

## Safety notes

- The carrier must never carry mains. PZEM and relay module are off-board in the mains zone.
- The 2-channel relay module is **not** a mechanically linked DPST; final 8 A/1.840 W only.
- The mechanical barrier, PE path, and creepage/clearance are not proven by this PCB.
- Do not add mains traces to this board without a new review.

## Reproduce

```powershell
.venv\Scripts\python.exe hardware\generators\generate_schematic.py
$env:PATH = "$PWD\tools\kicad\bin;$env:PATH"
kicad-cli sch erc --output reports/kicad/erc.json hardware/kicad/smartplug.kicad_sch
kicad-cli pcb drc --output reports/kicad/drc.json hardware/kicad/smartplug.kicad_pcb
kicad-cli pcb export gerbers -o hardware/manufacturing/provisional/Gerber -l F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts hardware/kicad/smartplug.kicad_pcb
kicad-cli pcb export drill -o hardware/manufacturing/provisional/Drill --generate-map --map-format pdf hardware/kicad/smartplug.kicad_pcb
.venv\Scripts\python.exe scripts\render_pcb_preview.py
```
