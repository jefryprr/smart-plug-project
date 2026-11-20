# CORE_ONLY_SHOPEE Print Package

**Status:** `PROTOTYPE_ONLY` / `UNVERIFIED_DIMENSIONS` / `NOT_FOR_MAINS_USE`  
**Printer:** 300 × 300 mm bed or larger  
**Material:** ABS/PC flame-retardant target (UL94 V-0 not verified)  
**Model date:** 2026-11-20

## Files

| File | Qty | Notes |
|---|---:|---|
| `body_bottom_recommended.stl` | 1 | 220 × 120 × 60 mm; open-top up; supports for socket/gland/USB |
| `body_top_recommended.stl` | 1 | 220 × 120 × 10 mm; top face up |
| `gasket.stl` | 1 | 216 × 116 × 1 mm frame; cut silicone sheet alternative |
| `usb_cover.stl` | 1 | front service cover |
| `devkit_key.stl` | 1 | reverse-insertion key |
| `pzem_bracket.stl` | 1 | 37 × 80 × 2 mm, 4× M3, holes 65 × 23 |
| `psu_bracket.stl` | 1 | 50 × 65 × 2 mm, 3× M3 at board holes |
| `relay_shelf.stl` | 1 | 55 × 28 × 3 mm, 2× M3 to wall bosses |

Optional: `relay_module_bracket.stl` is not needed when the shelf is used.

## Print settings (starting point)

- 0.4 mm nozzle, 0.20 mm layers, 4–6 perimeters, 30–40% infill.
- Body: open-top up; tree supports for the socket, back-wall gland, and USB openings.
- Lid: top face up; counterbores print cleanly.
- Gasket: print in flexible material or cut from 1 mm silicone/EPDM sheet.
- No vent hole is present. Do not drill unless a vent is selected and reviewed.

## Hardware mapping

- **8× M3×5 heat-set inserts** (OD 4.2 mm): 4 lid bosses + 4 carrier bosses.
- **4× M3×16** lid screws.
- **13× M3×8**: 4 carrier + 3 PSU + 4 PZEM + 2 relay shelf.
- **4× M4×16** socket screws at 38 × 38 fixing. Verify length against the actual flange + 2.5 mm wall + 12 mm boss; if the screw bottoms out, use M4×12 or a washer.
- **1 set M4** PE screw/nut/star washer.
- Nylon standoffs M3×12 are **optional**; direct insert mounting is used.

## Socket warning

The DV DSMS-2P-16A is a **surface mounting socket**, not a panel-mount socket. This model uses a **round 45.6 mm cutout**, a 50 × 50 flange land, and 4× M4 bosses at 38 × 38. A **square** 45.6 cutout would remove the fixing bosses. The model also assumes the socket body is round/rounded and no larger than the 45.6 mm opening; a square 40 × 40 body will not pass. Confirm the actual socket body and depth before printing; if the body is square, the retention design must change.

## Assembly check (no power)

1. Test heat-set inserts in a scrap print; install 8 inserts.
2. Test-fit carrier, DevKitC-1 v1.0, PZEM, PSU board, relay shelf, button, socket, gland, gasket, USB cover.
3. Verify PE stud access, barrier, cable bend radius, and that no module forces the lid.
4. Verify the socket flange sits on the 50 × 50 land and the M4 screws engage the bosses.
5. Do not energize. This is a mechanical fit trial only.

## Not proven

- ABS/PC FR grade, UL94, layer adhesion, heat deflection, impact, IP/sealing.
- Socket/PZEM/relay dimensions (measure purchased samples).
- Creepage/clearance, PE continuity/fault current, hipot/leakage, thermal rise at 8 A.
- Certification or production readiness.

**Do not use this printed enclosure for 230 VAC until a competent engineer and lab approve it.**
