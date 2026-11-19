# Software Guide

**Design revision:** `REV_D_CORE_ONLY`  
**Status:** digital prototype; software tests pass where executable, but the device is not flashed or deployed.

This guide is for running and understanding the software without touching mains hardware.

---

## 1. What is in the repository

```text
apps/
  api/                 Fastify API + SQLite dev adapter
  web/                 Next.js dashboard
  device-simulator/    MQTT device twin
  android/             Expo Android source + generated project
packages/
  domain/              pure rules: commands, energy, cost, schedule, freshness
  api-contract/        OpenAPI 3.1 + Zod
  mqtt-contract/       topics, schemas, ACL direction, fixtures
firmware/              portable C safety core + ESP-IDF v6.1 skeleton
database/              PostgreSQL migrations + dev seed
infrastructure/        Docker/Mosquitto/Caddy templates
```

The device is the source of truth for `commanded_output` and fault/lockout. The API stores a shadow. The UI shows `APPLIED` only after a device ACK; `observed_output` only when feedback exists.

---

## 2. Quick start

### Prerequisites

- Node.js **22+**
- npm **10+**
- Optional: Docker/PostgreSQL, MQTT broker, Android SDK, ESP-IDF

### Install and run

```powershell
npm ci
npm run api:dev      # API on :4000, SQLite, seeded demo
npm run web:dev      # Next.js on :3000
npm run sim:dev      # device simulator (needs a local MQTT broker)
```

Open `http://localhost:3000` and sign in with the local demo account:

```text
demo@example.com / demo1234
pairing code: 123456
```

> Demo credentials are seeded for local development only. Never use them in production or expose the demo to the internet.

### Run tests

```powershell
npm run typecheck
npm test
npm run build -w @smartplug/web
npx playwright test
```

The root `npm test` covers domain, MQTT contract, API + simulator integration, and simulator tests. Playwright covers the web UI. See [`TESTING.md`](TESTING.md).

---

## 3. Component responsibilities

| Component | Path | Responsibility |
|---|---|---|
| **Domain** | `packages/domain` | Command priority, energy delta, cost/tariff, schedule, freshness, secret redaction |
| **API contract** | `packages/api-contract` | OpenAPI 3.1 paths and Zod request/response schemas |
| **MQTT contract** | `packages/mqtt-contract` | `smartplug/v1/{device_id}/...` topics, payload schemas, ACL direction, fixtures |
| **API** | `apps/api` | Fastify, auth/RBAC, tenant scoping, commands, telemetry, energy, events, analytics, diagnostics, notification adapter |
| **Simulator** | `apps/device-simulator` | MQTT device twin, state machine, ACK, telemetry |
| **Web** | `apps/web` | Next.js dashboard, login, devices, analytics, schedules, automation, events, diagnostics, settings |
| **Android** | `apps/android` | Expo React Native app; debug APK built |
| **Firmware** | `firmware/` | Portable C safety core + ESP-IDF skeleton |

---

## 4. Data and control semantics

- Timestamps are UTC; UI displays Asia/Jakarta.
- Meter counters are cumulative; energy deltas handle reset/gap detection.
- Missing data is `null`, not zero.
- Tariff history is effective by interval start; no retroactive rewrite.
- Commands are idempotent, TTL-bound, replay-checked, and lockout-aware.
- `commanded_output` is the requested state; `observed_output` requires verified feedback.
- The UI shows `APPLIED` only after a device ACK.
- Auto ON requires a valid clock; an invalid clock blocks it.
- The local button and schedule core logic continue without internet. LAN API is deferred (`ADR-009`).

---

## 5. API and MQTT contracts

- OpenAPI: [`../packages/api-contract/openapi.yaml`](../packages/api-contract/openapi.yaml)
- MQTT contract: [`../packages/mqtt-contract/src/index.ts`](../packages/mqtt-contract/src/index.ts)
- Fixtures: [`../packages/mqtt-contract/fixtures/`](../packages/mqtt-contract/fixtures/)
- Command status: `PENDING → ACCEPTED → DELIVERED → APPLIED`, or `REJECTED/EXPIRED/TIMEOUT`.
- MQTT namespace: `smartplug/v1/{device_id}/...`.

The dev broker is anonymous only for local simulation. Production requires TLS, a password file, and per-device ACLs — not deployed/tested.

---

## 6. Database

| Environment | Implementation | Status |
|---|---|---|
| Development | SQLite `node:sqlite` (`apps/api/src/db/schema.ts`) | PASS |
| Target | PostgreSQL 16 (`database/migrations/001_init.sql`) | Adapter/deployment BLOCKED |

The API PostgreSQL adapter is not implemented. Docker/PostgreSQL clean-room deployment is blocked. Do not claim production readiness.

---

## 7. Security

- JWT access tokens + refresh rotation, scrypt password hashing, RBAC, tenant scoping.
- Refresh tokens are stored as hashes; logout revokes the session.
- Logger redaction covers authorization, password, and refresh token fields.
- MQTT ACL plan exists; production broker/TLS not deployed.
- No secure boot, flash encryption, or signed OTA yet (`ADR-012`).
- Android uses SecureStore for tokens; production signing/rotation/revoke still needed.

See [`../security/THREAT_MODEL.md`](../security/THREAT_MODEL.md), [`../security/SECURITY_AUDIT_REPORT.md`](../security/SECURITY_AUDIT_REPORT.md), and [`../SECURITY.md`](../SECURITY.md).

---

## 8. Android

A debug arm64-v8a APK was built and v2-signature verified. It was **not installed** on a device/emulator. Production signing, push/BLE, and device tests remain blocked. See [`../apps/android/README_BUILD_APK.md`](../apps/android/README_BUILD_APK.md) and [`../reports/ANDROID_BUILD.md`](../reports/ANDROID_BUILD.md).

---

## 9. Firmware

- Portable C safety core: `firmware/core/`.
- Host tests: `firmware/test/host/run_tests.ps1` (88 checks, including time gating).
- ESP-IDF v6.1 target build: `scripts/build_firmware.ps1` (build only, not flashed).
- No PZEM/Wi-Fi/MQTT/OTA integration or boot-waveform test yet. No OLED/RTC/external RGB by design; onboard RGB GPIO48 is a status indicator.

See [`../firmware/README.md`](../firmware/README.md) and [`../reports/FIRMWARE_BUILD.md`](../reports/FIRMWARE_BUILD.md).

---

## 10. Known gaps

| Gap | Status |
|---|---|
| Firmware flash and hardware integration | BLOCKED |
| Android device/emulator test | BLOCKED |
| PostgreSQL adapter/deployment | BLOCKED |
| MQTT TLS/ACL production | BLOCKED |
| Signed OTA/rollback | BLOCKED |
| Full system HIL | BLOCKED |
| Local LAN API | Deferred (`ADR-009`) |

---

## 11. Related documents

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`TESTING.md`](TESTING.md)
- [`software/README.md`](software/README.md)
- [`../docs/tutorials/17_SETUP_BACKEND_DB_MQTT.md`](tutorials/17_SETUP_BACKEND_DB_MQTT.md)
- [`../docs/tutorials/18_RUN_NEXTJS_WEB.md`](tutorials/18_RUN_NEXTJS_WEB.md)
- [`../docs/tutorials/19_BUILD_ANDROID_APK.md`](tutorials/19_BUILD_ANDROID_APK.md)
