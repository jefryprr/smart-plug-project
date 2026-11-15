# PCB Render — Status

**Status:** `PARTIAL / BLOCKED`

| Artifact | Status | Note |
|---|---|---|
| `placement_preview.png` | `PROVISIONAL` | Parsed from `smartplug.kicad_pcb`; not a KiCad plot |
| `placement_preview.svg` | `PROVISIONAL` | Same |
| `front.png` | `BLOCKED` | Requires KiCad plot/render |
| `back.png` | `BLOCKED` | Requires KiCad plot/render |
| `top_copper.svg` | `BLOCKED` | Requires KiCad plot |
| `bottom_copper.svg` | `BLOCKED` | Requires KiCad plot |
| `assembly.png` | `BLOCKED` | Requires routed/placed PCB + KiCad render |
| `3d_angled.png` | `BLOCKED` | Requires KiCad 3D render/STEP |
| `pcb_model.step` | `BLOCKED` | Requires KiCad 3D export |

The placement preview is derived from the actual board outline and courtyards, but it does not show copper, routing, or a validated mechanical fit. Do not use it as fabrication evidence.
