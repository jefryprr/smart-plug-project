# KiCad Native Files — REV_A_PROVISIONAL

**Status:** `SYSTEM_BLOCK_SCHEMATIC_PROVISIONAL` + `PLACEMENT_ONLY_PCB`
**KiCad CLI:** 10.0.8 (portable extract in `tools/kicad`)
**ERC:** 0 violations on the block-level text-only schematic (not component-level connectivity)
**DRC:** 0 violations / 0 unconnected on the placement-only PCB
**Gerber/drill:** provisional placement-only export; `NOT_FOR_FABRICATION`
**Component-level schematic/routing:** `BLOCKED` (no approved MPNs/footprints)

## Files

| File | Content |
|---|---|
| `smartplug.kicad_pro` | Project skeleton |
| `smartplug.kicad_sch` | Root system block schematic with 9 hierarchical sheets |
| `AC_INPUT_OUTPUT.kicad_sch` | Plug/socket/fuse/MOV/PE block |
| `SAFETY_AND_SWITCH.kicad_sch` | Relay/thermal cutoff/driver block |
| `AC_DC_POWER.kicad_sch` | PSU block |
| `PZEM_AND_CT.kicad_sch` | Metering/CT/isolated UART block |
| `LOW_VOLTAGE_CONTROL.kicad_sch` | SELV control block |
| `ESP32S3_CARRIER.kicad_sch` | MCU carrier block |
| `DISPLAY_AND_BUTTONS.kicad_sch` | OLED/button/RGB block |
| `TEMP_SENSING.kicad_sch` | TMP102/RTC block |
| `SERVICE_AND_DEBUG.kicad_sch` | USB/UART service block |
| `smartplug.kicad_pcb` | 75×50 mm placement-only low-voltage carrier |

## Important

- This is **not** a component-level production schematic. It has text/labels and block structure, not every approved part/footprint/net. ERC is 0 because there are no electrical symbols to check; this is not proof of connectivity.
- The PCB is **placement-only**: outline, courtyards, mounting holes, warnings. DRC is 0 for that geometry, but there is no routing/nets/component circuit.
- Provisional Gerber/drill exist for mechanical review only. Do not order a functional board.
- Do not fabricate.

## Regenerate

```powershell
.venv\Scripts\python.exe hardware\generators\generate_kicad.py
.venv\Scripts\python.exe scripts\render_pcb_preview.py
```

## When KiCad is installed

```powershell
$env:PATH = "$PWD\tools\kicad\bin;$env:PATH"
kicad-cli sch erc --output reports/kicad/erc.json hardware/kicad/smartplug.kicad_sch
kicad-cli pcb drc --output reports/kicad/drc.json hardware/kicad/smartplug.kicad_pcb
kicad-cli pcb export gerbers -o hardware/manufacturing/provisional/Gerber -l F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts hardware/kicad/smartplug.kicad_pcb
kicad-cli pcb export drill -o hardware/manufacturing/provisional/Drill --generate-map --map-format pdf hardware/kicad/smartplug.kicad_pcb
```

Add approved footprints/nets, route, re-run DRC, export functional Gerber/drill, then seek F4 release.
