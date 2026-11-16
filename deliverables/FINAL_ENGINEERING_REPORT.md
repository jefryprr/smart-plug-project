# Final Engineering Report — ESP32-S3 IoT Smart Plug

**Date:** 16 November 2026
**Author/agent:** OpenCode (DeepSeek V4.1 Flash 1017)
**PRD version:** 1.0
**Design revision:** `REV_C_PSU_BOARD`
**Source commit:** see `git log`; generated from the REV_C working tree on 2026-11-16
**Manifest:** `deliverables/manifest.json`

---

## Amendment 2026-11-16 (REV_C_PSU_BOARD)

- User approved **8 A final** (~1.840 W at 230 V), limited to electronics/SMPS loads; not heaters/motors.
- PZEM-004T V4 and a **common 2-channel 5 V optocoupler relay module** are **off-board**, with enclosure brackets. The **HLK-5M05 is on the separate 50x65 mm PSU board**, not the carrier. The module is two independent SPDT channels, **not** a mechanically linked DPST.
- PSU replaced by user instruction: **Hi-Link HLK-5M05** (5 V 1 A / 5 W, 38×23×18 mm). Efficiency ~70% means ~2.1 W heat; isolation/certificate/batch are unverified (`PENDING_APPROVAL`). Study: `research/PSU_HLK_5M05.md`.
- **150×100×70 FAILS** the coarse fit; **180×120×70 is rejected** because the PZEM/relay/socket would only stack with a 0.5 mm gap, ignoring brackets and wiring. **220×120×70 PASSES** side-by-side and is **CONFIRMED** by the user (Q06=C, 2026-11-15).
- **Enclosure detailed:** 60 mm body + 10 mm lid, 4× M3 lid screws, 1 mm gasket, carrier standoffs, module bosses, mechanical barrier, right-wall socket/gland/M12 vent, top OLED/button/RGB cutouts, front USB service cover, and a printed DevKit reverse-insertion key. Assembly STEP/STL and fit report generated; physical fit/sealing/thermal are still unverified.
- **KiCad 10.0.8 CLI installed**; ERC 0 on the block-level schematic; the SELV carrier is routed at 100x70 mm (25 footprints = 22 assembled + 3 fiducials, 18 nets) with **DRC 0/0** at 0.15 mm, and the separate **PSU board** is routed at 50x65 mm (13 assembled + 3 mounting holes + 3 fiducials, 8 nets) with **DRC 0/0**. Both have routed Gerber/drill/POS exported. Both remain `ENGINEERING_REVIEW_REQUIRED` / `NOT_FOR_FABRICATION`.
- **ESP-IDF v6.1 target build PASS** (esp32s3, 192,496-byte `.bin`, SHA-256 in `reports/FIRMWARE_BUILD.md`); no board was flashed. **Android debug APK PASS** (arm64-v8a, 46,852,340 bytes, v2 debug signature verified; not device-tested).
- **Indonesian procurement matrix added** (2026-11-16): 57 lines, 40 listing-verified + 17 estimated. CORE Rp717.087 (restock Rp665.619), FULL Rp834.687; budget verdict `CORE_OVER_750K_MARKETPLACE; RESTOCK_WITH_MECH_FITS; FULL_OVER_BUDGET`. Details: `research/PROCUREMENT_INDONESIA.md`, `bom/BOM_PROCUREMENT.md`.

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

The digital tests pass where executable (27 PASS / 11 BLOCKED / 0 FAIL), but
critical physical and toolchain gates remain blocked: component-level
schematic/routing, firmware integration/flash tests, Android device tests,
PostgreSQL deployment, and all mains/thermal/PE/isolation/load testing.

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

Key decisions: inline outlet (Q01=B), **8 A final (amendment; 1.840 W)**, mixed
SMPS loads (Q04=B), review two-pole (Q05=A), **220×120×70 confirmed because
150×100 fails fit and 180×120 fails real clearance**, official DevKitC-1 N16R8 (Q08=B), PZEM comparison and
off-board (Q09=D), **common 2-channel optocoupler relay module off-board**
(Q10 amendment), lab prototype (Q12=A), ESP-IDF (Q23=A), Expo (Q24=A), default
OFF (Q25=C), computer-only lab (Q26=A), digital parallel phases (Q27=C).

