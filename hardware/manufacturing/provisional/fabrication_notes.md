# Fabrication Notes — Provisional

**Status:** `BLOCKED`
**Board:** low-voltage carrier only (SELV). No mains on PCB.
**Outline:** 75 × 50 mm, 2-layer, 1.6 mm FR4, 1 oz Cu (provisional).
**Toolchain:** KiCad CLI not installed.

## What exists

- `hardware/kicad/smartplug.kicad_pcb` — placement-only board outline, courtyards, mounting holes, silkscreen warnings.
- `hardware/kicad/smartplug.kicad_sch` + 9 child sheets — system block schematic.
- `hardware/pcb/render/placement_preview.png/.svg` — parsed preview, **not** a KiCad plot.
- `bom/BOM_MASTER.csv` — unpriced, unapproved.

## What is missing

| Artifact | Status | Root cause |
|---|---|---|
| Component-level schematic | `BLOCKED` | MPN/footprint/clearance approval incomplete |
| ERC report | `BLOCKED` | KiCad CLI not installed |
| Footprints/nets | `BLOCKED` | No approved MPNs; no library mapping |
| Routing | `BLOCKED` | Placement only |
| DRC report | `BLOCKED` | KiCad CLI not installed |
| Gerber | `BLOCKED` | KiCad CLI not installed |
| Drill | `BLOCKED` | KiCad CLI not installed |
| POSITION | `NOT_APPLICABLE` | No SMT assembly release |
| Stackup/controlled impedance | `UNVERIFIED` | No manufacturer quote/stackup |
| Mains clearance review | `BLOCKED` | No approved worksheet values |

## Provisional stackup

| Layer | Material | Thickness |
|---|---|---:|
| F.Cu | Copper 1 oz | 0.035 mm |
| Dielectric | FR4 | 1.53 mm |
| B.Cu | Copper 1 oz | 0.035 mm |

This is a default prototype stackup, not a production decision. Confirm with the fabricator and thermal/current calculations.

## Safety notes

- The carrier must never carry mains. Mains modules are off-board.
- The mechanical barrier, PE path, and creepage/clearance are not proven by this PCB.
- Do not add mains traces to this board without a new review.

## Reproduce

```powershell
.venv\Scripts\python.exe hardware\generators\generate_kicad.py
.venv\Scripts\python.exe scripts\render_pcb_preview.py
```

The output remains `PLACEMENT_ONLY` until KiCad ERC/DRC and layout are completed.
