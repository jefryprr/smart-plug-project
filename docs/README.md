# Documentation Index

**Project:** SMART PLUG PROJECT<br>
**Design revision:** `REV_D_CORE_ONLY`<br>
**Status:** `PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`<br>
**Fabrication:** `NOT_RELEASED`

This is the map of all project documentation. If you are new, start with [`START_HERE.md`](START_HERE.md) or [`../README.id.md`](../README.id.md).

---

## Start here

| Document | What it covers |
|---|---|
| [`START_HERE.md`](START_HERE.md) | Guided path for non-engineers |
| [`../README.md`](../README.md) | English project landing page |
| [`../README.id.md`](../README.id.md) | Indonesian project landing page |
| [`FAQ.md`](FAQ.md) | Common questions |
| [`GLOSSARY.md`](GLOSSARY.md) | Plain-language terms |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | What is PASS, BLOCKED, and unverified |
| [`REPOSITORY_MAP.md`](REPOSITORY_MAP.md) | Every top-level file/directory and what it is for |
| [`SAFETY.md`](SAFETY.md) | Safety overview and non-negotiable rules |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System, hardware, software, data flow |
| [`HARDWARE_GUIDE.md`](HARDWARE_GUIDE.md) | Boards, modules, connectors, power tree |
| [`SOFTWARE_GUIDE.md`](SOFTWARE_GUIDE.md) | API, web, Android, MQTT, simulator |
| [`TESTING.md`](TESTING.md) | How to reproduce the digital gate |

---

## Hardware

| Document | What it covers |
|---|---|
| [`hardware/SYSTEM_ARCHITECTURE.md`](hardware/SYSTEM_ARCHITECTURE.md) | Functional block architecture |
| [`hardware/SYSTEM_ARCHITECTURE.png`](hardware/SYSTEM_ARCHITECTURE.png) | Architecture image (also `.svg`, `.pdf`) |
| [`../hardware/psu/README.md`](../hardware/psu/README.md) | REV_D_CORE_ONLY 50 × 65 mm mains-entry PSU board |
| [`../hardware/kicad/README.md`](../hardware/kicad/README.md) | KiCad block schematic + routed carrier + PSU |
| [`../hardware/carrier/README.md`](../hardware/carrier/README.md) | SELV carrier, sockets, connectors |
| [`../hardware/wiring/README.md`](../hardware/wiring/README.md) | Main + metering harnesses (CORE-only) |
| [`../hardware/interfaces/gpio_map.md`](../hardware/interfaces/gpio_map.md) | GPIO assignment and restrictions |
| [`../hardware/mechanical/README.md`](../hardware/mechanical/README.md) | CadQuery enclosure, brackets, exports |
| [`../hardware/mechanical/FIT_ANALYSIS.md`](../hardware/mechanical/FIT_ANALYSIS.md) | Digital fit report |
| [`../hardware/manufacturing/provisional/fabrication_notes.md`](../hardware/manufacturing/provisional/fabrication_notes.md) | Provisional fabrication notes |
| [`hardware/PROCUREMENT_AND_INCOMING_QC.md`](hardware/PROCUREMENT_AND_INCOMING_QC.md) | Incoming inspection checklist |

### Research and BOM

| Document | What it covers |
|---|---|
| [`../research/COMPONENT_RESEARCH.md`](../research/COMPONENT_RESEARCH.md) | Candidate comparison |
| [`../research/PSU_HLK_5M05.md`](../research/PSU_HLK_5M05.md) | HLK-5M05 study |
| [`../research/PSU_BOARD_EVIDENCE.md`](../research/PSU_BOARD_EVIDENCE.md) | REV_D_CORE_ONLY PSU research evidence table |
| [`../research/OFFBOARD_MODULES.md`](../research/OFFBOARD_MODULES.md) | PZEM/relay off-board study |
| [`../research/PZEM_INTERNAL_ISOLATION.md`](../research/PZEM_INTERNAL_ISOLATION.md) | PZEM internal isolation evidence |
| [`../research/PROCUREMENT_INDONESIA.md`](../research/PROCUREMENT_INDONESIA.md) | Dated Indonesian sourcing/price study |
| [`../research/FEASIBILITY_STUDY.md`](../research/FEASIBILITY_STUDY.md) | Mechanical/electrical feasibility |
| [`../research/datasheets/MANIFEST.md`](../research/datasheets/MANIFEST.md) | Datasheet links, hashes, status |
| [`../bom/BOM_MASTER.md`](../bom/BOM_MASTER.md) | Engineering BOM |
| [`../bom/BOM_PROCUREMENT.md`](../bom/BOM_PROCUREMENT.md) | Dated prototype buy list |
| [`../bom/COMPONENT_APPROVALS.yaml`](../bom/COMPONENT_APPROVALS.yaml) | Approval status per component |