**Unresolved safety-critical blockers:**
- Socket/plug MPN/certification/PE (Q02).
- 2-channel relay module batch/rating/active-low verification; channels are not mechanically linked.
- PZEM V4 batch datasheet/isolation/pinout.
- PE hardware/enclosure material/clearance values.
- No hardware/lab/engineer/regulatory sign-off.

---

## 4. Research, components, approvals, datasheets

- `research/COMPONENT_RESEARCH.md`: 45 candidates with evidence scores.
- `research/candidates.csv`: all candidates, not just winners.
- `research/PROCUREMENT_INDONESIA.md`: dated Indonesian supplier/price study, stock risks, and budget scenarios.
- `bom/BOM_MASTER.csv`: 48 engineering rows, **unpriced**, **unapproved**.
- `bom/BOM_PROCUREMENT.csv`: 57 dated prototype buy rows (40 listing-verified, 17 estimated).
- `bom/BOM_SUMMARY.json`: `PROCUREMENT_PRICED_2026-11-15`; CORE Rp717.087, FULL Rp834.687.
- `bom/COMPONENT_APPROVALS.yaml`: no `approved_for_fabrication`.
- `research/datasheets/MANIFEST.md`: 12 PDFs hashed (including the HLK-5M05 distributor copy) plus the PZEM-004T V1.0 archive; V4/socket/enclosure/HLK batch still marked deficient.
- `research/UNKNOWN_SPECIFICATIONS.md`: 31 open unknowns (including compatible board, enclosure flame rating, PZEM internal isolation, and relay batch).

**Recommended provisional parts:** Espressif-compatible DevKitC-1 N16R8 (explicit Q08=B
deviation; official stock unconfirmed), PZEM-004T V4 100 A CT with **internal optocoupler isolation** (no ADuM/B0505S), 74HCT125 + 10k/20k UART level shift,
off-board 2-channel optocoupler relay module (10 A class claim), Hi-Link HLK-5M05
(user-selected; efficiency/isolation batch unverified), Littelfuse 5x20 10 A slow-blow,
MOV 10D271K, SEFUSE SF96E 99 °C TCO, DS3231 module, SSD1306 OLED,
Simon Schuko 16 A socket, BOSS BP16 plug, MG Duradus 220x120x70 ABS enclosure.

**Budget verdict:** CORE electronics is Rp717.087 before shipping (Rp757.087 all-in),
which is **about Rp7.087 over** the Rp750.000 cap. The detailed enclosure adds an estimated **Rp28.000**
mechanical addendum (gasket, vent, printed USB cover/key, PSU bracket, thermal pad),
so marketplace CORE is about **Rp745.087 / Rp785.087 all-in**. EasyWare restock prices
bring it to about **Rp693.619 / Rp733.619 all-in**. FULL is Rp834.687 (Rp874.687 all-in),
or about Rp902.687 all-in with the addendum; do not downgrade safety parts to force it.

---

## 5. Architecture, isolation, data/control flow

- Diagram: `docs/hardware/SYSTEM_ARCHITECTURE.png/.svg/.pdf`.
- Functional split: mains / isolation barrier / SELV / network.
- PE continuous; no relay/fuse in PE.
- Two-channel L/N switching reviewed; off-board 2-channel module is **not** a mechanically linked DPST; final 8 A.
- PZEM UART isolated by the module’s internal optocouplers; no external ADuM/B0505S. CT around one conductor. No TMP102/temperature sensor.
- Relay driver with 100 kΩ pulldown, flyback diode, boot-safe OFF.
- Device is source of truth for commanded/fault/lockout; API stores shadow.
- UI shows `commanded` vs `observed`; `APPLIED` only after ACK.

Details: `safety/ISOLATION_PLAN.md`, `safety/ELECTRICAL_RATING_CHAIN.md`,
`docs/hardware/SYSTEM_ARCHITECTURE.md`.

---

## 6. Feasibility: size, cost, supply, trade-offs

