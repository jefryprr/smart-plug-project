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
- `export/relay_module_bracket.stl` / `relay_module_bracket.step`
- `export/psu_bracket.stl` / `psu_bracket.step`

## 2. Suggested FDM settings (prototype only)

| Setting | Value |
|---|---|
| Material | ABS/PC FR or PETG prototype; not certified |
| Layer height | 0.20 mm |
| Walls | 4 perimeters (>=1.6 mm) |
| Infill | 30–40% |
| Supports | Tree supports for socket, gland, vent, and USB cutouts |
| Orientation | Body flat on its back; lid top face up; gasket flat |
| Post-processing | Deburr holes, test heat-set inserts, check gasket compression |

## 3. Assembly check (no power)

1. Print the body, lid, gasket, USB cover, DevKit key, and module brackets.
2. Install 4× M3 heat-set inserts in the lid bosses; install module inserts/bosses as needed.
3. Test-fit the carrier (100×70), DevKitC-1 (two 1×22 rows, 22.86 mm), OLED, button, RGB pipe, PZEM on its bracket, relay module, HLK-5M05, fuse/MOV, terminals, CT, and Type F socket mock.
4. Verify the barrier, two grommet holes, 5 V/relay/PZEM cable routes, and bend radius.
5. Verify the button travel, onboard-RGB side window, and the front USB cover.
6. Verify the right-wall socket, M16 gland, and M12 vent threads.
7. Install the DevKit key and confirm it blocks a reversed board without touching the correct board.
8. Record measurements and clashes; update `parameters.yaml` and re-run `enclosure.py` and `render.py`.

## 4. Stop conditions

Stop and redesign if:
- the carrier or a module does not fit without force;
- the barrier is bypassed by a cable or module;
- the socket cannot be retained mechanically;
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