---

## Safety

| Document | What it covers |
|---|---|
| [`SAFETY.md`](SAFETY.md) | Summary and rules |
| [`../safety/ISOLATION_PLAN.md`](../safety/ISOLATION_PLAN.md) | Boundary map, ground policy, verification plan |
| [`../safety/ELECTRICAL_RATING_CHAIN.md`](../safety/ELECTRICAL_RATING_CHAIN.md) | Rating chain from plug to load |
| [`../safety/PROTECTION_COORDINATION.md`](../safety/PROTECTION_COORDINATION.md) | Fuse/MOV/TCO coordination |
| [`../safety/CLEARANCE_CREEPAGE_WORKSHEET.md`](../safety/CLEARANCE_CREEPAGE_WORKSHEET.md) | Creepage/clearance inputs and gaps |
| [`../safety/THERMAL_RISK_AND_DERATING.md`](../safety/THERMAL_RISK_AND_DERATING.md) | Thermal risks and derating |
| [`../safety/THERMAL_CALCULATION.md`](../safety/THERMAL_CALCULATION.md) | Thermal calculation |
| [`../safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md`](../safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md) | FMEA |
| [`../safety/POLARITY_AND_EARTH_ASSESSMENT.md`](../safety/POLARITY_AND_EARTH_ASSESSMENT.md) | PE/polarity assessment |
| [`../safety/REGULATORY_PLAN_INDONESIA.md`](../safety/REGULATORY_PLAN_INDONESIA.md) | Indonesian regulatory plan |
| [`../safety/STANDARD_APPLICABILITY_MATRIX.md`](../safety/STANDARD_APPLICABILITY_MATRIX.md) | Standards applicability |
| [`../safety/RESIDUAL_RISK_REGISTER.csv`](../safety/RESIDUAL_RISK_REGISTER.csv) | Residual risks |
| [`../safety/REVIEW_SIGNOFF_TEMPLATE.md`](../safety/REVIEW_SIGNOFF_TEMPLATE.md) | Engineer sign-off template |

---

## Decisions

