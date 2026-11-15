# Print Prototype Guide — Mechanical Only

**Status:** `PROTOTYPE_ONLY`
**Do not use this printed part with mains.** This guide is for checking fit, button access, OLED window, cable routing, and assembly order with **no power**.

## 1. Files

- `export/body_bottom_recommended.stl`
- `export/body_top_recommended.stl`
- `export/assembly_recommended.step` (viewer/CAD)
- `export/pzem_bracket.stl` / `pzem_bracket.step`
- `export/relay_module_bracket.stl` / `relay_module_bracket.step`
- `export/body_bottom_provisional.stl` / `body_top_provisional.stl` (comparison only; 150×100 fails fit with off-board modules)

## 2. Suggested FDM settings (prototype only)

| Setting | Value |
|---|---|
| Material | PETG or ABS (prototype; not certified) |
| Layer height | 0.20 mm |
| Walls | 3 perimeters (≥1.2 mm) |
| Infill | 20–30% |
| Supports | Tree supports for cutouts |
| Orientation | Bottom shell flat; top shell flat with supports in cavity |
| Post-processing | Remove supports, deburr holes, test insert fit |

## 3. Assembly check (no power)

1. Print both shells (confirmed 220×120×70) and both module brackets.
2. Install M3 heat-set inserts in the bottom bosses (temperature per insert datasheet).
3. Test-fit the carrier PCB, DevKitC-1 envelope, OLED, button, socket mock, PZEM on its bracket, and 2-channel relay module on its bracket.
4. Check the isolation barrier and cable pass-through.
5. Check the OLED window, button travel, RGB diffuser, and USB service cover.
6. Check cable gland thread and strain relief.
7. Record measurements and clashes; update `parameters.yaml` and re-run `enclosure.py`.

## 4. Stop conditions

Stop and redesign if:
- the carrier or module does not fit without force;
- the barrier is bypassed by a cable or module;
- the socket cannot be retained mechanically;
- the PE stud/terminal cannot be accessed;
- the USB cover can be opened while mains is connected;
- the enclosure material softens or deforms near the relay/PSU.

## 5. What this does not prove

- No electrical safety, dielectric strength, fire rating, IP rating, or thermal performance.
- No production tolerances or drop test.
- No certification.

**Next step:** engineer review of material/enclosure and a low-voltage mechanical fit trial.
