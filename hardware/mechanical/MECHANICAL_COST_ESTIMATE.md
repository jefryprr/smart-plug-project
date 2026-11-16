# Mechanical Cost Estimate — REV_C_PSU_BOARD

**Status:** `ESTIMATED` / not a supplier quote  
**Date:** 2026-11-16  
**Scope:** items added by the detailed enclosure (gasket, vent, printed cover/key, PSU bracket, thermal pad, label). Items already priced in `bom/BOM_PROCUREMENT.csv` are not double-counted.

| Item | Estimate (IDR) | Note |
|---|---:|---|
| Lid gasket, 1.0 mm silicone/EPDM, 216×116 frame | 5,000 | Cut from sheet; exact material/UL rating TBD |
| M12 ePTFE pressure vent, IP67 | 8,000 | Thermal/pressure equalisation; exact MPN TBD |
| 3D-printed PSU bracket | 3,000 | Filament/time share |
| 3D-printed USB service cover | 3,000 | Printed with gasket lip |
| 3D-printed DevKit reverse-insertion key | 2,000 | Printed bracket, 2× M3 |
| Thermal pad / barrier piece | 3,000 | Flame-retardant grade TBD |
| Safety/rating label | 2,000 | Already in electronics BOM as E-042; listed for completeness |
| Cable ties / anchors | 2,000 | PA66 |
| **Addendum total** | **28,000** | Excludes enclosure, socket, plug, gland, screws, inserts, PZEM/relay brackets already in the electronics BOM |

## Budget impact

- Electronics CORE: **Rp717,087** (Rp757,087 all-in) — includes PTC/TVS.
- Addendum: **~Rp28,000**.
- CORE with addendum: **~Rp731,297** (Rp771,297 all-in) at marketplace prices.
- CORE with EasyWare restock + addendum: **~Rp679,829** (Rp719,829 all-in).
- FULL electronics: **Rp820,897** (Rp860,897 all-in); addendum applies once.

The marketplace CORE + addendum is about **Rp21,000 over** the Rp750,000 cap. Do not delete the gasket, vent, key, or PE hardware to fit the cap. Options: wait for EasyWare restock, source a local enclosure at a lower price, or accept the overage.

## Status

All prices are estimates, not quotes. The gasket material, vent IP rating, thermal pad flame rating, and printed-part strength are `UNVERIFIED`. Physical fit, thermal, and sealing tests are still required.