- `research/FEASIBILITY_STUDY.md`: 13 questions answered with `GO/REDESIGN/BLOCKED`.
- 150×100×70 internal volume ~895 cm³; with off-board PZEM + 2ch relay module the coarse fit **FAILS**.
- 180×120×70: **rejected**; it only fit by stacking PZEM/relay/socket with a 0.5 mm gap and ignoring brackets/wiring.
- 220×120×70 confirmed (Q06=C): side-by-side coarse fit **PASS**; dimensions still approximate.
- Final continuous rating **8 A / ~1.840 W**, electronics/SMPS only.
- BOM prices: CORE Rp717.087 (Rp757.087 all-in), CORE restock Rp665.619 (Rp705.619 all-in), FULL Rp834.687 (Rp874.687 all-in). The electronics CORE is ~Rp757k all-in at marketplace prices; with the mechanical addendum it is ~Rp785k. EasyWare restock brings it to ~Rp734k all-in (under the cap). FULL exceeds the cap. Safety parts are not downgraded.
- Supply/documentation risk: PZEM batch, ESP32 official stock, HLK batch, socket/plug, enclosure flammability, thermal cutoff.
- 220×120×70 enclosure confirmed after 150×100 and 180×120 clearance review failed.

---

## 7. 26 deliverable categories

| No. | Category | Key path | Status |
|---:|---|---|---|
| 01 | Component research | `research/COMPONENT_RESEARCH.md`, `PROCUREMENT_INDONESIA.md`, `candidates.csv` | PARTIAL (dated sourcing) |
| 02 | BOM | `bom/BOM_MASTER.csv`, `BOM_PROCUREMENT.csv`, `BOM_SUMMARY.json` | PARTIAL (procurement priced; safety unapproved) |
| 03 | Datasheets | `research/datasheets/MANIFEST.md` | PARTIAL |
| 04 | System architecture | `docs/hardware/SYSTEM_ARCHITECTURE.*` | PASS (digital) |
| 05 | Schematic | `hardware/kicad/*.kicad_sch` | PARTIAL (block text; ERC 0) |
| 06 | Wiring | `hardware/wiring/*.yaml`, `renders/` | PASS (render) |
| 07 | GPIO mapping | `hardware/interfaces/gpio_map.*` | UNVERIFIED (board) |
| 08 | PCB native | `hardware/kicad/smartplug.kicad_pcb`, `psu_rev_c.kicad_pcb` | PASS (routed, DRC 0/0) |
| 09 | PCB manufacturing | `hardware/manufacturing/provisional/` (carrier + `psu/`) | PARTIAL (routed Gerber/drill/POS; not released) |
| 10 | PCB visualization | `hardware/pcb/render/placement_preview.*` | PARTIAL |
| 11 | Enclosure 3D | `hardware/mechanical/export/` | PARTIAL |
| 12 | Enclosure rendering | `hardware/mechanical/render/`, `drawings/` | PARTIAL |
| 13 | Firmware | `firmware/core/`, `firmware/main/` | PARTIAL (target build PASS) |
| 14 | Firmware config | `firmware/partitions.csv`, `sdkconfig.defaults` | PARTIAL |
| 15 | Web | `apps/web/` | PASS (digital) |
| 16 | Android | `apps/android/` | PASS (debug APK; not device-tested) |
| 17 | Backend | `apps/api/` | PASS (digital) |
| 18 | Database | `database/migrations/` | PARTIAL (Postgres schema only) |
| 19 | MQTT | `packages/mqtt-contract/`, `infrastructure/broker/` | PASS (digital) |
| 20 | Notifications | `apps/api/src/services/notifications.ts` | PARTIAL (mock) |
| 21 | Deployment | `infrastructure/` | BLOCKED |
| 22 | Automated testing | `tests/`, `reports/` | PARTIAL (27 PASS/11 BLOCKED) |
| 23 | Engineering validation | `validation/` | PARTIAL |
| 24 | Security audit | `security/` | PARTIAL |
| 25 | Engineer documentation | `docs/tutorials/`, `docs/operations/` | PASS (digital) |
| 26 | Final handoff | `deliverables/` | PARTIAL |

---

## 8. Requirements traceability (80 FRs)

Full machine-readable records: `requirements/traceability.yaml`.
Summary: 80 total; 28 PASS, 25 PARTIAL, 24 NOT_STARTED, 3 BLOCKED.
`PASS` means digital evidence only; it does not imply physical validation.

