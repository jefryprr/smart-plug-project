# ADR Index

| ADR | Decision | Status |
|---|---|---|
| `ADR-001-PRODUCT-FORM-FACTOR.md` | Inline outlet, lab prototype scope | Accepted |
| `ADR-002-METERING-ARCHITECTURE.md` | PZEM V4 provisional + isolation barrier | Proposed/deficient |
| `ADR-003-SWITCHING-ARCHITECTURE.md` | Two-pole review; off-board 2-channel module; 8 A final | Proposed |
| `ADR-004-FIRMWARE-STACK.md` | ESP-IDF + portable C core | Accepted |
| `ADR-005-BACKEND-STACK.md` | Next.js + Fastify + SQLite dev/Postgres target | Accepted |
| `ADR-006-ANDROID-STACK.md` | Expo dev build | Accepted |
| `ADR-007-DEPLOYMENT.md` | Docker Compose + Caddy | Accepted direction, not deployed |
| `ADR-008-HARDWARE-TOOLCHAIN.md` | Custom KiCad generator, WireViz, CadQuery | Accepted with deviations |
| `ADR-009-LOCAL-LAN.md` | Defer authenticated local LAN API | Deferred |
| `ADR-010-TIME-ENERGY-SEMANTICS.md` | UTC, delta energy, tariff history | Accepted |
| `ADR-011-SYNTHETIC-DATA.md` | Label demo data | Accepted |
| `ADR-012-NO-IRREVERSIBLE-EFUSE.md` | No eFuse/secure boot without approval | Accepted |
| `ADR-013-PSU-HLK-5M05.md` | Hi-Link HLK-5M05 selected; IRM-05-5 fallback; PSU PENDING_APPROVAL | Accepted (user), component pending |
| `ADR-014-PROCUREMENT-STAGING.md` | CORE first, FULL (OLED/RTC/RGB) later; no safety downgrade for budget | Proposed |
| `ADR-015-DEVKITC-1-SOCKET.md` | Two 1x22 sockets at 22.86 mm; no 2x22 IDC socket | Accepted (digital) |
| `ADR-016-PZEM-ISOLATION-REV-C.md` | REV_D_CORE_ONLY uses PZEM internal optocouplers only; OUT3 conditional | Accepted as design input; batch/hipot unverified |
| `ADR-017-CORE-ONLY-TIME-SYNC.md` | CORE-only build; SNTP/NVS/API/MQTT/manual time; no RTC; schedules blocked when invalid | Accepted as design input; physical validation blocked |

## Superseding

If an ADR changes, add a new ADR and mark the old one `Superseded by ADR-xxx`; do not silently rewrite history.
