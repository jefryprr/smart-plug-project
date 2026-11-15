# ADR Index

| ADR | Decision | Status |
|---|---|---|
| `ADR-001-PRODUCT-FORM-FACTOR.md` | Inline outlet, lab prototype scope | Accepted |
| `ADR-002-METERING-ARCHITECTURE.md` | PZEM V4 provisional + isolation barrier | Proposed/deficient |
| `ADR-003-SWITCHING-ARCHITECTURE.md` | Two-pole review; 8 A provisional relay | Proposed |
| `ADR-004-FIRMWARE-STACK.md` | ESP-IDF + portable C core | Accepted |
| `ADR-005-BACKEND-STACK.md` | Next.js + Fastify + SQLite dev/Postgres target | Accepted |
| `ADR-006-ANDROID-STACK.md` | Expo dev build | Accepted |
| `ADR-007-DEPLOYMENT.md` | Docker Compose + Caddy | Accepted direction, not deployed |
| `ADR-008-HARDWARE-TOOLCHAIN.md` | Custom KiCad generator, WireViz, CadQuery | Accepted with deviations |
| `ADR-009-LOCAL-LAN.md` | Defer authenticated local LAN API | Deferred |
| `ADR-010-TIME-ENERGY-SEMANTICS.md` | UTC, delta energy, tariff history | Accepted |
| `ADR-011-SYNTHETIC-DATA.md` | Label demo data | Accepted |
| `ADR-012-NO-IRREVERSIBLE-EFUSE.md` | No eFuse/secure boot without approval | Accepted |

## Superseding

If an ADR changes, add a new ADR and mark the old one `Superseded by ADR-xxx`; do not silently rewrite history.