| FR | Priority | Phase | Status | Description | Key implementation | Tests |
|---|---|---|---|---|---|---|
| FR-001 | P0 | F1+F2 | PARTIAL | Real-time voltage monitoring | `apps/api/src/services/telemetry.ts`, `apps/web/src/components/ElectricalReadings.tsx` | T-SW-006 |
| FR-002 | P0 | F1+F2 | PARTIAL | Real-time current monitoring | `apps/api/src/services/telemetry.ts`, `apps/web/src/components/ElectricalReadings.tsx` | T-SW-006 |
| FR-003 | P0 | F1+F2 | PARTIAL | Real-time active power | `apps/api/src/services/telemetry.ts` | T-SW-006 |
| FR-004 | P0 | F1+F2 | PASS | Energy consumption (kWh) | `packages/domain/src/index.ts`, `apps/api/src/services/telemetry.ts` | T-SW-008, DOMAIN-ENERGY |
| FR-005 | P1 | F1+F2 | PARTIAL | Power factor monitoring | `apps/api/src/services/telemetry.ts`, `apps/web/src/components/ElectricalReadings.tsx` | T-SW-006 |
| FR-006 | P0 | F2 | PASS | Electricity cost calculator | `packages/domain/src/index.ts`, `apps/api/src/services/energy.ts` | DOMAIN-COST |
| FR-007 | P0 | F2 | PASS | Custom electricity tariff | `apps/api/src/routes/automation.ts`, `apps/api/src/services/energy.ts` | API-TARIFF |
| FR-008 | P0 | F2 | PASS | Energy history | `apps/api/src/routes/telemetry.ts`, `apps/api/src/db/schema.ts` | API-TELEMETRY |
| FR-009 | P1 | F2 | PASS | Energy analytics | `apps/api/src/services/energy.ts`, `apps/web/src/components/EnergyGraph.tsx` | API-ANALYTICS, T-SW-011 |
| FR-010 | P1 | F2 | NOT_STARTED | Peak power tracking | — | — |
| FR-011 | P1 | F2 | PASS | Energy budget monitoring | `apps/api/src/routes/automation.ts`, `apps/api/src/services/alerts.ts` | API-BUDGET, ALERT-BUDGET |
| FR-012 | P2 | F2 | NOT_STARTED | Energy data CSV export | — | — |
| FR-013 | P0 | F2 | PASS | Remote ON/OFF | `apps/api/src/services/commands.ts`, `apps/api/src/mqtt/bridge.ts` | API-COMMAND, INTEGRATION-COMMAND |
| FR-014 | P0 | F1+F2 | PARTIAL | Local ON/OFF | `firmware/main/app_main.c`, `apps/api/src/services/commands.ts` | CORE-BUTTON |
| FR-015 | P0 | F1 | PARTIAL | Physical ON/OFF button | `firmware/main/app_main.c` | CORE-BUTTON |
| FR-016 | P0 | F1+F2 | PARTIAL | Scheduled ON/OFF | `packages/domain/src/index.ts`, `firmware/core/smartplug_core.c` | DOMAIN-SCHEDULE, CORE-SCHEDULE |
| FR-017 | P1 | F1+F2 | PASS | Weekly scheduling | `packages/domain/src/index.ts`, `firmware/core/smartplug_core.c` | DOMAIN-SCHEDULE, CORE-SCHEDULE, API-AUTOMATION |
| FR-018 | P0 | F1+F2 | NOT_STARTED | Countdown timer | — | — |
| FR-019 | P1 | F1+F2 | NOT_STARTED | Automatic standby detection | — | — |
| FR-020 | P1 | F1+F2 | NOT_STARTED | Automatic standby cut-off | — | — |
| FR-021 | P1 | F1+F2 | NOT_STARTED | Idle detection | — | — |
| FR-022 | P1 | F1+F2 | NOT_STARTED | Power threshold automation | — | — |
| FR-023 | P0 | F1+F2 | PARTIAL | Power recovery settings | `firmware/main/app_main.c`, `docs/decisions/USER_ANSWERS.md` | CORE-BOOT |
| FR-024 | P0 | F1+F2 | PARTIAL | Offline scheduling | `firmware/core/smartplug_core.c` | CORE-SCHEDULE |
| FR-025 | P0 | F1+F2 | PASS | Automation priority management | `packages/domain/src/index.ts`, `firmware/core/smartplug_core.c` | DOMAIN-PRIORITY, CORE-PRIORITY |
| FR-026 | P0 | F1 | PARTIAL | Overcurrent protection | `firmware/core/smartplug_core.c`, `apps/api/src/services/alerts.ts` | CORE-MEASUREMENT, ALERT-HIGH-POWER |
| FR-027 | P0 | F1 | PARTIAL | Overtemperature protection | `firmware/core/smartplug_core.c`, `apps/api/src/services/alerts.ts` | CORE-MEASUREMENT, ALERT-TEMP |
| FR-028 | P0 | F1+F2 | PASS | Overvoltage warning | `firmware/core/smartplug_core.c`, `packages/domain/src/index.ts` | CORE-MEASUREMENT, DOMAIN-MEASUREMENT |
| FR-029 | P0 | F1+F2 | PASS | Undervoltage warning | `firmware/core/smartplug_core.c`, `packages/domain/src/index.ts` | CORE-MEASUREMENT, DOMAIN-MEASUREMENT |
| FR-030 | P0 | F1 | BLOCKED | Surge protection | `safety/PROTECTION_COORDINATION.md`, `bom/BOM_MASTER.csv` | T-HW-013 |
| FR-031 | P0 | F1 | BLOCKED | Thermal cutoff | `safety/THERMAL_RISK_AND_DERATING.md`, `bom/BOM_MASTER.csv` | T-HW-019 |
| FR-032 | P0 | F1 | BLOCKED | Fuse protection | `safety/ELECTRICAL_RATING_CHAIN.md`, `safety/PROTECTION_COORDINATION.md` | T-HW-013 |
| FR-033 | P0 | F1 | PARTIAL | Fail-safe startup | `firmware/main/app_main.c`, `firmware/core/smartplug_core.c` | CORE-BOOT |
| FR-034 | P0 | F1 | PASS | Sensor failure detection | `firmware/core/smartplug_core.c`, `packages/domain/src/index.ts` | CORE-MEASUREMENT, DOMAIN-MEASUREMENT, ALERT-SENSOR |
| FR-035 | P0 | F1+F2 | PASS | Electrical fault logging | `apps/api/src/services/audit.ts`, `apps/api/src/routes/operations.ts` | API-EVENTS |
| FR-036 | P0 | F1 | PASS | Fault lockout | `firmware/core/smartplug_core.c`, `packages/domain/src/index.ts` | CORE-LOCKOUT, DOMAIN-LOCKOUT, API-LOCKOUT |
| FR-037 | P0 | F1 | NOT_STARTED | OLED display | — | — |
| FR-038 | P1 | F1 | NOT_STARTED | OLED page navigation | — | — |
| FR-039 | P1 | F1 | NOT_STARTED | RGB NeoPixel status | — | — |
| FR-040 | P2 | F1 | NOT_STARTED | RGB engineering debug | — | — |
| FR-041 | P0 | F1 | NOT_STARTED | RGB fault indicator | — | — |
| FR-042 | P2 | F1 | NOT_STARTED | RGB night mode | — | — |
| FR-043 | P0 | F2 | PASS | Web dashboard | `apps/web/src/app`, `apps/web/src/components` | T-SW-011, T-SW-012 |
| FR-044 | P0 | F2 | PARTIAL | Android application | `apps/android/App.tsx` | T-SW-013, T-SW-014 |
| FR-045 | P1 | F2 | PASS | Device naming | `apps/api/src/routes/devices.ts`, `apps/web/src/components/DeviceSettings.tsx` | API-DEVICE-PATCH |
| FR-046 | P0 | F2 | PASS | Device status dashboard | `apps/web/src/components/DeviceSummaryCard.tsx`, `apps/web/src/app/(app)/dashboard/page.tsx` | T-SW-011 |
| FR-047 | P1 | F1+F2 | PASS | Engineering diagnostics dashboard | `apps/web/src/components/DeviceHealth.tsx`, `apps/api/src/routes/operations.ts` | API-DIAGNOSTICS, T-SW-011 |
| FR-048 | P0 | F1 | NOT_STARTED | Wi-Fi connectivity | — | — |
| FR-049 | P1 | F1+F2 | NOT_STARTED | BLE provisioning | — | — |
| FR-050 | P1 | F1+F2 | NOT_STARTED | SoftAP setup | — | — |
| FR-051 | P0 | F2 | PARTIAL | Hybrid local-cloud control | `apps/api/src/services/commands.ts`, `apps/api/src/mqtt/bridge.ts` | INTEGRATION-COMMAND |
| FR-052 | P0 | F1+F2 | PASS | MQTT integration | `packages/mqtt-contract/src/index.ts`, `apps/api/src/mqtt/bridge.ts` | T-SW-003, T-SW-004, INTEGRATION-COMMAND |
| FR-053 | P1 | F2 | NOT_STARTED | Home Assistant integration | — | — |
| FR-054 | P0 | F2 | PASS | REST API | `packages/api-contract/openapi.yaml`, `apps/api/src` | T-SW-001, API-TESTS |
| FR-055 | P0 | F2 | PARTIAL | Real-time synchronization | `apps/api/src/mqtt/bridge.ts`, `apps/web/src/lib/hooks.ts` | INTEGRATION-COMMAND |
| FR-056 | P0 | F1 | NOT_STARTED | Wi-Fi auto reconnection | — | — |
| FR-057 | P1 | F1+F2 | NOT_STARTED | Offline data buffering | — | — |
| FR-058 | P0 | F2 | PARTIAL | Cloud database | `apps/api/src/db/schema.ts`, `database/migrations/001_init.sql` | T-SW-002 |
| FR-059 | P1 | F2 | PARTIAL | Multi-device management | `apps/api/src/routes/devices.ts`, `apps/web/src/app/(app)/devices/page.tsx` | API-DEVICES |
| FR-060 | P1 | F2 | NOT_STARTED | Power anomaly detection | — | — |
| FR-061 | P1 | F2 | NOT_STARTED | Historical pattern analysis | — | — |
| FR-062 | P0 | F1+F2 | PASS | High power alert | `apps/api/src/services/alerts.ts` | ALERT-HIGH-POWER |
| FR-063 | P0 | F1+F2 | PARTIAL | High temperature alert | `apps/api/src/services/alerts.ts`, `firmware/core/smartplug_core.c` | ALERT-TEMP |
| FR-064 | P1 | F2 | NOT_STARTED | Standby consumption alert | — | — |
| FR-065 | P1 | F2 | PASS | Energy budget alert | `apps/api/src/services/alerts.ts` | ALERT-BUDGET |
| FR-066 | P1 | F2 | PARTIAL | Telegram notification | `apps/api/src/services/notifications.ts` | API-NOTIFICATION |
| FR-067 | P1 | F2 | NOT_STARTED | Android push notification | — | — |
| FR-068 | P0 | F2 | PASS | Event history | `apps/api/src/routes/operations.ts`, `apps/web/src/app/(app)/devices/[id]/events/page.tsx` | API-EVENTS |
| FR-069 | P0 | F1+F2 | PARTIAL | OTA firmware update | `apps/api/src/routes/operations.ts`, `firmware/partitions.csv` | API-OTA |
| FR-070 | P0 | F1+F2 | PARTIAL | OTA rollback | `firmware/sdkconfig.defaults`, `firmware/partitions.csv` | T-SW-018 |
| FR-071 | P0 | F1+F2 | PARTIAL | Firmware integrity verification | `security/OTA_SIGNING_AND_RECOVERY.md` | T-SW-018 |
| FR-072 | P0 | F1 | PARTIAL | Watchdog system | `firmware/sdkconfig.defaults` | T-HW-017 |
| FR-073 | P0 | F2 | PASS | Secure authentication | `apps/api/src/auth`, `apps/api/src/routes/auth.ts` | API-AUTH, SECURITY-NEGATIVE |
| FR-074 | P0 | F2 | PASS | Role-based access control | `apps/api/src/services/access.ts`, `apps/api/src/routes` | API-RBAC |
| FR-075 | P0 | F2 | PARTIAL | Encrypted communication | `security/THREAT_MODEL.md`, `infrastructure/reverse-proxy/Caddyfile` | T-SW-019 |
| FR-076 | P0 | F1+F2 | PASS | Device pairing security | `apps/api/src/routes/auth.ts`, `apps/api/src/services/commands.ts` | API-PAIRING, T-SW-015 |
| FR-077 | P0 | F1+F2 | PASS | Command validation | `firmware/core/smartplug_core.c`, `packages/domain/src/index.ts` | CORE-COMMAND, DOMAIN-COMMAND, API-COMMAND |
| FR-078 | P0 | F2 | PASS | Activity and audit logging | `apps/api/src/services/audit.ts`, `apps/api/src/db/schema.ts` | API-AUDIT |
| FR-079 | P0 | F1+F2 | NOT_STARTED | Factory reset | — | — |
| FR-080 | P0 | F1+F2 | PARTIAL | Device diagnostics | `apps/api/src/routes/operations.ts`, `apps/web/src/components/DeviceHealth.tsx` | API-DIAGNOSTICS |

