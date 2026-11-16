# Fit Analysis - REV_C_PSU_BOARD

**Status:** coarse digital fit check only. Dimensions are approximate; no physical fit validation.

## Preset: recommended (220 x 120 x 70)

- Status: **PASS**
- Modules checked: 15
- Enclosure internal bounds (mm): (-107.5, -57.5, 2.5, 107.5, 57.5, 67.5)

## Limitations
- All module dimensions are approximate envelopes, not measured samples.
- No tolerance stack, cable bend, or thermal expansion is modeled.
- A PASS here is only a coarse digital fit check; it is not a mechanical validation.
- Barrier crossing check is a simple AABB test, not a creepage/clearance calculation.

## Interpretation
- A `PASS` is not a safety or manufacturing release.
- Only the confirmed 220 x 120 x 70 preset is generated; 150 x 100 and 180 x 120 are rejected.
- Physical fit requires measured samples, tolerance stack, cable bend, and assembly trial.
