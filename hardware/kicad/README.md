# KiCad Native Files — REV_A_PROVISIONAL

**Status:** `SYSTEM_BLOCK_SCHEMATIC_PROVISIONAL` + `PLACEMENT_ONLY_PCB`
**ERC/DRC/Gerber:** `BLOCKED` (KiCad CLI not installed)

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

- This is **not** a component-level production schematic. It has text/labels and block structure, not every approved part/footprint/net.
- The PCB is **placement-only**: outline, courtyards, mounting holes, warnings. No routing, nets, footprints final, or DRC.
- The files parse with `kiutils`, but were **not opened in KiCad** (not installed).
- Do not fabricate.

## Regenerate

```powershell
.venv\Scripts\python.exe hardware\generators\generate_kicad.py
.venv\Scripts\python.exe scripts\render_pcb_preview.py
```

## When KiCad is installed

```powershell
kicad-cli sch erc --output reports/kicad/erc.json hardware/kicad/smartplug.kicad_sch
kicad-cli pcb drc --output reports/kicad/drc.json hardware/kicad/smartplug.kicad_pcb
```

Fix findings, add approved footprints/nets, route, re-run DRC, export Gerber/drill, then seek F4 release.
