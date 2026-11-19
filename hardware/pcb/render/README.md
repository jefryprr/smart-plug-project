# PCB Render — Status (REV_D_CORE_ONLY)

**Status:** `ROUTED_PREVIEW / NOT_FOR_FABRICATION`

| Artifact | Status | Note |
|---|---|---|
| `carrier.svg` | `ROUTED_PREVIEW` | KiCad CLI SVG of F.Cu/B.Cu/silkscreen/edge cuts |
| `placement_preview.png` | `PROVISIONAL` | Coarse matplotlib outline; not a KiCad plot |
| `placement_preview.svg` | `PROVISIONAL` | Same |
| 3D STEP/render | `BLOCKED` | Not exported for the routed board |

The routed carrier is 100 × 70 mm, DRC 0/0 at 0.15 mm. The preview is not a
fabrication release; use `hardware/manufacturing/provisional/` only after
engineering review.