| Document | What it covers |
|---|---|
| [`decisions/ADR-INDEX.md`](decisions/ADR-INDEX.md) | All 17 ADRs |
| [`decisions/USER_ANSWERS.md`](decisions/USER_ANSWERS.md) | User decisions Q01–Q28 (markdown) |
| [`decisions/USER_ANSWERS.yaml`](decisions/USER_ANSWERS.yaml) | User decisions Q01–Q28 (machine-readable) |
| [`decisions/ASSUMPTION_REGISTER.md`](decisions/ASSUMPTION_REGISTER.md) | Open assumptions |
| [`decisions/OPEN_QUESTIONS.md`](decisions/OPEN_QUESTIONS.md) | Open questions/blockers |
| [`decisions/QUESTIONNAIRE.md`](decisions/QUESTIONNAIRE.md) | Original questionnaire |
| [`decisions/TOOLCHAIN_COMPATIBILITY.md`](decisions/TOOLCHAIN_COMPATIBILITY.md) | Toolchain compatibility |
| [`decisions/ADR-001-PRODUCT-FORM-FACTOR.md`](decisions/ADR-001-PRODUCT-FORM-FACTOR.md) | Inline outlet form factor |
| [`decisions/ADR-002-METERING-ARCHITECTURE.md`](decisions/ADR-002-METERING-ARCHITECTURE.md) | Metering architecture |
| [`decisions/ADR-003-SWITCHING-ARCHITECTURE.md`](decisions/ADR-003-SWITCHING-ARCHITECTURE.md) | Switching architecture |
| [`decisions/ADR-004-FIRMWARE-STACK.md`](decisions/ADR-004-FIRMWARE-STACK.md) | ESP-IDF + C core |
| [`decisions/ADR-005-BACKEND-STACK.md`](decisions/ADR-005-BACKEND-STACK.md) | Next.js + Fastify |
| [`decisions/ADR-006-ANDROID-STACK.md`](decisions/ADR-006-ANDROID-STACK.md) | Expo Android |
| [`decisions/ADR-007-DEPLOYMENT.md`](decisions/ADR-007-DEPLOYMENT.md) | Docker/Caddy target |
| [`decisions/ADR-008-HARDWARE-TOOLCHAIN.md`](decisions/ADR-008-HARDWARE-TOOLCHAIN.md) | KiCad/WireViz/CadQuery |
| [`decisions/ADR-009-LOCAL-LAN.md`](decisions/ADR-009-LOCAL-LAN.md) | Local LAN API deferred |
| [`decisions/ADR-010-TIME-ENERGY-SEMANTICS.md`](decisions/ADR-010-TIME-ENERGY-SEMANTICS.md) | UTC/energy/tariff semantics |
| [`decisions/ADR-011-SYNTHETIC-DATA.md`](decisions/ADR-011-SYNTHETIC-DATA.md) | Demo data labeling |
| [`decisions/ADR-012-NO-IRREVERSIBLE-EFUSE.md`](decisions/ADR-012-NO-IRREVERSIBLE-EFUSE.md) | No eFuse/secure boot without approval |
| [`decisions/ADR-013-PSU-HLK-5M05.md`](decisions/ADR-013-PSU-HLK-5M05.md) | HLK-5M05 selection |
| [`decisions/ADR-014-PROCUREMENT-STAGING.md`](decisions/ADR-014-PROCUREMENT-STAGING.md) | CORE/FULL procurement |
| [`decisions/ADR-015-DEVKITC-1-SOCKET.md`](decisions/ADR-015-DEVKITC-1-SOCKET.md) | DevKitC-1 socket spacing |
| [`decisions/ADR-016-PZEM-ISOLATION-REV-C.md`](decisions/ADR-016-PZEM-ISOLATION-REV-C.md) | PZEM internal isolation in REV_D_CORE_ONLY |

---

## Software

| Document | What it covers |
|---|---|
| [`SOFTWARE_GUIDE.md`](SOFTWARE_GUIDE.md) | End-to-end software guide |
| [`software/README.md`](software/README.md) | Component responsibilities, contracts, data rules |
| [`../packages/api-contract/openapi.yaml`](../packages/api-contract/openapi.yaml) | OpenAPI 3.1 |
| [`../packages/mqtt-contract/src/index.ts`](../packages/mqtt-contract/src/index.ts) | MQTT topics/schemas |
| [`../database/README.md`](../database/README.md) | PostgreSQL migrations/seed |
| [`../infrastructure/deployment/README.md`](../infrastructure/deployment/README.md) | Deployment templates |
| [`../security/THREAT_MODEL.md`](../security/THREAT_MODEL.md) | Threat model |
| [`../security/SECURITY_AUDIT_REPORT.md`](../security/SECURITY_AUDIT_REPORT.md) | Security audit |

---

## Assembly and operations

| Document | What it covers |
|---|---|
| [`assembly/ASSEMBLY_PLAN.md`](assembly/ASSEMBLY_PLAN.md) | Three assembly scopes |
| [`assembly/LOW_VOLTAGE_ASSEMBLY.md`](assembly/LOW_VOLTAGE_ASSEMBLY.md) | Low-voltage assembly |
| [`assembly/MAINS_ASSEMBLY_QUALIFIED.md`](assembly/MAINS_ASSEMBLY_QUALIFIED.md) | Mains scope for qualified personnel |
| [`assembly/INSPECTION_CHECKLIST.md`](assembly/INSPECTION_CHECKLIST.md) | Inspection checklist |
| [`operations/RUNBOOK.md`](operations/RUNBOOK.md) | Operations runbook |
| [`operations/INCIDENT_RESPONSE.md`](operations/INCIDENT_RESPONSE.md) | Incident response |
| [`operations/BACKUP_RESTORE.md`](operations/BACKUP_RESTORE.md) | Backup/restore |
| [`operations/ROLLBACK_SERVER.md`](operations/ROLLBACK_SERVER.md) | Server rollback |
| [`operations/KEY_ROTATION.md`](operations/KEY_ROTATION.md) | Key rotation |
| [`operations/DEVICE_REPLACEMENT.md`](operations/DEVICE_REPLACEMENT.md) | Device replacement |
| [`operations/TROUBLESHOOTING.md`](operations/TROUBLESHOOTING.md) | Troubleshooting |

