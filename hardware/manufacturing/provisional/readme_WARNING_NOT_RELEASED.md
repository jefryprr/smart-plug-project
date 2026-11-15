# WARNING — PROVISIONAL MANUFACTURING PACKAGE

**STATUS:** `NOT_FOR_FABRICATION`
**DESIGN REVISION:** `REV_A_PROVISIONAL`
**DATE:** 2026-11-15

This directory contains **provisional placement-only** manufacturing geometry, not a functional circuit.

- Gerber/drill were exported by KiCad 10.0.8 from a **placement-only low-voltage carrier** (75×50 mm).
- The PCB has **no routing, no nets, no approved component footprints**; copper layers are essentially empty.
- ERC is 0 on the text-only block schematic; DRC is 0 on the placement geometry. These do not prove a functional circuit.
- The schematic is a **system block schematic**, not a component-level production schematic.
- No component is approved for fabrication.
- BOM is **UNPRICED/UNAPPROVED**.

Do not send this directory to a PCB manufacturer for a functional board. It is only useful for mechanical/outline review and toolchain evidence.

The valid next steps are:
1. Select/verify all MPNs and footprints.
2. Complete component-level schematic and connectivity.
3. Route the PCB, run ERC/DRC on the real circuit.
4. Re-export Gerber/drill/POS/BOM.
5. Obtain `F4 FABRICATION_RELEASED` sign-off.
