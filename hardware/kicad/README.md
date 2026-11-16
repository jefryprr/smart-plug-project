# KiCad Native Files — REV_C_PSU_BOARD

**Status:** `SYSTEM_BLOCK_SCHEMATIC` + `ROUTED_SELV_CARRIER`  
**KiCad CLI:** 10.0.8 (portable extract in `tools/kicad`)  
**ERC:** 0 violations on the block-level schematic (not a component-level netlist)  
**DRC:** 0 violations / 0 unconnected on the routed 100 × 70 mm SELV carrier (0.15 mm)  
**Gerber/drill/POS:** routed provisional export; `NOT_FOR_FABRICATION`  
**Functional schematic/netlist:** `hardware/schematic/carrier_schematic.*`, `hardware/carrier/netlist.csv`

## Files

| File | Content |
|---|---|
| `smartplug.kicad_pro` | Project skeleton |
| `smartplug.kicad_sch` | Root system block schematic with 10 hierarchical sheets |
| `AC_INPUT_OUTPUT.kicad_sch` | Plug/socket/fuse/MOV/PE block |
| `SAFETY_AND_SWITCH.kicad_sch` | Relay/thermal cutoff/driver block |
| `AC_DC_POWER.kicad_sch` | PSU block |
| `PZEM_AND_CT.kicad_sch` | Metering/CT/PZEM internal isolation block |
| `LOW_VOLTAGE_CONTROL.kicad_sch` | SELV control: 74HCT125, divider, relay driver |
| `ESP32S3_CARRIER.kicad_sch` | MCU carrier block |
| `DISPLAY_AND_BUTTONS.kicad_sch` | OLED/button/RGB block |
| `RTC_ONLY.kicad_sch` | DS3231 only; no TMP102 |
| `SERVICE_AND_DEBUG.kicad_sch` | USB/UART service block |
| `PSU_MAINS_5V.kicad_sch` | REV_C PSU board block: TB1/TB2, F1, MOV, TCO, HLK, PTC/TVS, 3x JST |
| `smartplug.kicad_pcb` | Routed 100 × 70 mm SELV carrier |

## Important

- The KiCad schematic is a **system block schematic** (text/labels), not a
  symbol-level production schematic. The functional schematic and pin/net table
  are in `hardware/schematic/` and `hardware/carrier/netlist.csv`.
- The PCB is **routed**: 25 footprints (22 assembled + 3 fiducials), 18 nets, copper tracks, vias, B.Cu GND
  zone, 100 × 70 mm. DRC is 0/0 at 0.15 mm clearance.
- It is **not released for fabrication**: no engineer sign-off, no physical fit,
  no hipot/thermal/load test, no vendor footprint review.
- The mains-entry PSU board (`psu_rev_c.kicad_pcb`, 50 x 65 mm) carries TB1/TB2, fuse/MOV/TCO, HLK-5M05 and the 3x JST 5 V outputs. The carrier is SELV-only and receives 5 V at J8.
- PZEM internal optocouplers are the only UART isolation barrier. No ADuM1201 or
  B0505S. No temperature sensor in REV_C_PSU_BOARD.

## Regenerate

```powershell
.venv\Scripts\python.exe hardware\generators\generate_kicad.py
tools\kicad\bin\python.exe scripts\generate_carrier_pcb.py
tools\kicad\bin\python.exe scripts\route_carrier.py
.venv\Scripts\python.exe scripts\run_kicad_check.py --mode all
```