---

## UI/UX

| Document | What it covers |
|---|---|
| [`ui-ux/USER_FLOWS.md`](ui-ux/USER_FLOWS.md) | User flows |
| [`ui-ux/DESIGN_SYSTEM.md`](ui-ux/DESIGN_SYSTEM.md) | Design tokens/components |
| [`ui-ux/SCREEN_SPECIFICATIONS.md`](ui-ux/SCREEN_SPECIFICATIONS.md) | Screen specs |
| [`ui-ux/RESPONSIVE_MATRIX.md`](ui-ux/RESPONSIVE_MATRIX.md) | Responsive behavior |
| [`ui-ux/ACCESSIBILITY_CHECKLIST.md`](ui-ux/ACCESSIBILITY_CHECKLIST.md) | Accessibility |
| [`ui-ux/SCREENSHOTS.md`](ui-ux/SCREENSHOTS.md) | Screenshot index |
| [`ui-ux/screenshots/`](ui-ux/screenshots/) | 12 real Playwright screenshots |
| [`assets/banner.png`](assets/banner.png) | README banner |
| [`assets/social-preview.png`](assets/social-preview.png) | 1280 × 640 social preview |

---

## Tutorials (26 files)

Start with [`tutorials/00_READ_FIRST.md`](tutorials/00_READ_FIRST.md). The full tutorial index is [`tutorials/README.md`](tutorials/README.md).

| # | Tutorial |
|---|---|
| 00 | [Baca Dulu](tutorials/00_READ_FIRST.md) |
| 01 | [Setup Windows 11 + OpenCode](tutorials/01_SETUP_WINDOWS_OPENCODE.md) |
| 02 | [Setup KiCad](tutorials/02_SETUP_KICAD.md) |
| 03 | [Setup Circuit-Synth](tutorials/03_SETUP_CIRCUIT_SYNTH.md) |
| 04 | [Setup WireViz](tutorials/04_SETUP_WIREVIZ.md) |
| 05 | [Setup CadQuery](tutorials/05_SETUP_CADQUERY.md) |
| 06 | [Install Support Tools](tutorials/06_INSTALL_SUPPORT_TOOLS.md) |
| 07 | [Baca BOM dan Datasheet](tutorials/07_READ_BOM_AND_DATASHEETS.md) |
| 08 | [Baca Schematic dan GPIO](tutorials/08_READ_SCHEMATIC_AND_GPIO.md) |
| 09 | [Periksa PCB Secara Digital](tutorials/09_CHECK_PCB_DIGITALLY.md) |
| 10 | [Perencanaan Assembly](tutorials/10_ASSEMBLY_PLANNING.md) |
| 11 | [Soldering Low Voltage](tutorials/11_SOLDERING_LOW_VOLTAGE.md) |
| 12 | [Mains Assembly (Qualified Only)](tutorials/12_MAINS_ASSEMBLY_FOR_QUALIFIED_PERSONNEL.md) |
| 13 | [Inspection Before Power](tutorials/13_INSPECTION_BEFORE_POWER.md) |
| 14 | [Setup ESP-IDF](tutorials/14_SETUP_ESP_IDF.md) |
| 15 | [Flash dan Konfigurasi](tutorials/15_FLASH_AND_CONFIGURE.md) |
| 16 | [Local Mock Test](tutorials/16_LOCAL_MOCK_TEST.md) |
| 17 | [Setup Backend, DB, MQTT](tutorials/17_SETUP_BACKEND_DB_MQTT.md) |
| 18 | [Jalankan Web Next.js](tutorials/18_RUN_NEXTJS_WEB.md) |
| 19 | [Build Android APK](tutorials/19_BUILD_ANDROID_APK.md) |
| 20 | [Pair Device](tutorials/20_PAIR_DEVICE.md) |
| 21 | [Telegram / Push](tutorials/21_CONFIGURE_TELEGRAM_PUSH.md) |
| 22 | [Deploy Staging/Production](tutorials/22_DEPLOY_STAGING_PRODUCTION.md) |
| 23 | [Testing dan Validasi](tutorials/23_TESTING_AND_VALIDATION.md) |
| 24 | [Operations dan Troubleshooting](tutorials/24_OPERATIONS_AND_TROUBLESHOOTING.md) |
| 25 | [Final Handoff](tutorials/25_FINAL_HANDOFF.md) |

