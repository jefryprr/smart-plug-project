# Fit Analysis — REV_A_PROVISIONAL

**Status:** coarse digital fit check only. Dimensions are approximate; no physical fit validation.

## Preset: provisional

- Status: **PASS**
- Modules checked: 12
- Enclosure internal bounds (mm): (-72.5, -47.5, 2.5, 72.5, 47.5, 67.5)

## Preset: recommended

- Status: **PASS**
- Modules checked: 12
- Enclosure internal bounds (mm): (-87.5, -57.5, 2.5, 87.5, 57.5, 67.5)

## Limitations
- All module dimensions are approximate envelopes, not measured samples.
- No tolerance stack, cable bend, or thermal expansion is modeled.
- A PASS here is only a coarse digital fit check; it is not a mechanical validation.
- Barrier crossing check is a simple AABB test, not a creepage/clearance calculation.

## Interpretation
- A `PASS` is not a safety or manufacturing release.
- If the 150×100×70 preset fails, use the `recommended` 180×120×70 preset after user approval (Q06=C).
- Physical fit requires measured samples, tolerance stack, cable bend, and assembly trial.
