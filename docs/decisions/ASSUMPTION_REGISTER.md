# Assumption Register — REV_A_PROVISIONAL

**Status:** `OPEN` unless noted. Assumptions are not facts. Each has a verification plan.

| ID | Assumption | Source/basis | Impact if wrong | Reviewer | Verification | Status |
|---|---|---|---|---|---|---|
| A-001 | Supply is 230 VAC / 50 Hz nominal | Indonesian household context | Voltage/current rating, PSU, MOV, clearance | Engineer | Measure at lab/site | `PROVISIONAL` |
| A-002 | Final continuous load rating is **8 A (≈1.840 W at 230 V)**, limited to electronics/SMPS; not heaters/motors | User amendment 2026-11-15 | Label/rating, thermal test, user expectation | Engineer | Rating chain + thermal test | `PROVISIONAL` |
| A-003 | Loads are mixed electronics/SMPS, not motors | Q04=B | Relay inrush/lifecycle | Engineer | Load survey + inrush test | `PROVISIONAL` |
| A-004 | Type F/E-F socket is appropriate for Indonesia | Q02=D lean B | Connector/PE/regulatory | Engineer/regulatory | Product selection + standard review | `OPEN` |
| A-005 | Two-pole disconnection is safer for reversible plug | Q05=A | Relay size/rating | Engineer | Design review | `PROVISIONAL` |
| A-006 | **220×120×70 mm** is the confirmed enclosure; 150×100 fails fit and 180×120 fails real clearance with off-board PZEM + 2-channel relay | Q06=C confirmed 2026-11-15 | Enclosure/thermal/barrier | Mechanical engineer | Measured fit + tolerance stack + thermal test | `CONFIRMED_DECISION`; physical fit `UNVERIFIED` |
| A-007 | ESP32-S3-DevKitC-1 N16R8 official board is used | Q08=B | GPIO/RGB/strapping/space | Hardware engineer | Photo/revision check | `OPEN` |
| A-008 | PZEM-004T V4 100 A CT (closed or split) is representative | Q09=D + procurement | Metering/isolation | Hardware engineer | Batch datasheet + measurement | `OPEN` |
| A-009 | PZEM-004T V4 internal optocouplers are sufficient as the UART galvanic barrier; no external ADuM/B0505S | User decision + Tasmota/Components101 evidence | Isolation safety (single barrier) | Engineer | Creepage + hipot/leakage test | `PROVISIONAL` |
| A-010 | Common 2-channel 5 V optocoupler relay module (10 A class claim) is adequate for 8 A prototype, with active-low inputs and two independent SPST channels | User amendment 2026-11-15 | Channel non-linkage, contact rating, isolation, lifecycle | Engineer | Exact module datasheet + thermal/lifecycle test | `OPEN` |
| A-011 | Hi-Link HLK-5M05 5 V/1 A is enough for the estimated peak (~0.58 A), but efficiency ~70% and isolation/certification are unverified | User selection + power budget | Brownout/thermal/isolation | Hardware engineer | Measured peak/ripple/temperature/hipot | `PROVISIONAL` |
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
| A-023 | Indonesian procurement prices are 2026-11-15/16 listing snapshots, not supplier quotes; 43 lines listing-verified, 13 estimated | `bom/BOM_PROCUREMENT.csv` | Budget/schedule | Project owner | Re-quote before purchase | `PROVISIONAL` |
| A-024 | ESP32-S3 N16R8 compatible board at Rp139.968 is acceptable for prototype only as an explicit Q08=B deviation | Official local stock unconfirmed | GPIO/RGB/regulator/security | Hardware engineer | Board photo + pinout + RF test | `OPEN` |
| A-025 | MG Duradus 220x120x70 ABS IP65 enclosure fits, but flame-retardant grade is unverified | Listing + fit CAD | Fire/mechanical safety | Mechanical engineer | Material certificate + thermal/impact test | `OPEN` |
| A-026 | No temperature sensor is installed in REV_B; firmware must not require temperature validity | User instruction 2026-11-16 | Thermal safety/ON policy | Engineer | Thermal test + TCO/fuse review | `PROVISIONAL` |
| A-027 | 74HCT125 + 10k/20k divider are sufficient for PZEM 5V TTL to ESP32 3.3V | TI datasheet + divider calculation | UART reliability | Hardware engineer | Bench UART test at 9600 baud | `PROVISIONAL` |
| A-028 | 5 V rail needs a 1.1 A PTC plus SMBJ5.0A TVS; the HLK-5M05 alone is not treated as sufficient protection | Engineering judgment | 5 V wiring/transient protection | Hardware engineer | Bench trip/clamp test; verify PTC hold current | `PROVISIONAL` |
| A-029 | Enclosure 60 mm body + 10 mm lid, 1 mm gasket, M12 vent, printed USB cover and DevKit key are adequate for a prototype | Mechanical concept + CadQuery | Fit/sealing/thermal/service | Mechanical engineer | Print, measure, gasket/thermal/impact test | `PROVISIONAL` |
| A-030 | OLED/button/RGB on the top lid above J4/J6/J7 is acceptable ergonomically | Layout choice | User access/cable length | Product/mechanical | User review and physical fit | `OPEN` |
| A-031 | The printed DevKit key blocks reverse insertion without touching the correct board | Geometry concept | DevKit damage risk | Mechanical engineer | Print and insertion trial both orientations | `OPEN` |
| A-032 | First-order enclosure thermal estimate is 13-19 W loss and ~19-28 K rise; the M12 vent is not credited | Engineering calculation | Thermal safety | Thermal engineer | Closed-box 8 A/40 C test | `UNVERIFIED` |

## Rules

- An assumption that affects safety cannot become `CONFIRMED` without evidence.
- A change to A-002/A-004/A-007/A-008/A-010/A-011/A-013 triggers impact analysis across BOM/schematic/PCB/CAD/wiring/firmware.
- Assumptions are not a substitute for datasheets or tests.
