# Mechanical BOM Fit Verification — CORE_ONLY_SHOPEE

**Date:** 2026-11-20  
**Source BOM:** `bom/CORE_ONLY_SHOPEE_SHOPPING_LIST.csv`  
**Design:** `hardware/mechanical/parameters.yaml`, `source/enclosure.py`  
**Status:** `PROTOTYPE_ONLY` / `UNVERIFIED_DIMENSIONS` / `NOT_FOR_MAINS_USE`

## 1. Findings that changed the model

| Item | Old model | Shopping-list item | Action |
|---|---|---|---|
| Socket | 35×45×45 body, 45×45 square cutout, Mennekes assumption | DV DSMS-2P-16A, surface socket, flange 50×50, fixing 38×38, depth ~44–55, user cutout 45.6 | Body envelope 40×40×45; flange land 50×50; **round 45.6 cutout**; 4× M4 bosses at 38×38. A square 45.6 cutout would remove the fixing bosses. **Confirm before print.** |
| PZEM | 53×89×24, bracket 58×94 | PZEM-004T V4 PCB ~74×31×18 | Body 31×74×18; bracket 37×80, holes 65×23; bosses at x=16.5/39.5, y=±32.5. |
| PE stud | 3.2 mm hole, 8 mm boss | M4×16 screw, M4 nut/ring | Hole 4.3 mm; boss 10 mm; height 14.5 mm; moved to x=45,y=50. |
| Heat-set inserts | 2.5 mm pilot, no insert hole | 8× M3×5, OD 4.2 | 4 lid + 4 carrier bosses with 4.2×5.5 holes. Nylon standoffs not required. |
| Gasket | floating frame, no land | 1 mm silicone sheet, 216×116 | Flat gasket land on body rim + 5 mm lid ring; **no groove**; leak test required. |
| Vent | 12 mm through-hole | M12 vent not purchased (row 33) | No vent hole; no blind knockout in final model. Thermal/IP review open. |
| Gland | right wall y=10,z=18, 16.0 hole | M16 IP68 gland | Back wall x=20,z=18; 16.3 hole; 22 mm boss; clear of PE boss and socket/PSU. |
| PSU bracket | 38×23 HLK plate | PSU board 50×65, 3 holes | New 50×65×2 plate with holes at board (3,3),(47,3),(16,42); 3× M3×8. |
| Relay shelf | legs through right wall | 55×28×3 shelf | Plate at z=40–43; 2 internal wall bosses; 2× M3×8; no through-wall holes. |
| Print bed | 220×220 assumed | 300×300 selected | Body 220×120×60 and lid 220×120×10 fit with margin. |

## 2. Hardware count mapping

| Hardware | Qty | Use |
|---|---:|---|
| M3×5 heat-set inserts | 8 | 4 lid + 4 carrier |
| M3×16 lid screws | 4 | Lid |
| M3×8 module screws | **13** | 4 carrier + 3 PSU + 4 PZEM + 2 relay shelf |
| M4×16 socket screws | 4 | DV socket flange 38×38 |
| M4 PE screw/nut/ring | 1 set | PE stud |
| Nylon standoffs M3×12 | 0 | Optional/spare; direct insert mounting |
| M12 vent | 0 | Not fitted |

The shopping list has 2 packs of 10 M3×8 (20 pcs); 13 used leaves spares.

## 3. Geometry verification

- Body: 220×120×60 mm, watertight STL; fits 300×300 bed.
- Lid: 220×120×10 mm, watertight STL.
- Gasket: 216×116 outer, 206×106 inner, 1 mm.
- Fit report: **PASS (coarse AABB)**, 13 modules.
- No vent hole; no through-wall relay-shelf holes.
- Gland-hole vs PE-boss overlap: **0.0 mm³** (CadQuery intersection check in `verify_bom_fit.py`). The gland is at x=20 on the back wall, clear of the PE boss at x=45,y=50.
- Socket cutout: round 45.6 mm; 4 M4 bosses at 38×38; 50×50 flange land.
- PE: M4 clearance; no PE switching/fuse.

## 4. Open items / do not claim safe

- **Socket cutout shape must be confirmed.** User wrote 45.6×45.6; model uses round 45.6 because square removes the 38×38 fixing bosses. The model also assumes the socket body is round/rounded and no larger than the 45.6 round opening. A square 40×40 body will **not** pass through that round hole. Measure the body cross-section and depth on the received part. If the body is square, use an outside mounting plinth or a different retention design.
- Actual socket depth 44–55 mm, PZEM PCB, relay module, and DV socket dimensions must be measured on the received parts.
- M4×16 socket screw length must be checked against the actual flange thickness + 2.5 mm wall + 12 mm boss. If it bottoms out, use M4×12 or a washer; do not leave a sharp screw tip inside the enclosure.
- ABS/PC FR grade, UL94 certificate, wall thickness, layer adhesion, and heat deflection are unverified.
- Gasket compression/leak, IP rating, impact, thermal rise, creepage/clearance, PE continuity/fault current, hipot/leakage are all unverified.
- The printed enclosure is **not** a certified electrical enclosure. Do not energize 230 VAC without engineer review and lab tests.
- No claim of `READY_FOR_FABRICATION` or `READY_FOR_USE`.
