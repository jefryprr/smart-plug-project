# Phase 2 Software Report — REV_A_PROVISIONAL

**Date:** 15 November 2026
**Agent:** OpenCode (DeepSeek V4.1 Flash 1017)
**PRD:** v1.0
**Design revision:** `REV_A_PROVISIONAL`
**Phase 2 status:** `PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED`
**Deployment:** `BLOCKED` (no Docker/Postgres/VPS/domain/TLS)
**Android APK:** `PASS` (debug, arm64-v8a, signature verified; not installed on device)

---

## 1. Stack dan ADR

| Layer | Choice | ADR/status |
|---|---|---|
| Web | Next.js 16.4.6, React 19.3.1, TypeScript 5.9.3 | build PASS |
| API | Fastify 5.12.8, TypeScript, Zod 4 | 38 tests PASS |
| Domain | TypeScript pure package | 34 tests PASS |
| DB dev | SQLite `node:sqlite` | tested |
| DB target | PostgreSQL 16 schema | schema only, no adapter |
| MQTT | `mqtt` 5.16.1 client, `aedes` 1.2.0 test broker | contract/integration PASS |
| Notifications | Telegram adapter + mock | mock tested; no live token |
| Android | Expo SDK 58 / RN 0.88.1 | typecheck + bundle + debug APK PASS; not device-tested |
| Deployment | Docker Compose + Caddy templates | not executed |

ADRs: `docs/decisions/ADR-004` (firmware), `ADR-005` (backend), `ADR-006` (Android), `ADR-007` (deployment), `ADR-009` (local LAN), `ADR-010` (time/energy), `ADR-011` (synthetic data).

---

## 2. Arsitektur software

```
Web/Android → API (auth/RBAC/TTL/idempotency) → DB
                  │
                  ├─ MQTT publish command (non-retained, QoS1)
                  └─ MQTT subscribe telemetry/state/ack/event/availability
Device simulator → MQTT → API → DB → waitFor ACK
```

- Device is source of truth for commanded/fault/lockout.
- Command status: `PENDING → ACCEPTED → DELIVERED → APPLIED`, or `REJECTED/EXPIRED/TIMEOUT`.
- `observed_output` is null unless verified feedback exists.
- UI never treats publish as success.

Detailed: `docs/hardware/SYSTEM_ARCHITECTURE.md`, `apps/api/src`, `apps/device-simulator/src`.

---

## 3. Contracts and versions

| Contract | Path | Version |
|---|---|---|
| OpenAPI | `packages/api-contract/openapi.yaml` | 3.1.0, 21 paths |
| API schemas | `packages/api-contract/src/index.ts` | Zod, schema_version 1 |
| MQTT schemas | `packages/mqtt-contract/src/index.ts` | `smartplug/v1`, schema_version 1 |
| MQTT fixtures | `packages/mqtt-contract/fixtures/` | synthetic |

Topics: telemetry, state, event, availability, command, ack, diag, config/desired, config/reported. Command/desired are non-retained.

---

## 4. Backend features

- Auth: scrypt password hash, JWT access token, refresh rotation/revoke, rate limit.
- Tenancy: homes/memberships, object-level authorization, 404 for other tenant.
- Devices: list/detail/rename, single-use pairing claim.
- Commands: idempotency key, TTL, sequence/replay, lockout, ACK handling, expiry job.
- Telemetry: validation, dedup by device+sequence, energy delta, gaps/reset.
- Energy: tariff history, daily aggregates, cost estimate, missing-tariff semantics.
- Schedules: weekly versioned config.
- Events/audit: append-only at application layer, pagination.
- Diagnostics: role-gated.
- Notifications: mock/Telegram test.
- OTA: request event only, no delivery.
- Health: live/ready.

Schema: `apps/api/src/db/schema.ts` (SQLite), `database/migrations/001_init.sql` (Postgres target).

---

## 5. Web

- App Router pages: login, dashboard, devices, onboarding, device overview/analytics/schedules/automation/events/diagnostics/settings, settings pages, admin firmware.
- Components: PowerControl, ElectricalReadings, UsageAndCost, EnergyGraph, EventList, DeviceHealth, ScheduleEditor, DeviceSettings.
- Design system/UX docs: `docs/ui-ux/`.
- Screenshots: `docs/ui-ux/screenshots/` (12 images).
- Build: `next build` PASS.
- E2E: 5 Playwright tests PASS.
- Accessibility: axe WCAG 2 A/AA login/dashboard no serious/critical.
- Demo data labeled `SYNTHETIC_DEMO`.

---

## 6. Android

