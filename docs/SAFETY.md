# Safety Overview

**Design revision:** `REV_C_PSU_BOARD`  
**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW` / `HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_FABRICATION`

> [!DANGER]
> **Do not connect this prototype to 230 VAC.** No physical assembly has been built, energized, or tested. Mains work is only for qualified personnel under a lab procedure. This page is a summary, not an approval or an energization guide.

---

## 1. The two domains

| Domain | What is in it | Rule |
|---|---|---|
| **MAINS** | Plug, fuse, MOV, TCO, PSU input, PZEM voltage terminals, relay contacts, socket | Hazardous. Assume live. |
| **SELV** | 5 V/3.3 V carrier, ESP32, OLED, RTC, button, RGB, relay coil driver | Designed to be separated from mains, but the assembly is **not proven safe**. |

Mixing the two without a verified barrier can put mains potential on the ESP32, USB, or enclosure. That is the central hazard of this project.

---

## 2. Protection chain

```text
Plug L -> F1 10 A fuse -> MOV1 275 VAC -> TF1 99 °C TCO -> relay/load + HLK-5M05
Plug N -> relay/load + HLK-5M05 + MOV1
Plug PE -> dedicated chassis stud -> socket PE
```

- **Fuse** clears overcurrent and a failed MOV.
- **MOV** clamps mains surges.
- **TCO** is a one-shot 99 °C thermal cutoff in the L path. It is not a current fuse.
- **PE** is continuous and is never switched, fused, or routed through a relay.
- **HLK-5M05** provides the 5 V rail; its isolation is a datasheet claim, not a batch certificate.

The protection order is documented in [`../safety/PROTECTION_COORDINATION.md`](../safety/PROTECTION_COORDINATION.md). It is not a substitute for a protection coordination study.

---

## 3. Isolation

| Barrier | Design | Status |
|---|---|---|
| PSU AC/DC | HLK-5M05, 2500 VAC datasheet claim | `DOCUMENTATION_DEFICIENT` |
| PZEM UART | PZEM-004T V4 internal optocouplers | `PROVISIONAL`; batch/hipot unverified |
| Relay coil/contact | Off-board optocoupler module | `DOCUMENTATION_DEFICIENT`; shared VCC/GND means not a certified galvanic barrier |
| PCB creepage/clearance | 2 mm isolation notch, 4 mm L/N traces, 6–12 mm provisional spacing | `UNVERIFIED`; not an IEC 60664-1 calculation |
| Enclosure | Mechanical barrier at x = −4 mm | Digital only; material/flame/impact unverified |

The external **ADuM1201 + B0505S** barrier is not fitted in REV_C. It remains a documented fallback if the PZEM batch fails inspection/hipot. See [`../docs/decisions/ADR-016-PZEM-ISOLATION-REV-C.md`](decisions/ADR-016-PZEM-ISOLATION-REV-C.md).

---

## 4. Thermal

- HLK-5M05 dissipates roughly **2.1 W** at 5 W output / 70% efficiency.
- TCO SF96E has a 99 °C rated functioning temperature and **84 °C holding temperature**.
- The 8 A path includes terminals, fuse clips, TCO, traces, and the relay contacts.
- The enclosure is 3D-printed; flame rating and thermal behavior are unverified.

No 8 A thermal test has been performed. The design must keep the TCO hotspot below 84 °C with margin in the closed enclosure.

---

## 5. USB and service

- Do not connect USB while mains is present.
- The service cover and USB opening are design features, not proof of safety.
- Do not use an oscilloscope, logic analyzer, or USB cable that bridges the mains and SELV domains.
- Only qualified personnel with an isolation transformer/differential probe and a lab procedure may probe the mains side.

---

## 6. What is still blocked

- Working voltage, overvoltage category, pollution degree, material group, altitude.
- Creepage/clearance to IEC 60664-1.
- Hipot, insulation resistance, leakage current.
- PE continuity and fault-current.
- Thermal 8 A, fuse/MOV/TCO coordination, relay lifecycle.
- Enclosure flammability, impact, sealing, IP.
- Firmware flash, boot waveform, PZEM/relay integration.
- Regulatory/SNI/CE/UL review.

See [`../reports/FAILURES.md`](../reports/FAILURES.md) and [`../safety/RESIDUAL_RISK_REGISTER.csv`](../safety/RESIDUAL_RISK_REGISTER.csv).

---

## 7. Non-negotiable rules

1. Do not energize this prototype from mains.
2. Do not work on mains alone.
3. Do not disconnect or switch PE.
4. Do not treat a mock/simulator as a physical test.
5. Do not print a rating label or certification mark.
6. Do not send provisional Gerber files to a fab as a functional board.
7. Do not put real secrets, tokens, or private keys in the repo.

---

## 8. Related documents

- [`../safety/ISOLATION_PLAN.md`](../safety/ISOLATION_PLAN.md)
- [`../safety/PROTECTION_COORDINATION.md`](../safety/PROTECTION_COORDINATION.md)
- [`../safety/CLEARANCE_CREEPAGE_WORKSHEET.md`](../safety/CLEARANCE_CREEPAGE_WORKSHEET.md)
- [`../safety/THERMAL_CALCULATION.md`](../safety/THERMAL_CALCULATION.md)
- [`../safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md`](../safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md)
- [`../safety/POLARITY_AND_EARTH_ASSESSMENT.md`](../safety/POLARITY_AND_EARTH_ASSESSMENT.md)
- [`../safety/REGULATORY_PLAN_INDONESIA.md`](../safety/REGULATORY_PLAN_INDONESIA.md)
- [`../safety/REVIEW_SIGNOFF_TEMPLATE.md`](../safety/REVIEW_SIGNOFF_TEMPLATE.md)