---

## Reports and deliverables

| Document | What it covers |
|---|---|
| [`../reports/TEST_MATRIX.csv`](../reports/TEST_MATRIX.csv) | Every test/status/exit code/log |
| [`../reports/VALIDATION_SUMMARY.json`](../reports/VALIDATION_SUMMARY.json) | Machine-readable gate |
| [`../reports/FAILURES.md`](../reports/FAILURES.md) | Blockers |
| [`../reports/PHASE_1_ENGINEERING_REPORT.md`](../reports/PHASE_1_ENGINEERING_REPORT.md) | Hardware phase |
| [`../reports/PHASE_2_SOFTWARE_REPORT.md`](../reports/PHASE_2_SOFTWARE_REPORT.md) | Software phase |
| [`../reports/FIRMWARE_BUILD.md`](../reports/FIRMWARE_BUILD.md) | ESP-IDF build evidence |
| [`../reports/ANDROID_BUILD.md`](../reports/ANDROID_BUILD.md) | APK build evidence |
| [`../reports/AMENDMENT_8A_OFFBOARD.md`](../reports/AMENDMENT_8A_OFFBOARD.md) | 8 A/off-board amendment |
| [`../reports/RESEARCH_LOG.md`](../reports/RESEARCH_LOG.md) | REV_D_CORE_ONLY research log |
| [`../reports/CHANGELOG.md`](../reports/CHANGELOG.md) | Commit rationale |
| [`../deliverables/FINAL_ENGINEERING_REPORT.md`](../deliverables/FINAL_ENGINEERING_REPORT.md) | Final handoff |
| [`../deliverables/manifest.json`](../deliverables/manifest.json) | 26 categories, hashes, blockers |
| [`../deliverables/CHECKSUMS.sha256`](../deliverables/CHECKSUMS.sha256) | SHA-256 manifest |

---

## Validation and traceability

| Document | What it covers |
|---|---|
| [`../validation/ISOLATION_BOUNDARY_CHECK.md`](../validation/ISOLATION_BOUNDARY_CHECK.md) | Static wiring isolation check |
| [`../validation/WIRING_CONNECTIONS.csv`](../validation/WIRING_CONNECTIONS.csv) | Derived wiring connections |
| [`../validation/NETLIST_SCHEMATIC.csv`](../validation/NETLIST_SCHEMATIC.csv) | Derived netlist |
| [`../validation/PSU_CROSSCHECK.json`](../validation/PSU_CROSSCHECK.json) | PSU static crosscheck |
| [`../validation/GPIO_CROSSCHECK.json`](../validation/GPIO_CROSSCHECK.json) | GPIO crosscheck |
| [`../validation/CONNECTIVITY_DIFF.json`](../validation/CONNECTIVITY_DIFF.json) | Connectivity diff |
| [`../requirements/traceability.yaml`](../requirements/traceability.yaml) | Requirements → evidence |

---

## Contributing and project policy

| Document | What it covers |
|---|---|
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to contribute |
| [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) | Community behavior |
| [`../SECURITY.md`](../SECURITY.md) | Vulnerability reporting |
| [`../SUPPORT.md`](../SUPPORT.md) | Where to get help |
| [`../CHANGELOG.md`](../CHANGELOG.md) | Release/change history |
| [`../ROADMAP.md`](../ROADMAP.md) | Project phases and gates |
| [`../LICENSE`](../LICENSE) | MIT license |
| [`../NOTICE.md`](../NOTICE.md) | Third-party notices |
| [`../AGENTS.md`](../AGENTS.md) | Agent operating rules |
| [`../PRD.md`](../PRD.md) | Product requirements document |