- Source: `apps/android/App.tsx` (login, devices, overview, readings, ON/OFF with ACK, settings).
- `npm run typecheck` PASS.
- `npx expo export --platform android` PASS: 596 modules, 1.5 MB Hermes bundle.
- APK: **debug build PASS**. `apps/android/android/app/build/outputs/apk/debug/app-debug.apk`, 46,852,340 bytes, SHA-256 `BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61`; `arm64-v8a`; v2 debug signature verified. Not installed/tested on a device or emulator.
- BLE provisioning/push: **not implemented**.
- Token storage: SecureStore design.

---

## 7. Device simulator and MQTT integration

- `apps/device-simulator/src/simulator.ts`: state machine, command TTL/replay, ACK, telemetry, fault injection, availability LWT.
- 4 simulator tests PASS.
- Full API→MQTT→simulator→ACK integration: 4 tests PASS.
- Simulator is explicitly not HIL/real hardware.

---

## 8. Notifications and OTA

- Telegram: adapter + mock; no live token/sandbox test. Test endpoint rate-limited.
- Android push: not implemented (no FCM/Expo credentials).
- OTA: partition/rollback config + API request event only. No signed image, no delivery, no rollback test.

---

## 9. Security

- Threat model, authorization matrix, MQTT ACL plan, provisioning/OTA plans.
- `npm audit`: 0 known npm vulnerabilities.
- Negative auth/RBAC/replay/pairing/lockout tests PASS.
- Gaps: TLS/MQTT ACL not executed, no secure boot/flash encryption, no signed OTA, no revoke-all-sessions, sessionStorage XSS risk, no independent pentest.
- Report: `security/SECURITY_AUDIT_REPORT.md`.

---

## 10. Deployment

- Config: `infrastructure/docker-compose.dev.yaml`, Dockerfiles, Mosquitto/Caddy templates.
- **Not executed**: Docker/Postgres/Mosquitto not installed.
- API uses SQLite dev adapter; PostgreSQL adapter missing.
- No production URL, domain, certificate, or cloud claim.
- Operations runbooks provided.

---

## 11. Test results

| Test | Result |
|---|---|
| TypeScript typecheck (4 workspaces) | PASS |
| Domain tests | 34 PASS |
| MQTT contract | 11 PASS |
| API + simulator | 38 PASS |
| Simulator | 4 PASS |
| Firmware core | 74 checks, 0 failures |
| Web build | PASS |
| Playwright | 5 PASS |
| axe login/dashboard | PASS |
| Static connectivity/GPIO/BOM | PASS |
| npm audit | 0 known vulnerabilities |
| Overall gate | 23 PASS / 11 BLOCKED / 0 FAIL (KiCad + ESP-IDF build now run) |

See `reports/VALIDATION_SUMMARY.json`, `reports/TEST_MATRIX.csv`, `reports/FAILURES.md`.

---

## 12. Performance/availability

- No production latency/availability measurement.
- API tests are local; no load test.
- Telemetry interval/polling chosen for demo, not benchmarked.
- Analytics range capped at 400 days; telemetry page max 500.
- MQTT QoS 0/1; no broker cluster/HA.
- SQLite single-writer; not suitable for multi-instance production.

---

## 13. Regressions and bottlenecks

- Changing GPIO/board revision requires GPIO/firmware/PCB/wiring/CAD regeneration.
- Changing relay/PSU/fuse/PE/enclosure requires full safety gate.
- Changing API schema requires web/Android contract tests.
- Changing time/energy rules requires analytics/automation tests.
- Bottlenecks: no Postgres adapter, no TLS/ACL execution, no local LAN transport, no signed OTA, no Android device/emulator test (debug APK exists).

---

## 14. Roadmap

1. Implement PostgreSQL adapter; run migrations/contract tests.
2. Deploy staging with TLS/MQTT ACL; run negative tests.
3. Flash the built ESP-IDF image; integrate PZEM/OLED/RGB/RTC/Wi-Fi/MQTT/OTA.
4. Install/test the debug APK; implement BLE provisioning/push and release signing.
5. Implement local LAN authenticated API/gateway.
6. Add revoke-all-sessions, device credential rotation, signed OTA.
7. Independent security review.
8. Hardware/lab validation and engineering sign-off.

---

## 15. Kesimpulan Fase 2

Fase 2 digital **belum** `DIGITAL_COMPLETE`: backend/web/API/simulator/firmware core are functional and tested, but PostgreSQL deployment, production TLS/ACL, Android APK, push, local LAN, and signed OTA are not complete. Status: **`PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED`**. No production deployment or safety claim.
