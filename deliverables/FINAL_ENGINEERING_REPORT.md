# Final Engineering Report — ESP32-S3 IoT Smart Plug

**Date:** 15 November 2026
**Author/agent:** OpenCode (DeepSeek V4.1 Flash 1017)
**PRD version:** 1.0
**Design revision:** `REV_A_PROVISIONAL`
**Source commit:** `{{GIT_COMMIT}}`
**Manifest:** `deliverables/manifest.json`

---

## 1. Executive summary

This package is a **digital engineering prototype** of an inline ESP32-S3 smart
outlet. It includes research, BOM, safety analysis, native KiCad block/placement
files, WireViz harnesses, CadQuery enclosure, a portable firmware safety core,
backend API, MQTT contract, web dashboard, Android source, device simulator,
tests, and documentation.

**Digital status:** `PARTIAL_DIGITAL`
**Engineering status:** `ENGINEERING_REVIEW_REQUIRED`
**Hardware status:** `HARDWARE_VALIDATION_REQUIRED`
**Fabrication:** `NOT_RELEASED`
**Ready for use:** **NO**

The digital tests pass where executable (19 PASS / 15 BLOCKED / 0 FAIL), but
critical physical and toolchain gates remain blocked: KiCad ERC/DRC/Gerber,
ESP-IDF build, Android APK, PostgreSQL deployment, and all mains/thermal/PE/
isolation/load testing.

---

## 2. Problem and scope

A household user needs to measure and control a plug-in AC load, see energy/cost,
schedule/automate, and retain local control when the cloud is unavailable. The
system must never claim a physical OFF state without observation and must not
let software bypass a hard fault/lockout.

**Phase 1 scope:** hardware research/BOM, schematic/wiring/PCB/CAD, local firmware,
safety documents.
**Phase 2 scope:** MQTT/backend/database/web/Android/deployment.
**Out of scope:** consumer certification, legal metering, medical/life-critical
control, lab tests by an unqualified person.

---

## 3. User decisions and unresolved blockers

All 28 answers are in `docs/decisions/USER_ANSWERS.md/.yaml`.

Key decisions: inline outlet (Q01=B), target 10 A (Q03=B), mixed SMPS loads
(Q04=B), review two-pole (Q05=A), ≤150×100×70 mm (Q06=B), official DevKitC-1
N16R8 (Q08=B), PZEM comparison (Q09=D), relay study (Q10=C), lab prototype
(Q12=A), ESP-IDF (Q23=A), Expo (Q24=A), default OFF (Q25=C), computer-only lab
(Q26=A), digital parallel phases (Q27=C).

**Unresolved safety-critical blockers:**
- Socket/plug MPN/certification/PE (Q02).
- Relay 10 A DPST availability; provisional 8 A.
- PZEM V4 batch datasheet/isolation/pinout.
- PE hardware/enclosure material/clearance values.
- No hardware/lab/engineer/regulatory sign-off.

---

## 4. Research, components, approvals, datasheets

- `research/COMPONENT_RESEARCH.md`: 41 candidates with evidence scores.
- `research/candidates.csv`: all candidates, not just winners.
- `bom/BOM_MASTER.csv`: 46 rows, **unpriced**, **unapproved**.
- `bom/BOM_SUMMARY.json`: `UNPRICED`, no Rp0 placeholders.
- `bom/COMPONENT_APPROVALS.yaml`: no `approved_for_fabrication`.
- `research/datasheets/MANIFEST.md`: 9 PDFs hashed; PZEM/socket/enclosure marked deficient.
- `research/UNKNOWN_SPECIFICATIONS.md`: 26 open unknowns.

**Recommended provisional parts:** Espressif DevKitC-1 N16R8, PZEM-004T V4 100 A
split CT + ADuM1201/B0505S barrier, TE RT2 `RT444005` DPST-NO 8 A, Mean Well
IRM-05-5, Littelfuse 215 10 A, EPCOS S10K275, Sefuse SF169E, TMP102, DS3231M,
SSD1306, Type F 16 A socket (unapproved).

---

