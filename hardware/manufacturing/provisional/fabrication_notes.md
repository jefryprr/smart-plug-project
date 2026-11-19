# Fabrication Notes — Routed Provisional Carrier + PSU Board (REV_D_CORE_ONLY)

**Status:** `ROUTED_PROTOTYPE / ENGINEERING_REVIEW_REQUIRED / NOT_FOR_FABRICATION`  
**Carrier:** SELV only, 100 × 70 mm; no mains.  
**PSU board:** 50 × 65 mm mains entry, 2 oz Cu target, 2 mm isolation notch.  
**Toolchain:** KiCad 10.0.8 portable (`tools/kicad/bin/kicad-cli.exe`).

## What exists

- `hardware/kicad/smartplug.kicad_pcb` — routed 100 × 70 mm **SELV carrier**, 25 footprints (22 assembled + 3 fiducials), 18 nets, 3 fiducials. No PTC/TVS on the carrier.
- `hardware/kicad/psu_rev_d.kicad_pcb` — routed 50 × 65 mm **PSU board**, 19 footprints (13 assembled + 3 mounting holes + 3 fiducials), 8 nets, TB1/TB2, F1, MOV1, TF1, HLK-5M05, F2/D1, 3× JST.
- `hardware/kicad/smartplug.kicad_sch` + 9 child sheets — system block schematic, including `PSU_MAINS_5V`.
- `hardware/schematic/carrier_schematic.svg/.png` — carrier functional block schematic.
- `hardware/psu/psu_schematic.svg/.png` — PSU functional schematic.
- `hardware/carrier/netlist.csv`, `hardware/psu/netlist.csv` — pin/net tables.
- `reports/kicad/erc.json` — 0 violations (block scope).
- `reports/kicad/drc.json` (carrier) and `reports/kicad/psu_drc.json` (PSU) — 0 violations, 0 unconnected.
- `hardware/manufacturing/provisional/Gerber|Drill|POSITION.csv` — carrier routed prototype.
- `hardware/manufacturing/provisional/psu/Gerber|Drill|POSITION.csv` — PSU routed prototype.
- `hardware/pcb/render/placement_preview.png/.svg` — carrier preview.
- `bom/BOM_MASTER.csv` — 57 rows, unpriced engineering BOM.
- `bom/BOM_PROCUREMENT.csv` — dated prototype buy list.

## What is still missing

| Artifact | Status | Root cause |
|---|---|---|
| Production component schematic | `PARTIAL` | Functional block schematics + netlists; no KiCad symbol-level schematic |
| Footprint library review | `PARTIAL` | Standard/datasheet-derived footprints; HLK is not sample-verified |
| Carrier routing | `PASS_DIGITAL` | Routed, DRC 0/0; SELV only |
| PSU routing | `PASS_DIGITAL` | Routed, DRC 0/0; **DRC is geometry only, not creepage/hipot** |
| Functional Gerber | `PASS_DIGITAL` | Routed copper exported; not fabricated |
| POSITION | `PROVISIONAL` | Assembly positions exist but no assembly release |
| Mains clearance/creepage | `BLOCKED` | OVC/PD/material group/altitude not approved; 2 mm notch is provisional |
| 8 A thermal / 2 oz capability | `BLOCKED` | No lab, no fabricated board |
| Hipot/leakage/PE/thermal/load | `BLOCKED` | No lab/hardware |

## Stackup

| Layer | Carrier | PSU board |
|---|---|---|
| F.Cu | 1 oz (0.035 mm) | **2 oz target (0.070 mm)** — confirm fab capability |
| Dielectric | FR4 1.53 mm | FR4 1.53 mm |
| B.Cu | 1 oz (0.035 mm) | **2 oz target** |
| Board | 1.6 mm, 2-layer | 1.6 mm, 2-layer |
| Surface | HASL/ENIG TBD | HASL/ENIG TBD; solder mask not a creepage substitute |

## PSU board-specific notes

- 4 mm L/N traces; 2 mm routed notch at x=19..21, y=0..45; HLK bridges the notch.
- PE is **not** on the PSU board; it is a dedicated chassis stud.
- TB1/TB2 pin order: pin 1 = N, pin 2 = L. Verify before wiring.
- F1 is before the MOV; TF1 is after the MOV in the L path.
- The 5 V output order is J5 carrier, J6 relay, J7 PZEM (conditional, ADR-016).
- Stencil/assembly: 13 SMT/THT components on the PSU board; fiducials FID1–FID3.

## Release rule

Do not send either board to a manufacturer for mains use until an engineer has reviewed the schematic, footprint, creepage/clearance, stackup, assembly, and test plan, and the F4 gate is approved. This package is `NOT_FOR_FABRICATION`.