---

## 9. ERC/DRC/netlist/GPIO/PCB/3D results

- KiCad CLI 10.0.8: ERC **0 violations** on the block-level schematic; routed SELV carrier **DRC 0 violations/0 unconnected** at 0.15 mm; routed Gerber/drill/POS exported.
- Native KiCad files parse with `kiutils`: **PASS**.
- Schematic is a system block schematic; not component-level connectivity.
- PCB is a routed 100×70 mm SELV carrier; DRC 0/0 at 0.15 mm; not released for fabrication.
- Static wiring check: PE PASS, relay contacts separate PASS, coil SELV PASS,
  PZEM internal isolation review still required; mains/SELV static separation PASS.
- GPIO map vs firmware defines: PASS static; board revision UNVERIFIED.
- CadQuery STEP/STL + assembly + renders: generated; fit is coarse AABB and
  dimensions are approximate.
- No physical PE/thermal/isolation/load/3D fit validation.

---

## 10. Firmware status

- Portable C core: state machine, priority, TTL/replay, lockout, measurement
  validation, energy delta, schedule, CRC16, JSON. **75 checks PASS** with Zig host.
- ESP-IDF minimal app: relay OFF at boot, button debounce, core state machine,
  ON blocked while meter/temp invalid.
- ESP-IDF v6.1 target build: **PASS**, `firmware/build/smartplug.bin` (192,496 bytes); no flash/bench test.
- PZEM/OLED/RGB/RTC/Wi-Fi/MQTT/OTA components: **NOT_IMPLEMENTED**.
- Secure boot/flash encryption: not enabled (irreversible, no approval).

