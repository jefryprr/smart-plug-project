# Mechanical Cost Estimate — REV_D_CORE_ONLY / CORE_ONLY_SHOPEE

**Status:** `ESTIMATED` / not a supplier quote  
**Date:** 2026-11-20  
**Scope:** items added by the enclosure (gasket, printed cover/key, PSU/PZEM/relay brackets, thermal pad, label). Items already priced in `bom/BOM_PROCUREMENT.csv` are not double-counted. The M12 vent is deferred and is **not** included.

| Item | Estimate (IDR) | Note |
|---|---:|---|
| Lid gasket, 1.0 mm silicone/EPDM, 216 x 116 frame | 5,000 | Cut from sheet; exact material/UL rating TBD |
| 3D-printed PSU bracket 50 x 65 | 3,000 | Filament/time share |
| 3D-printed PZEM bracket 37 x 80 | 3,000 | Filament/time share |
| 3D-printed relay shelf 55 x 28 | 4,000 | Filament/time share |
| 3D-printed USB service cover | 3,000 | Printed with gasket lip |
| 3D-printed DevKit reverse-insertion key | 2,000 | Printed bracket, 2x M3 |
| M4 x 16 socket screws (4 pcs) | 4,000 | Estimated; not a quote |
| Thermal pad / barrier piece | 3,000 | Flame-retardant grade TBD |
| Safety/rating label | 2,000 | Already in electronics BOM as E-042; listed for completeness |
| Cable ties / anchors | 2,000 | PA66 |
| **Addendum total** | **31,000** | Excludes enclosure, socket, plug, gland, screws, inserts |

## Budget impact

- Electronics CORE: **Rp754,016** (Rp794,016 all-in with Rp40,000 shipping).
- Addendum: **Rp31,000**.
- CORE + addendum: **Rp785,016 / Rp825,016 all-in** at marketplace prices.
- CORE restock + addendum: **Rp733,548 / Rp773,548 all-in** (above the Rp750,000 cap).
- CORE restock without addendum: **Rp702,548 / Rp742,548 all-in** (under the cap).
- FULL UI: **DEFERRED**; not part of the active budget.

The marketplace CORE and the restock + addendum are above the Rp750,000 cap; restock without the addendum is under it. Do not delete the gasket, key, PE hardware, or safety parts to fit the cap. The enclosure is 3D-printed; filament/print time is not included in the addendum.

## Status

All prices are estimates, not quotes. The gasket material, thermal pad flame rating, and printed-part strength are `UNVERIFIED`. No vent is fitted. Physical fit, thermal, and sealing tests are still required.
