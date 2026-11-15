# Fit Analysis — REV_B_NO_TEMP

**Status:** coarse digital fit check only. Dimensions are approximate; no physical fit validation.

## Preset: provisional

- Status: **FAIL**
- Modules checked: 12
- Enclosure internal bounds (mm): (-72.5, -47.5, 2.5, 72.5, 47.5, 67.5)
- AABB clashes:
  - relay ↔ fuse
  - relay ↔ terminals
- Barrier crossings:
  - carrier: (-70.0, -25.0, 7.2, 10.0, 25.0, 8.8)
  - esp32: (-64.3, -12.7, 8.0, 4.299999999999997, 12.7, 18.0)

## Preset: recommended

- Status: **PASS**
- Modules checked: 12
- Enclosure internal bounds (mm): (-107.5, -57.5, 2.5, 107.5, 57.5, 67.5)

## Limitations
- All module dimensions are approximate envelopes, not measured samples.
- No tolerance stack, cable bend, or thermal expansion is modeled.
- A PASS here is only a coarse digital fit check; it is not a mechanical validation.
- Barrier crossing check is a simple AABB test, not a creepage/clearance calculation.

## Interpretation
- A `PASS` is not a safety or manufacturing release.
- The 150×100×70 and 180×120×70 presets fail clearance review; 220×120×70 is confirmed (Q06=C, 2026-11-15). Physical fit is still unverified.
- Physical fit requires measured samples, tolerance stack, cable bend, and assembly trial.