---

## 11. Web/API/DB/MQTT/Android status

- API: 38 tests PASS; auth/RBAC/tenant/idempotency/lockout/ACK/analytics/audit.
- Web: Next build PASS; 5 Playwright tests PASS; axe login/dashboard PASS.
- MQTT: 11 contract tests PASS; aedes+simulator integration PASS.
- DB: SQLite dev adapter tested; PostgreSQL schema/migrations exist, adapter missing.
- Android: typecheck + Expo Android bundle PASS; **debug APK built** (arm64-v8a, SHA-256 in `reports/ANDROID_BUILD.md`), not installed/tested on a device.
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

- `safety/ELECTRICAL_RATING_CHAIN.md`: final rating **8 A/1.840 W**; module channels are not DPST.
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

**BLOCKED:** component-level schematic/routing/functional Gerber, firmware
integration/flash tests, Android device tests, PostgreSQL/Docker, MQTT TLS/ACL production,
boot-safe waveform, PE continuity, thermal/fuse/surge, load/temperature,
isolation review, HIL, deployment clean-room.

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

1. **Select/verify components:** socket/plug, 2-channel optocoupler relay module,
   PZEM batch, PSU, fuse/holder, MOV, thermal cutoff, terminal, 220×120 enclosure,
   PE hardware, PZEM/relay brackets.
