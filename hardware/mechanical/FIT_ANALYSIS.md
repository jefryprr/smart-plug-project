# Fit Analysis - REV_D_CORE_ONLY

**Status:** coarse digital fit check only. Dimensions are approximate; no physical fit validation.

## Preset: recommended (220 x 120 x 70)

- Status: **PASS**
- Modules checked: 13
- Enclosure internal bounds (mm): (-107.5, -57.5, 2.5, 107.5, 57.5, 67.5)

## Limitations
- All module dimensions are approximate envelopes, not measured samples.
- PZEM/socket/relay dimensions must be measured on the purchased parts.
- No tolerance stack, cable bend, or thermal expansion is modeled.
- A PASS here is only a coarse digital fit check; it is not a mechanical validation.
- Barrier crossing check is a simple AABB test, not a creepage/clearance calculation.
- PSU component heights are lumped into a 30 mm envelope; the BLX-A cover swing and fuse service access under the relay shelf are not modeled.

## Interpretation
- A `PASS` is not a safety or manufacturing release.
- Only the confirmed 220 x 120 x 70 preset is generated; 150 x 100 and 180 x 120 are rejected.
- Physical fit requires measured samples, tolerance stack, cable bend, and assembly trial.

## PCB change impact (2026-11-25)
- PSU board outline (50 x 65 mm) and mounting holes H1/H3/H4 are unchanged; `psu_bracket` and the three enclosure bosses do not need to move.
- Carrier outline (100 x 70 mm) and its four mounting holes are unchanged; carrier bosses do not need to move.
- HLK body shifted 1.5 mm in board Y; still inside the 50 x 65 mm PSU envelope and below the 30 mm component envelope. No body/lid change.
- BLX-A fuse holder: closed height worst-case 18 mm above the board (board top ~11.6 mm -> top ~29.6 mm). Relay shelf bottom is z=40.0, so closed clearance is ~10.4 mm. The cover swing is NOT modeled and the holder sits under the relay shelf (x 93.75..104.25, y -14.75..8.25). Treat fuse service access as `REVIEW REQUIRED`; measure the sample and add a shelf cutout or relocate the holder if the cover cannot open.
- TCO (x 94.5..104.5, y -21..-16) is mostly outside the relay shelf; MOV (x 80.5..93, y -16.65..-11.15) is partly under it. Their heights (~5 mm and ~12 mm) are below the shelf; no collision, but sample dimensions are unverified.
- KF129 terminal body height (~10 mm) stays below the shelf; TB1 wire entry at y~11.6 is at the shelf edge. Check cable bend/strain relief.
- Carrier additions C4, JP1, TP1/TP2/TP4/TP5 are low-profile and inside the existing carrier envelope. JP1 is accessible with the lid off; no panel feature is needed.
- Enclosure body, lid, socket, gland, barrier, and gasket are unchanged by the PCB edits. No STL/STEP regeneration was required for the PCB outline; the relay-shelf service question remains open.
