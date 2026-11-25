# REV_D_CORE_ONLY Mains-Entry PSU Board — 50 × 65 mm

**Status:** `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_FABRICATION`  
**Design revision:** `REV_D_CORE_ONLY`  
**Board:** 50 × 65 mm, 2-layer FR4 1.6 mm, **2 oz Cu target** (verify fab capability), **6 A provisional load path** (limited by BLX-A 6.3 A holder).  
**Toolchain:** KiCad 10.0.8 portable (`tools/kicad/bin`).

## What it is

A separate mains-entry board for the smart plug:

- TB1: 230 VAC L/N input, KF129-2P 5.08 mm terminal block (300 V/25 A claim, unverified).
- F1: 5×20 mm **6.3 A** 250 VAC time-lag fuse (Littelfuse 215-series claim) in a **BLX-A 6.3 A** PCB holder.
- MOV1: generic 10D271K, 275 VAC class, 10 mm, across L/N after the fuse.
- TF1: **generic 96 °C** one-shot, 10 A / 250 VAC (marked 96 °C, RFT 99 °C, holding 84 °C), in the L path after the MOV. **Not** SEFUSE SF96E; do not claim SF96E.
- PS1: HLK-5M05 5 V/1 A, 4-pin module.
- TB2: 230 VAC L/N output to the relay/load, KF129-2P.
- J5/J6/J7: 3× JST-XH 2-pin 5 V outputs.
- F2/D1: **1.0 A** PTC + SMBJ5.0A TVS on the total 5 V output.
- C1/C2: 100 µF + 100 nF at the 5 V output.

PE is **not** on this board. It is a dedicated chassis stud (plug PE → stud → socket PE), never switched or fused.

## Protection order

```
TB1 L → F1 → MOV1 (L-N) → TF1 → TB2 L + HLK AC L
TB1 N → TB2 N + HLK AC N + MOV1 N
HLK +Vo → F2 PTC → +5V → J5/J6/J7 + D1/C1/C2
HLK -Vo → GND
```

The TCO is in the L path after the MOV, so it removes both the load and the HLK input when it opens. The MOV is after the fuse so a failed MOV is cleared by F1.

## 5 V output allocation

| Output | Connector | Load | Status |
|---|---|---|---|
| OUT1 | J5 | Carrier J8 (SELV carrier) | `PROVISIONAL` |
| OUT2 | J6 | Relay module VCC | `PROVISIONAL` |
| OUT3 | J7 | PZEM V4 TTL 5 V | `PROVISIONAL`, conditional on PZEM batch/hipot (ADR-016) |

Total 5 V load estimate is ≤1 A; HLK is 1 A. Peak is not measured. Do not add loads without a new budget.

## Layout / safety notes

- 2 mm routed isolation notch at x=19..21, y=0..45; the HLK module bridges it.
- Mains leg on the right, SELV leg on the left. 2.5 mm mains traces;
  geometric copper mains-to-SELV minimum is 9.05 mm (audit file), L-N minimum
  1.3 mm. **These are not IEC creepage claims.**
- The HLK AC pins face the mains leg; DC pins face the SELV leg.
- The PSU board is mounted on 3 standoffs (H1/H3/H4) in the enclosure.
- The relay sits above the PSU board on a printed cantilever shelf; the relay is
  not on this PCB.
- The board is **not** a certified isolation barrier. HLK batch, creepage,
  hipot/leakage, fuse/MOV/TCO/terminal ratings, and thermal rise are unverified.

## Files

- `hardware/kicad/psu_rev_d.kicad_pcb` — routed board.
- `hardware/psu/netlist.csv` — every pad/net/position.
- `hardware/psu/placement.json` — placement.
- `hardware/psu/psu_schematic.svg/.png` — functional schematic.
- `hardware/manufacturing/provisional/psu/` — Gerber/drill/POS, not released.
- `reports/kicad/psu_drc.json` — DRC report.

## Digital verification

- DRC: **0 violations / 0 unconnected**.
- Board: 50.1 × 65.1 mm (edge bounding box including line width).
- 8 nets, 13 assembled footprints (plus 3 mounting holes and 3 fiducials).
- Static PSU crosscheck: `validation/PSU_CROSSCHECK.json`.

## Not proven

- Creepage/clearance to IEC 60664-1; working voltage/OVC/pollution degree.
- HLK batch isolation, certificate, ripple, thermal.
- Fuse/MOV/TCO/terminal/JST ratings and breaking capacity; BLX-A 6.3 A holder is the limiting part.
- 6 A thermal rise, 2 oz fabrication, solder mask/barrier.
- Assembly hipot/leakage, PE continuity, relay/socket/load tests.
- PZEM batch internal isolation and OUT3.

Do not energize this board from mains. Mains work is qualified-personnel/lab only.