2. **Install tools:** Docker/PostgreSQL; ESP-IDF v6.1, KiCad 10.0.8, and Android SDK are installed.
3. **Complete hardware design:** component schematic, footprints, routing, ERC/DRC,
   Gerber/drill, measured fit, clearance worksheet.
4. **Flash/test firmware:** flash the built image, then integrate PZEM/OLED/RGB/RTC/Wi-Fi/MQTT/OTA and run bench tests.
5. **Install/test the debug APK** on emulator/device; add push/provisioning and release signing.
6. **Implement PostgreSQL adapter** and deploy staging with TLS/MQTT ACL.
7. **Lab tests:** PE continuity, insulation/hipot, thermal rise, load/inrush,
   relay lifecycle, enclosure material, EMC/regulatory.
8. **Engineering/regulatory sign-off**, then F4/F5/F6.

---

## 17. User feedback needed

- Confirm **8 A/1.840 W final** (already used in the amended design).
- **220×120×70 is confirmed (Q06=C).** Build/measure the enclosure; 150×100 fails fit and 180×120 fails real clearance with off-board PZEM + relay module.
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
- Known limitations: procurement prices are listings not quotes, unapproved parts, block-level schematic,
  routed prototype PCB (not released), approximate CAD, no firmware integration/Android device test/Postgres deployment,
  no physical validation, no certification.
- This report does not replace `reports/PHASE_1_ENGINEERING_REPORT.md`,
  `reports/PHASE_2_SOFTWARE_REPORT.md`, or the safety documents.

- **DevKitC-1 socket corrected:** two 1x22 sockets at 22.86 mm (ADR-015).
