# Assumption Register — REV_A_PROVISIONAL

**Status:** `OPEN` unless noted. Assumptions are not facts. Each has a verification plan.

| ID | Assumption | Source/basis | Impact if wrong | Reviewer | Verification | Status |
|---|---|---|---|---|---|---|
| A-001 | Supply is 230 VAC / 50 Hz nominal | Indonesian household context | Voltage/current rating, PSU, MOV, clearance | Engineer | Measure at lab/site | `PROVISIONAL` |
| A-002 | Final continuous load rating is **8 A (≈1.840 W at 230 V)**, limited to electronics/SMPS; not heaters/motors | User amendment 2026-11-15 | Label/rating, thermal test, user expectation | Engineer | Rating chain + thermal test | `PROVISIONAL` |
| A-003 | Loads are mixed electronics/SMPS, not motors | Q04=B | Relay inrush/lifecycle | Engineer | Load survey + inrush test | `PROVISIONAL` |
| A-004 | Type F/E-F socket is appropriate for Indonesia | Q02=D lean B | Connector/PE/regulatory | Engineer/regulatory | Product selection + standard review | `OPEN` |
| A-005 | Two-pole disconnection is safer for reversible plug | Q05=A | Relay size/rating | Engineer | Design review | `PROVISIONAL` |
| A-006 | **220×120×70 mm** is the working enclosure; 150×100 fails fit and 180×120 fails real clearance with off-board PZEM + 2-channel relay | Q06=B + amendment | Enclosure/thermal/barrier | Mechanical engineer | User confirmation + measured fit + thermal test | `PROVISIONAL` |
| A-007 | ESP32-S3-DevKitC-1 N16R8 official board is used | Q08=B | GPIO/RGB/strapping/space | Hardware engineer | Photo/revision check | `OPEN` |
| A-008 | PZEM-004T V4 split CT is representative | Q09=D | Metering/isolation | Hardware engineer | Batch datasheet + measurement | `OPEN` |
| A-009 | ADuM1201 + B0505S barrier is sufficient for PZEM UART | Engineering judgment | Isolation safety | Engineer | Isolation review + hipot test | `OPEN` |
| A-010 | Common 2-channel 5 V optocoupler relay module (10 A class claim) is adequate for 8 A prototype, with active-low inputs and two independent SPST channels | User amendment 2026-11-15 | Channel non-linkage, contact rating, isolation, lifecycle | Engineer | Exact module datasheet + thermal/lifecycle test | `OPEN` |
| A-011 | Mean Well IRM-05-5 5 W is enough for peak load | Power budget | Brownout/thermal | Hardware engineer | Measured peak current | `PROVISIONAL` |
| A-012 | 100 A CT is not an output current rating | PRD warning | Safety/rating | Engineer | Rating chain | `CONFIRMED` |
| A-013 | PE can be routed directly without relay/fuse | Safety principle | Shock safety | Engineer | PE continuity test | `PROVISIONAL` |
| A-014 | 3D printed enclosure is prototype-only | PRD/material review | Fire/mechanical safety | Mechanical engineer | Material/enclosure review | `CONFIRMED` |
| A-015 | BLE + SoftAP can be secured with a short window | Q15=C | Provisioning security | Security engineer | Firmware test | `OPEN` |
| A-016 | DS3231M RTC is needed for offline schedule holdover | Q16=C | Schedule/space/BOM | Firmware engineer | Drift/backup test | `PROVISIONAL` |
| A-017 | SQLite is acceptable for local dev/tests, Postgres for deployment | Q22=A | Data layer | Backend engineer | Postgres adapter + migration test | `OPEN` |
| A-018 | Expo dev build can add BLE/push later | Q24=A | Android capability | Mobile engineer | Dev build + native module test | `OPEN` |
| A-019 | No owned components (Q28=B) | User answer | BOM/procurement | Project owner | Inventory check | `CONFIRMED` |
| A-020 | No lab/physical test capability (Q26=A) | User answer | All physical gates | Project owner | Facility confirmation | `CONFIRMED` |
| A-021 | Demo data is synthetic and labeled | Environment constraint | Misleading results | Software engineer | Code/UI review | `CONFIRMED` |
| A-022 | No irreversible eFuse action without approval | ADR-012 | Device recovery/security | Security engineer | Review | `CONFIRMED` |

## Rules

- An assumption that affects safety cannot become `CONFIRMED` without evidence.
- A change to A-002/A-004/A-007/A-008/A-010/A-011/A-013 triggers impact analysis across BOM/schematic/PCB/CAD/wiring/firmware.
- Assumptions are not a substitute for datasheets or tests.
