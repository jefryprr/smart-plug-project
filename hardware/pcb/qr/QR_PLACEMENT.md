# QR Label Placement — SELV Carrier

**Label:** 22 × 22 mm, center `(25.0, 47.0)` mm, rectangle `x=14.0..36.0`, `y=36.0..58.0` mm.

**Layer:** `F.SilkS` outline only; printed label applied inside. No copper, no solder-mask opening, no netlist change.

## Clearance checks

- **PASS** — no pad center within 1.5 mm of the label.
- **PASS** — no via inside the label + 0.5 mm.
- **PASS** — all test points, fiducials, and mounting holes are outside the label + keepout.
- **PASS** — board-edge margin 12.00 mm ≥ 2.0 mm.
- **PASS** — DevKit socket row gap 3.14 mm (label starts below the sockets).

## Notes

- The board has 101 track segments; some may pass under the label. The label is non-conductive and no copper is removed or exposed.
- The label must not be placed on the PSU mains board. This placement is on the SELV carrier only.
- The label adhesive must be low-outgassing acrylic or silicone; operating temperature ≥ 85 °C.
- Apply the label after reflow/cleaning, not before. Do not cover test points or vias.
- Add the footprint at `(25.0, 47.0)` mm on `F.SilkS`; run DRC after adding. Do not add pads, copper, or solder-mask openings.

## Result

**PASS**