## 5. Architecture, isolation, data/control flow

- Diagram: `docs/hardware/SYSTEM_ARCHITECTURE.png/.svg/.pdf`.
- Functional split: mains / isolation barrier / SELV / network.
- PE continuous; no relay/fuse in PE.
- Two-pole switching reviewed; provisional relay 8 A.
- PZEM UART isolated; CT around one conductor.
- Relay driver with 100 kΩ pulldown, flyback diode, boot-safe OFF.
- Device is source of truth for commanded/fault/lockout; API stores shadow.
- UI shows `commanded` vs `observed`; `APPLIED` only after ACK.

Details: `safety/ISOLATION_PLAN.md`, `safety/ELECTRICAL_RATING_CHAIN.md`,
`docs/hardware/SYSTEM_ARCHITECTURE.md`.

---

## 6. Feasibility: size, cost, supply, trade-offs

- `research/FEASIBILITY_STUDY.md`: 13 questions answered with `GO/REDESIGN/BLOCKED`.
- 150×100×70 internal volume ~895 cm³; estimated component envelope ~285 cm³.
- Coarse CAD fit passes, but dimensions are approximate; physical fit unverified.
- Target 10 A **not met** by 8 A relay; final continuous rating 8 A or lower.
- BOM unpriced; target Rp500–750k cannot be confirmed. Safety parts may push to Q07=C.
- Supply/documentation risk: PZEM, socket/plug, enclosure, thermal cutoff.
- Recommended larger 180×120×70 enclosure if measured fit/clearance requires it.

---

## 7. 26 deliverable categories

| No. | Category | Key path | Status |
|---:|---|---|---|
| 01 | Component research | `research/COMPONENT_RESEARCH.md`, `candidates.csv` | PARTIAL |
| 02 | BOM | `bom/BOM_MASTER.csv`, `BOM_SUMMARY.json` | PARTIAL (unpriced) |
| 03 | Datasheets | `research/datasheets/MANIFEST.md` | PARTIAL |
| 04 | System architecture | `docs/hardware/SYSTEM_ARCHITECTURE.*` | PASS (digital) |
| 05 | Schematic | `hardware/kicad/*.kicad_sch` | PARTIAL/BLOCKED (ERC) |
| 06 | Wiring | `hardware/wiring/*.yaml`, `renders/` | PASS (render) |
| 07 | GPIO mapping | `hardware/interfaces/gpio_map.*` | UNVERIFIED (board) |
| 08 | PCB native | `hardware/kicad/smartplug.kicad_pcb` | PARTIAL/BLOCKED (DRC) |
| 09 | PCB manufacturing | `hardware/manufacturing/provisional/` | BLOCKED |
| 10 | PCB visualization | `hardware/pcb/render/placement_preview.*` | PARTIAL |
| 11 | Enclosure 3D | `hardware/mechanical/export/` | PARTIAL |
| 12 | Enclosure rendering | `hardware/mechanical/render/`, `drawings/` | PARTIAL |
| 13 | Firmware | `firmware/core/`, `firmware/main/` | PARTIAL |
| 14 | Firmware config | `firmware/partitions.csv`, `sdkconfig.defaults` | PARTIAL |
| 15 | Web | `apps/web/` | PASS (digital) |
| 16 | Android | `apps/android/` | PARTIAL (APK blocked) |
| 17 | Backend | `apps/api/` | PASS (digital) |
| 18 | Database | `database/migrations/` | PARTIAL (Postgres schema only) |
| 19 | MQTT | `packages/mqtt-contract/`, `infrastructure/broker/` | PASS (digital) |
| 20 | Notifications | `apps/api/src/services/notifications.ts` | PARTIAL (mock) |
| 21 | Deployment | `infrastructure/` | BLOCKED |
| 22 | Automated testing | `tests/`, `reports/` | PARTIAL (19 PASS/15 BLOCKED) |
| 23 | Engineering validation | `validation/` | PARTIAL |
| 24 | Security audit | `security/` | PARTIAL |
| 25 | Engineer documentation | `docs/tutorials/`, `docs/operations/` | PASS (digital) |
| 26 | Final handoff | `deliverables/` | PARTIAL |

