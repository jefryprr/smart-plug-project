# WARNING — PROVISIONAL ROUTED PROTOTYPE

**STATUS:** `ROUTED_PROTOTYPE / ENGINEERING_REVIEW_REQUIRED / NOT_FOR_FABRICATION`  
**DESIGN REVISION:** `REV_D_CORE_ONLY`  
**DATE:** 2026-11-16

This directory contains a **routed SELV carrier** (100 × 70 mm), not a released
manufacturing package.

- Gerber/drill were exported by KiCad 10.0.8 from `hardware/kicad/smartplug.kicad_pcb`.
- DRC is **0 violations / 0 unconnected** at 0.15 mm default clearance.
- Copper is routed; there are real footprints, nets, vias, and a B.Cu GND zone.
- The board is **SELV only**. PZEM, relay module, HLK-5M05, fuse/MOV/TCO, and
  socket/plug remain off-board in the mains zone.
- The schematic is a **system block schematic** (`hardware/kicad/`) plus a
  functional schematic (`hardware/schematic/carrier_schematic.*`) and a
  component/net table. It is not a production-certified schematic.
- No component is approved for fabrication. BOM is `NOT_APPROVED`.
- No physical fit, hipot, thermal, or load test has been performed.

Do not send this directory to a PCB manufacturer for a functional board until
an engineer reviews the schematic, netlist, footprints, creepage, connector
pinout, and assembly. The valid next step is `F4 FABRICATION_RELEASED`.
