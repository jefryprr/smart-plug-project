# Gerber — BLOCKED

**Status:** `BLOCKED: KICAD_CLI_NOT_INSTALLED`

No Gerber files are present. Generating Gerber from a hand-written placement file without KiCad would be a fake manufacturing artifact.

Required before release:
1. Approved component-level schematic.
2. Approved footprints and board stackup.
3. Routed PCB with DRC clean (or reviewed exclusions).
4. `kicad-cli pcb export gerbers` with recorded command/version.
5. Gerber/drill re-import check.
6. `F4 FABRICATION_RELEASED` sign-off.

Do not order boards from this folder.
