# Enclosure Material Review — REV_A_PROVISIONAL

**Status:** `BLOCKED` — material and enclosure not selected.
**Target:** ABS/PC flame-retardant, UL94 V-0, **220x120x70 mm recommended** (Q06 change pending confirmation). The 150x100 target fails fit and the 180x120 candidate fails real clearance with off-board PZEM + 2-channel relay.
**Important:** A 3D-printed enclosure is a mechanical prototype, not a certified electrical enclosure.

## 1. Requirements

| Requirement | Target | Evidence | Status |
|---|---|---|---|
| Flammability | UL94 V-0 (or better) | Material datasheet | `OPEN` |
| Impact resistance | Suitable for indoor handheld/plug-in use | Izod/Charpy data | `OPEN` |
| Thermal aging | 70 °C internal, long-term | Material datasheet + oven test | `OPEN` |
| Electrical insulation | Adequate for mains barrier | Comparative tracking index (CTI), thickness | `OPEN` |
| Wall thickness | ≥2.5 mm provisional | Mechanical calculation/test | `PROVISIONAL` |
| PE bonding | Dedicated metal stud, not plastic | Mechanical drawing + continuity test | `BLOCKED` |
| Cable strain relief | Gland + internal anchor | Pull test | `BLOCKED` |
| Service access | USB cover, fuse access | Mechanical design | `PROVISIONAL` |

## 2. Candidate materials

| Material | Pros | Cons | Status |
|---|---|---|---|
| ABS FR (UL94 V-0) | Common, machinable, flame-retardant grades | UV/aging, impact | Candidate |
| Polycarbonate FR (UL94 V-0) | Better impact/heat | Cost, molding | Candidate |
| PA66 FR | Tough, heat-resistant | Moisture, creep | Candidate |
| PLA/PETG 3D print | Prototype only | Not certified, low heat, flammable | **Prototype only** |
| Metal enclosure | Excellent fire/EMI | PE bonding, machining, cost, isolation | Candidate for lab, not selected |

## 3. 3D printing caveat

- FDM layer lines create paths for moisture/contamination and reduce dielectric strength.
- PLA softens at low temperature; PETG/ABS are not automatically flame-retardant.
- Printed threads/inserts can pull out; use heat-set inserts and test.
- Do not place a 3D-printed enclosure in a household mains installation.
- Do not claim IP rating or fire rating from a print.

## 4. Required review

1. Select a rated enclosure/material with datasheet.
2. Verify wall thickness, CTI, UL94, impact, and temperature rating.
3. Review PE stud/barrier integration.
4. Perform thermal aging and impact tests (lab).
5. Update CAD parameters and re-run fit check.
6. Engineer sign-off.

**Conclusion:** material/enclosure is a safety-critical blocker. `REV_A_PROVISIONAL` CAD is for fit study only.
