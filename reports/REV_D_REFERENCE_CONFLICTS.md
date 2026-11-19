# REV_D_CORE_ONLY — Reference Conflict Inventory

**Date:** 2026-11-19  
**Purpose:** list every active OLED/RTC/external-RGB/v1.1 reference before the REV_D edit, and state whether it is removed, deferred, or historical.

## 1. Active references to remove

| Area | Current reference | Decision |
|---|---|---|
| Carrier connectors | J4 OLED (JST-XH 4), J5 RTC (JST-XH 6), J7 external RGB (JST-XH 3) | **Remove** from schematic, PCB, BOM, wiring, firmware, docs |
| Carrier I2C | SDA GPIO8, SCL GPIO9, 4.7k pullups R6/R7 | **Remove**; no I2C bus in CORE-only |
| OLED control | OLED reset GPIO6 | **Remove** |
| RTC control | RTC INT GPIO7, DS3231 module | **Remove**; no replacement RTC hardware |
| External RGB | RGB data GPIO10, 330R R3, 74HCT125 second gate | **Remove**; use onboard DevKitC-1 RGB |
| Board profile | `esp32s3_devkitc1_v1.1_provisional`, GPIO38 assumption | **Supersede** with v1.0 user-confirmed, GPIO48 |
| Firmware | OLED/RTC/RGB driver references, I2C init, GPIO6/7/10 | **Remove** from active build; add time service and onboard RGB status |
| BOM | OLED, DS3231, external RGB LED/connector, 330R, 4.7k pullups, related cables | **Remove or mark DEFERRED** |
| Web/Android | OLED/RTC/RGB settings/diagnostics | **Remove active references**; keep only deferred/historical notes |
| Enclosure | OLED window, RTC bosses, external RGB light pipe | **Remove**; add small onboard-RGB window if needed |

## 2. References that stay but become historical/deferred

| Area | Reference | Treatment |
|---|---|---|
| `PRD.md` FULL features | OLED, RTC, RGB external feature list | Mark **DEFERRED_CORE_ONLY**; not deleted from product roadmap |
| `reports/CHANGELOG.md`, `reports/AGENT_ACTION_LOG.md`, `reports/logs/` | Old REV_D_CORE_ONLY/OLED/RTC/RGB runs | Historical only; do not treat as active build |
| `docs/decisions/ADR-014-PROCUREMENT-STAGING.md` | FULL stage (OLED/RTC/RGB) | Update to DEFERRED for REV_D |
| `docs/decisions/ADR-015-DEVKITC-1-SOCKET.md` | v1.1/GPIO38 discussion | Update with v1.0 confirmation and history note |
| `research/candidates.csv`, `research/COMPONENT_RESEARCH.md` | OLED/RTC/RGB candidates | Keep as research/deferred candidates, not active BOM |
| `hardware/kicad/DISPLAY_AND_BUTTONS.kicad_sch`, `RTC_ONLY.kicad_sch` | Old block sheets | Remove from root sheet; keep files only if marked historical, otherwise delete |

## 3. Safety-critical items that must NOT be removed

- PSU board: TB1/TB2, F1, MOV, TCO, HLK-5M05, F2 PTC, D1 TVS, 3× JST 5 V.
- PE chassis stud and PE continuity.
- Relay module and its 5 V/GPIO control.
- PZEM + CT and the internal-isolation decision (ADR-016).
- Enclosure barrier, strain relief, gasket, vent, USB cover.
- Fuse/MOV/TCO/terminal ratings, creepage/clearance, thermal test plan.

## 4. Time architecture replacement

- UTC internal time; Asia/Jakarta display (UTC+7, no DST).
- `time_valid` only after trusted sync and age ≤ 12 h (configurable).
- SNTP primary; API/MQTT fallback; manual owner/admin set.
- NVS stores last-known UTC/source/timezone for display only.
- Schedule blocked and schedule-origin output forced OFF when invalid.
- Manual button/web/API control remains allowed.
- No replay of missed schedule events.

## 5. Revision rule

All active artifacts use `REV_D_CORE_ONLY`. Old REV_D_CORE_ONLY/REV_B/REV_A strings are historical only. No mixed-revision build.