---

## 8. Requirements traceability (80 FRs)

Full machine-readable records: `requirements/traceability.yaml`.
Summary: 80 total; 28 PASS, 25 PARTIAL, 24 NOT_STARTED, 3 BLOCKED.
`PASS` means digital evidence only; it does not imply physical validation.

{{FR_TABLE}}

---

## 9. ERC/DRC/netlist/GPIO/PCB/3D results

- KiCad CLI: not installed; ERC/DRC/Gerber/drill **BLOCKED**.
- Native KiCad files parse with `kiutils`: **PASS**.
- Schematic is a system block schematic; not component-level.
- PCB is placement-only 75×50 mm; no routing/nets/final footprints.
- Static wiring check: PE PASS, relay contacts separate PASS, coil SELV PASS,
  isolator sides PASS, mains/SELV static separation PASS.
- GPIO map vs firmware defines: PASS static; board revision UNVERIFIED.
- CadQuery STEP/STL + assembly + renders: generated; fit is coarse AABB and
  dimensions are approximate.
- No physical PE/thermal/isolation/load/3D fit validation.

---

## 10. Firmware status

- Portable C core: state machine, priority, TTL/replay, lockout, measurement
  validation, energy delta, schedule, CRC16, JSON. **74 checks PASS** with Zig host.
- ESP-IDF minimal app: relay OFF at boot, button debounce, core state machine,
  ON blocked while meter/temp invalid.
- ESP-IDF target build: **BLOCKED**; no `.bin`.
- PZEM/OLED/RGB/RTC/Wi-Fi/MQTT/OTA components: **NOT_IMPLEMENTED**.
- Secure boot/flash encryption: not enabled (irreversible, no approval).

---

## 11. Web/API/DB/MQTT/Android status

- API: 38 tests PASS; auth/RBAC/tenant/idempotency/lockout/ACK/analytics/audit.
- Web: Next build PASS; 5 Playwright tests PASS; axe login/dashboard PASS.
- MQTT: 11 contract tests PASS; aedes+simulator integration PASS.
- DB: SQLite dev adapter tested; PostgreSQL schema/migrations exist, adapter missing.
- Android: typecheck + Expo Android bundle PASS; **APK BLOCKED** (no SDK).
- Notifications: mock test PASS; Telegram live not tested.
- OTA: request event only; no signed image/rollback test.
- Deployment: config only; no URL/TLS/cloud claim.

---

## 12. Security and residual risk

- `security/THREAT_MODEL.md`, `API_AUTHORIZATION_MATRIX.csv`, `MQTT_ACL_PLAN.md`,
  `DEVICE_SECURITY_PLAN.md`, `PROVISIONING_SECURITY.md`, `OTA_SIGNING_AND_RECOVERY.md`.
- `npm audit`: 0 known npm vulnerabilities.
- Negative auth/RBAC/replay/pairing/lockout tests PASS.
- Gaps: TLS/MQTT ACL not executed, no secure boot/flash encryption, no signed OTA,
  no revoke-all-sessions, sessionStorage XSS risk, no independent pentest.
- Physical safety residual risks: relay weld, PE discontinuity, isolation failure,
  thermal hotspot, enclosure fire, USB mains contact. See
  `safety/RESIDUAL_RISK_REGISTER.csv`.

---

## 13. Safety/regulatory review requirements

- `safety/ELECTRICAL_RATING_CHAIN.md`: final rating 8 A or lower, not 10 A.
- `safety/ISOLATION_PLAN.md`: barrier unverified.
- `safety/CLEARANCE_CREEPAGE_WORKSHEET.md`: inputs incomplete; no numbers invented.
- `safety/POLARITY_AND_EARTH_ASSESSMENT.md`: PE continuous; test required.
- `safety/THERMAL_RISK_AND_DERATING.md`: thermal test required.
- `safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md`: draft.
- `safety/STANDARD_APPLICABILITY_MATRIX.md`: IEC/SNI applicability open.
- `safety/REVIEW_SIGNOFF_TEMPLATE.md`: no sign-off.

