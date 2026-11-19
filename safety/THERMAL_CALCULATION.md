# Thermal Calculation — REV_D_CORE_ONLY (First-Order, Not a Test)

**Status:** `ENGINEERING_ESTIMATE` / `THERMAL_TEST_REQUIRED`  
**Date:** 2026-11-16  
**Enclosure:** 220 × 120 × 70 mm, 60 mm body + 10 mm lid, ABS/PC FR target, M12 ePTFE vent.

## 1. Assumptions

- Load: **8 A / ~1.840 W**, electronics/SMPS only.
- Ambient: **40 °C** inside a shelf/cabinet; still air.
- Relay contact resistance: **50 mΩ per channel**, two channels carry 8 A.
- Fuse/holder + terminals/wiring: **2.5 W** combined.
- PZEM: **1.0 W**.
- HLK-5M05: **2.1 W** (70% efficiency at 5 W).
- Carrier/ESP32/OLED/RTC: **1.0 W**.
- No forced air; no credit for the M12 vent in the base calculation.
- Enclosure surface area (all six faces, approximate):
  `2 × (0.220×0.120 + 0.220×0.070 + 0.120×0.070) = 0.1004 m²`.

## 2. Base case

| Loss source | Estimate |
|---|---:|
| Relay contacts (2 × 8² × 0.050) | 6.4 W |
| Fuse/holder + terminals/wiring | 2.5 W |
| PZEM | 1.0 W |
| HLK-5M05 | 2.1 W |
| Carrier/ESP32/UI | 1.0 W |
| **Total** | **13.0 W** |

Effective natural-convection + radiation coefficient: **7 W/m²K** (assumption for a closed plastic box; not measured).

`ΔT = 13.0 / (0.1004 × 7) ≈ 18.5 K` → internal air ≈ **58.5 °C** at 40 °C ambient.

## 3. Worst-case contact resistance

If each relay channel is **100 mΩ**:

- Relay loss = 2 × 64 × 0.100 = **12.8 W**
- Total ≈ **19.4 W**
- `ΔT ≈ 27.6 K` → internal air ≈ **67.6 °C**.

Hotspots at the relay contacts, fuse clips, and terminals will be higher than the air average. TF1 is a SEFUSE SF96E one-shot: rated functioning temperature 99 °C, holding temperature 84 °C, 10 A / 250 VAC. Normal-operation hotspot temperature must stay below 84 °C with margin; if the 8 A test shows >84 °C at the TCO, relocate/derate before release. The TCO is a backup, not a control.

## 4. Vent and material

- The M12 ePTFE vent is intended for pressure equalisation and limited moisture exchange, not as a guaranteed airflow path. It is **not credited** above.
- ABS/PC FR is a target; actual material, CTI, and UL94 rating are unverified.
- A metal enclosure or an internal aluminum spreader would reduce hotspots, but is not selected.

## 5. Acceptance criteria (for the future lab test)

1. Closed enclosure, 8 A resistive/electronics load, ambient 40 °C.
2. Measure relay body/contacts, fuse holder, terminals, PZEM, HLK case, enclosure air, and lid.
3. Record steady-state after at least 60 minutes.
4. Pass only if all touchable surfaces and component ratings are respected and the TCO is not approached in normal operation.
5. If any hotspot is excessive, derate, add a spreader/vent, or change enclosure material. Do not remove the TCO/fuse.

## 5A. REV_D_CORE_ONLY PSU board

- The PSU board carries the full 8 A L/N path through TB1, F1, TCO, TB2, and 4 mm traces (2 oz target).
- HLK-5M05 adds ~2.1 W at 5 W output; fuse holder, terminals, and TCO add contact/joint losses.
- The 2 mm isolation notch and 4 mm traces are **not** a thermal rating. The board must be tested at 8 A in the closed enclosure.
- The TCO is in the L path after the MOV; it must sense the HLK/terminal/PCB hotspot, not only air.
- The relay is above the PSU board on a printed shelf; its contacts are a separate hotspot.
- Add PSU board hotspots to the 8 A test: TB1, F1 clips, TCO body, TB2, HLK case, L/N traces.

## 6. Status

`UNVERIFIED`. This calculation is a design aid, not a thermal test or a safety approval.
