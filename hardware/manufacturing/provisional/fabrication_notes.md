# Fabrication Notes — Routed Prototype Carrier (REV_B)

**Status:** `ROUTED_PROTOTYPE / ENGINEERING_REVIEW_REQUIRED / NOT_FOR_FABRICATION`  
**Board:** SELV carrier only. No mains on PCB.  
**Outline:** 100 × 70 mm, 2-layer, 1.6 mm FR4, 1 oz Cu (provisional).  
**Toolchain:** KiCad 10.0.8 portable (`tools/kicad/bin/kicad-cli.exe`).

## What exists

- `hardware/kicad/smartplug.kicad_pcb` — routed 100 × 70 mm SELV carrier, 27 footprints, 19 nets, 5 V PTC + TVS, 3 fiducials.
- `hardware/kicad/smartplug.kicad_sch` + 9 child sheets — system block schematic.
- `hardware/schematic/carrier_schematic.svg/.png` — functional block schematic.
- `hardware/carrier/netlist.csv` — pin/net table.
- `reports/kicad/erc.json` — 0 violations (block scope).
- `reports/kicad/drc.json` and `reports/kicad/carrier_drc.json` — 0 violations,
  0 unconnected at 0.15 mm default clearance.
- `Gerber/*.gtl/*.gbl/*.gto/*.gbo/*.gm1` — routed copper/silkscreen/edge cuts.
- `Drill/smartplug.drl`, `smartplug-drl_map.pdf`.
- `hardware/pcb/render/placement_preview.png/.svg` — preview.
- `bom/BOM_MASTER.csv` — 56 rows, unpriced engineering BOM.
- `bom/BOM_PROCUREMENT.csv` — dated prototype buy list.

## What is still missing

| Artifact | Status | Root cause |
|---|---|---|
| Production component schematic | `PARTIAL` | Functional block schematic + netlist; no KiCad symbol-level schematic |
| Footprint library review | `PARTIAL` | Standard KiCad footprints used; not vendor-certified |
| Routing | `PASS_DIGITAL` | Routed, DRC 0/0; 5 V PTC/TVS; 3 fiducials |
| Functional Gerber | `PASS_DIGITAL` | Routed copper exported; not fabricated |
| POSITION | `PROVISIONAL` | Assembly positions exist but no assembly release |
| Mains clearance/creepage | `BLOCKED` | Carrier is SELV; mains modules off-board; assembly review required |
| Hipot/thermal/load | `BLOCKED` | No lab/hardware |

## Stackup

| Layer | Material | Thickness |
|---|---|---:|
| F.Cu | Copper 1 oz | 0.035 mm |
| Dielectric | FR4 | 1.53 mm |
| B.Cu | Copper 1 oz | 0.035 mm |

Default prototype stackup, not a production decision.

## Safety notes

- The carrier must never carry mains. PZEM, relay, HLK-5M05, fuse/MOV/TCO, and
  socket/plug are off-board in the mains zone.
- The 2-channel relay module is **not** a mechanically linked DPST; final
  8 A/1.840 W only after thermal/lifecycle test.
- PZEM internal optocouplers are the only UART isolation barrier. Review
  creepage and perform hipot/leakage before mains use.
- No temperature sensor; thermal protection is fuse + one-shot TCO only.
- Do not add mains traces to this board without a new review.

## Reproduce

```powershell
tools\kicad\bin\python.exe scripts\generate_carrier_pcb.py
tools\kicad\bin\python.exe scripts\route_carrier.py
tools\kicad\bin\kicad-cli.exe pcb drc --format json --output reports/kicad/carrier_drc.json hardware/kicad/smartplug.kicad_pcb
tools\kicad\bin\kicad-cli.exe pcb export gerbers -o hardware/manufacturing/provisional/Gerber -l F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts hardware/kicad/smartplug.kicad_pcb
tools\kicad\bin\kicad-cli.exe pcb export drill -o hardware/manufacturing/provisional/Drill --generate-map --map-format pdf hardware/kicad/smartplug.kicad_pcb
```
