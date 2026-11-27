# QR Scan & Placement Test Report

**Date:** 2026-11-27  
**Label:** `hardware/pcb/qr/pcb_label_22mm.pdf` (22.00 × 22.00 mm)  
**Payload:** `https://github.com/jefryprr/smart-plug-project/blob/main/hardware/schematic/SYSTEM_SCHEMATIC.pdf`  
**QR:** version 6, 41 × 41 modules, ECC M, module size ≈ 0.329 mm, quiet zone ≥ 4 modules.

## 1. Scan test — PDF (print path)

Decoder: `zxing-cpp` 3.2.0. Each page rendered from the PDF at the stated DPI, no manual enhancement.

| DPI | Pixels | Result |
|---:|---:|---|
| 600 | 520×520 | PASS |
| 400 | 347×347 | PASS |
| 350 | 304×304 | PASS |
| 320 | 278×278 | PASS |
| 300 | 260×260 | PASS |
| 280 | 243×243 | PASS |
| 260 | 226×226 | PASS |
| 240 | 208×208 | PASS |
| 220 | 191×191 | PASS |
| 200 | 174×174 | PASS |
| 180 | 156×156 | PASS |
| 160 | 139×139 | PASS |

**Result: PASS at 160–600 dpi.**

OpenCV `QRCodeDetector` was also used on the 1200 dpi PNG: PASS at 200–1200 dpi for 0°/90°/180°/270°. OpenCV had one sampling artifact at exactly 300 dpi on the PDF raster; zxing-cpp decoded the same 300 dpi image correctly. This is a decoder artifact, not a label defect.

## 2. Placement check

Command: `python hardware/pcb/qr/verify_qr_placement.py`

- Label rectangle: `x=14..36 mm`, `y=36..58 mm`; center `(25,47) mm`.
- No pad center within 1.5 mm: **PASS**
- No via inside label + 0.5 mm: **PASS**
- No test point/fiducial/mounting hole inside keepout: **PASS**
- Board-edge margin: 12.00 mm: **PASS**
- DevKit socket row gap: 3.14 mm: **PASS**

**Result: PASS.**

## 3. Footprint check

- `kicad-cli fp export svg` successfully parsed and exported `SCHEMATIC_QR_22MM.kicad_mod`.
- Footprint has **no pads, no copper, no solder-mask openings**.
- Only `F.SilkS` outline and `F.CrtYd` courtyard.

## 4. PCB integrity

- **No change** was made to `hardware/kicad/smartplug.kicad_pcb`.
- No copper, pad, via, netlist, or solder-mask change.
- The label is a non-conductive printed sticker; it may cover low-voltage traces and the `BUTTON` silk text. That does not break connectivity.
- If the footprint is added in KiCad, run DRC and confirm no silk-over-pad violation before fabrication.

## 5. Limitations

- URL is not live until `SYSTEM_SCHEMATIC.pdf` is committed and pushed to `main`.
- Physical adhesion, chemical compatibility, UV/abrasion, and RF effects were not tested.
- The label is on the SELV carrier inside the enclosure; scanning requires mains OFF and the enclosure open.
- For scanning without opening the enclosure, apply a **duplicate label on the outside of the enclosure**; do not rely on the internal PCB label alone.

## Result

**QR DESIGN/TEST PASS; PHYSICAL LABEL APPLICATION NOT YET PERFORMED.**
