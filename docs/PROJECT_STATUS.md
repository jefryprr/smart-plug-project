# Project Status

**Design revision:** `REV_D_CORE_ONLY`  
**Last digital validation:** 2026-11-16  
**Overall:** `PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`  
**Fabrication:** `NOT_RELEASED`  
**Ready for use:** **NO**

This page is the honest scoreboard. It separates what was actually executed from what still needs hardware, a lab, an engineer, or a deployment environment.

---

## 1. Digital validation gate

Source: [`reports/VALIDATION_SUMMARY.json`](../reports/VALIDATION_SUMMARY.json), [`reports/TEST_MATRIX.csv`](../reports/TEST_MATRIX.csv), [`reports/FAILURES.md`](../reports/FAILURES.md).

| Result | Count |
|---|---:|
| PASS | 27 |
| BLOCKED | 11 |
| FAIL | 0 |

`PASS` means the specific command ran and exited successfully. It does **not** prove physical safety, isolation, thermal performance, or product readiness.

---

## 2. What is verified digitally

| Area | Evidence | Status |
|---|---|---|
| Domain rules | 34 Vitest tests — commands, energy, tariffs, schedules, freshness, redaction | PASS |
| MQTT contract | 12 tests — topics, schemas, ACL direction, fixtures | PASS |
| API + simulator | 43 API tests + 6 simulator tests — auth, RBAC, commands, ACK, telemetry, events, analytics, diagnostics, time | PASS |
| Simulator | 4 tests | PASS |
| Firmware core | 75 C host checks with Zig cc | PASS |
| Firmware target build | ESP-IDF v6.1, esp32s3, 192,496-byte `.bin` | PASS (build only) |
| Web | Next.js production build + 5 Playwright tests + axe checks | PASS |
| Static wiring/GPIO/BOM | Python crosschecks | PASS |
| WireViz | 2 harnesses rendered to SVG/PNG/PDF | PASS |
| KiCad block schematic | ERC 0 violations | PASS (block scope) |
| SELV carrier PCB | Routed 100 × 70 mm CORE-only, 19 footprints (16 assembled + 3 fiducials), 11 named nets, DRC 0/0 | PASS (digital) |
| PSU PCB | Routed 50 × 65 mm, 8 nets, DRC 0/0, 4 mm L/N traces, 2 mm isolation notch | PASS (digital) |
| Gerber/drill/POS | Exported for both boards | PROVISIONAL |
| CadQuery enclosure | 220 × 120 × 70 mm STEP/STL, brackets, gasket, USB cover, DevKit key | PASS (digital fit) |
| Android debug APK | arm64-v8a, 46,852,340 bytes, v2 debug signature verified | PASS (debug, not installed) |
| npm audit | 0 known npm vulnerabilities at the recorded date | PASS |

---

## 3. What is blocked or unverified

| Area | Why blocked | What would unblock it |
|---|---|---|
| Component-level schematic/footprint review | No vendor footprint review or engineer sign-off | Engineer review, approved MPNs/footprints, full ERC |
| Mains isolation/creepage/clearance | Working voltage, OVC, PD, material group, altitude, coating not finalized | Licensed standard + engineer worksheet + physical creepage check |
| Hipot/insulation resistance/leakage | No lab/hardware | Qualified lab test |
| PE continuity/fault current | No hardware/lab | PE bond hardware + continuity/fault test |
| Thermal 8 A / fuse / TCO / HLK | No closed-enclosure thermal test | Thermal chamber/thermocouples at 8 A |
| Load/inrush/relay lifecycle | No hardware/lab | Load bank + relay lifecycle test |
| Physical fit/sealing/impact/IP | No printed enclosure | Print, assemble, measure, seal, impact test |
| Firmware flash/boot waveform | No board/scope | Verified DevKitC-1 + flash + logic analyzer/scope |
| PZEM/Wi-Fi/MQTT/OTA/time integration | No hardware integration; no OLED/RTC by design | Bench test with real modules |
| Android device/emulator test | APK not installed | Install/test on emulator/device; production signing |
| PostgreSQL migration/deployment | PostgreSQL/Docker not installed | Implement adapter, run migrations, deploy |
| MQTT TLS/ACL production | Not deployed/tested | Broker TLS, password file, ACL, negative tests |
| Full system HIL | No hardware/lab | HIL fixture and qualified lab |
| Regulatory/SNI/CE/UL | No classification or certification | Regulatory consultant + lab + certification |

---

## 4. Status legend

| Status | Meaning |
|---|---|
| `PASS` | The specific check ran and passed. Digital unless explicitly stated. |
| `FAIL` | The check ran and failed. |
| `BLOCKED` | The check cannot run yet (no hardware, lab, tool, or approval). |
| `UNVERIFIED` | A value or claim has not been checked. |
| `PROVISIONAL` | A design choice exists but may change after review/test. |
| `DIGITAL_COMPLETE` | Digital artifacts exist; no physical validation. |
| `ENGINEERING_REVIEW_REQUIRED` | A competent engineer must review before fabrication/use. |
| `HARDWARE_VALIDATION_REQUIRED` | Physical lab tests are still required. |
| `READY_FOR_FABRICATION` | Release gate F4. Not used. |
| `READY_FOR_USE` | Actual-use release. Not used. |

---

## 5. Current blockers to fabrication

1. No approved component MPNs/footprints.
2. No component-level production schematic.
3. No engineer sign-off on isolation, creepage, PE, or protection coordination.
4. No hipot/leakage/PE/thermal/load evidence.
5. HLK-5M05 batch certificate/isolation/thermal unverified.
6. PZEM V4 batch internal isolation unverified (`OUT3` conditional).
7. Relay module batch/rating/active-LOW/weld behavior unverified.
8. Enclosure material/flame rating/impact/IP unverified.
9. No physical fit or cable-bend test.
10. No firmware flash/integration test.

Do not send the provisional Gerber files to a PCB manufacturer as a functional board. Do not energize the prototype from mains.

---

## 6. What would move the project forward

| Gate | Deliverable |
|---|---|
| F1 — Component approval | Approved MPNs, batch certificates, footprint review |
| F2 — Schematic/layout review | Component-level ERC/DRC, creepage/clearance worksheet, engineer sign-off |
| F3 — Digital build/test | Reproducible build, test matrix, traceability |
| F4 — Fabrication release | Only after F1–F3; currently **not passed** |
| F5 — Bench low-voltage | Flash firmware, verify rails, UART, relay driver, UI |
| F6 — Lab mains/thermal | Hipot, leakage, PE, 8 A thermal, inrush, relay lifecycle |
| F7 — Pilot | Enclosure, EMC, regulatory review, field trial |
| F8 — Production | Certification, manufacturing test, traceability, support |

The project is at the transition between **F3 digital** and **F4 fabrication review**. It is not at F4.

---

## 7. Related documents

- [`../reports/FAILURES.md`](../reports/FAILURES.md)
- [`../reports/TEST_MATRIX.csv`](../reports/TEST_MATRIX.csv)
- [`../deliverables/FINAL_ENGINEERING_REPORT.md`](../deliverables/FINAL_ENGINEERING_REPORT.md)
- [`../deliverables/manifest.json`](../deliverables/manifest.json)
- [`../safety/RESIDUAL_RISK_REGISTER.csv`](../safety/RESIDUAL_RISK_REGISTER.csv)
- [`../requirements/traceability.yaml`](../requirements/traceability.yaml)
