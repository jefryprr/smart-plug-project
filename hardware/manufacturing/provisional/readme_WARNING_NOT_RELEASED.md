# WARNING — PROVISIONAL MANUFACTURING PACKAGE

**STATUS:** `NOT_FOR_FABRICATION`
**DESIGN REVISION:** `REV_A_PROVISIONAL`
**DATE:** 2026-11-15

This directory does **not** contain a released manufacturing package.

- No Gerber files were generated: KiCad CLI is not installed.
- No drill files were generated.
- No pick-and-place file: PCB is placement-only and has no approved footprints/nets.
- No DRC/ERC report: KiCad is not installed.
- No component is approved for fabrication.
- The schematic is a **system block schematic**, not a component-level production schematic.
- The PCB is a **placement-only low-voltage carrier**; it has no mains and no routing.

Do not send this directory to a PCB manufacturer. Do not use it to order boards, stencils, or assembly.

The only valid next steps are:
1. Install KiCad, complete component-level schematic with approved MPNs.
2. Run ERC/DRC, fix findings.
3. Complete layout, stackup, clearance review.
4. Re-export Gerber/drill/POS/BOM.
5. Obtain `F4 FABRICATION_RELEASED` sign-off.
