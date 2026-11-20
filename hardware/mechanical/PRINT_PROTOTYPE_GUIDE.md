# Print Prototype Guide — Mechanical Only (REV_D_CORE_ONLY)

**Status:** `PROTOTYPE_ONLY`  
**Do not use this printed part with mains.** This guide is for checking fit, button access, onboard-RGB window, cable routing, gasket, and assembly order with **no power**. OLED/RTC/external RGB are deferred and not fitted.

## 1. Files

- `export/body_bottom_recommended.stl`
- `export/body_top_recommended.stl`
- `export/gasket.stl`
- `export/usb_cover.stl`
- `export/devkit_key.stl`
- `export/assembly_recommended.step` (viewer/CAD)
- `export/pzem_bracket.stl` / `pzem_bracket.step`
- `export/relay_shelf.stl` / `relay_shelf.step`
- `export/relay_module_bracket.stl` / `relay_module_bracket.step` (optional; not needed when the shelf is used)
- `export/psu_bracket.stl` / `psu_bracket.step`

## 2. Suggested FDM settings (prototype only)

| Setting | Value |
|---|---|
| Material | ABS/PC FR (selected); not certified |
| Layer height | 0.20 mm |
| Walls | 4-6 perimeters (>=1.6 mm; 2.5 mm wall) |
| Infill | 30–40% |
| Supports | Tree supports for socket, back-wall gland, and USB openings; no vent hole |
| Orientation | Body open-top up on 300×300 bed; lid top face up; gasket flat |
| Post-processing | Deburr holes, test heat-set inserts, check gasket compression |

## 3. Assembly check (no power)

1. Print the body, lid, gasket, USB cover, DevKit key, and module brackets.
2. Install 8× M3×5 heat-set inserts: 4 lid bosses, 4 carrier bosses. PSU/PZEM/relay bosses use M3×8 self-tapping screws.
3. Test-fit the CORE-only carrier (100×70), DevKitC-1 v1.0 (two 1×22 rows, 22.86 mm), button, PZEM on its 37×80 bracket, relay module on the shelf, HLK-5M05/PSU board, fuse/MOV/TCO, terminals, CT, and DV DSMS-2P-16A socket.
4. Verify the barrier, two grommet holes, 5 V/relay/PZEM cable routes, and bend radius.
5. Verify the button travel, onboard-RGB side window, and the front USB cover.
6. Verify the round 45.6 mm socket cutout, 50×50 flange land, 38×38 M4 fixing, and the back-wall M16 gland. No M12 vent is present.
7. Install the DevKit key and confirm it blocks a reversed board without touching the correct board.
8. Record measurements and clashes; update `parameters.yaml` and re-run `enclosure.py` and `render.py`.

## 4. Stop conditions

Stop and redesign if:
- the carrier or a module does not fit without force;
- the barrier is bypassed by a cable or module;
- the socket flange/fixing does not match 38×38 or the round 45.6 cutout;
- the PE stud/terminal cannot be accessed;
- the USB cover can be opened while mains is connected;
- the DevKit key does not block reverse insertion or touches the correct board;
- the gasket does not compress evenly;
- the enclosure material softens or deforms near the relay/PSU.

## 5. What this does not prove

- No electrical safety, dielectric strength, fire rating, IP rating, or thermal performance.
- No production tolerances, drop test, or gasket leakage test.
- No certification.

**Next step:** engineer review of material/enclosure and a **low-voltage** mechanical fit trial.