**No one has signed off this design. Do not fabricate or energize.**

---

## 14. PASS / FAIL / BLOCKED / UNVERIFIED

**PASS (digital):** domain, MQTT contract, API+simulator, simulator, firmware core,
web build/E2E/axe, static connectivity/GPIO/BOM, WireViz, CadQuery export/render,
KiCad parse, npm audit.

**FAIL:** none in the executed digital gate.

**BLOCKED:** KiCad ERC/DRC/Gerber, ESP-IDF build, Android APK, PostgreSQL/Docker,
MQTT TLS/ACL production, Boot-safe waveform, PE continuity, thermal/fuse/surge,
load/temperature, isolation review, HIL, deployment clean-room.

**UNVERIFIED:** physical dimensions, PZEM batch/protocol/isolation, relay rating/
lifecycle, socket/plug/PE, enclosure material, clearance/creepage, energy accuracy,
thermal performance, regulatory compliance.

See `reports/TEST_MATRIX.csv`, `reports/FAILURES.md`, `reports/VALIDATION_SUMMARY.json`.

---

## 15. Status definitions

| Status | Meaning |
|---|---|
| `DIGITAL_COMPLETE` | All required digital artifacts generated and digital checks pass. **Not claimed.** |
| `PARTIAL_DIGITAL` | Substantial digital artifacts/tests exist; some P0 digital/toolchain gaps remain. **Current.** |
| `ENGINEERING_REVIEW_REQUIRED` | Design has not been signed off by a qualified engineer. **Current.** |
| `HARDWARE_VALIDATION_REQUIRED` | No physical test evidence. **Current.** |
| `READY_FOR_FABRICATION` | Only after F4 safety/manufacturing review. **Not claimed.** |
| `READY_FOR_USE` | Only after physical/regulatory validation. **Not claimed.** |

---

## 16. Human action plan

1. **Select/verify components:** socket/plug, relay 10 A DPST or accept 8 A, PZEM
   batch, PSU, fuse/holder, MOV, thermal cutoff, terminal, enclosure, PE hardware.
2. **Install tools:** KiCad + CLI, ESP-IDF, Android SDK, Docker/PostgreSQL.
3. **Complete hardware design:** component schematic, footprints, routing, ERC/DRC,
   Gerber/drill, measured fit, clearance worksheet.
4. **Build firmware:** ESP-IDF target, PZEM/OLED/RGB/RTC/Wi-Fi/MQTT/OTA, bench tests.
5. **Build/verify Android APK** and push/provisioning.
6. **Implement PostgreSQL adapter** and deploy staging with TLS/MQTT ACL.
7. **Lab tests:** PE continuity, insulation/hipot, thermal rise, load/inrush,
   relay lifecycle, enclosure material, EMC/regulatory.
8. **Engineering/regulatory sign-off**, then F4/F5/F6.

---

## 17. User feedback needed

- Approve changing final continuous rating from 10 A to **8 A or lower**, or approve
  a larger 2P 16 A contactor/enclosure.
- Approve socket/plug product family (Type F vs Type E/F combo vs local standard).
- Approve PZEM V4 vs ADE7953 alternative if V4 documentation remains deficient.
- Approve enclosure material/size change if measured fit/clearance fails.
- Approve any purchase, VPS/domain, EAS/Firebase account, or irreversible eFuse step.
- Provide lab/engineer access for physical validation.

---

## 18. Appendix

- Full manifest with SHA-256: `deliverables/manifest.json`.
- Test logs: `reports/logs/`.
- Screenshots: `docs/ui-ux/screenshots/`.
- Datasheet hashes: `research/datasheets/MANIFEST.md`.
- Known limitations: unpriced BOM, unapproved parts, block-level schematic,
  placement-only PCB, approximate CAD, no ESP-IDF/APK/Postgres deployment,
  no physical validation, no certification.
- This report does not replace `reports/PHASE_1_ENGINEERING_REPORT.md`,
  `reports/PHASE_2_SOFTWARE_REPORT.md`, or the safety documents.
