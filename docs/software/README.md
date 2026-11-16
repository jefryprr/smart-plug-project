# Software Documentation

## Components

| Component | Path | Responsibility |
|---|---|---|
| Domain | `packages/domain` | command priority, energy delta, cost, schedule, freshness |
| API contract | `packages/api-contract` | OpenAPI 3.1 + Zod schemas |
| MQTT contract | `packages/mqtt-contract` | topics, schemas, ACL direction, fixtures |
| API | `apps/api` | Fastify, SQLite adapter, auth/RBAC, commands, telemetry, energy, events |
| Simulator | `apps/device-simulator` | MQTT device twin, state machine, ACK, telemetry |
| Web | `apps/web` | Next.js dashboard |
| Android | `apps/android` | Expo source + generated project (debug APK built) |

## Run

```powershell
npm ci
npm run api:dev
npm run sim:dev
npm run web:dev
```

## Contracts

- OpenAPI: `packages/api-contract/openapi.yaml` (21 paths).
- MQTT namespace: `smartplug/v1/{device_id}/...`.
- Command status: `PENDING → ACCEPTED → DELIVERED → APPLIED`, or `REJECTED/EXPIRED/TIMEOUT`.
- `observed_output` only with verified feedback.

## Data rules

- UTC timestamps; UI Asia/Jakarta.
- Cumulative meter counters; delta with reset/gap detection.
- Missing data is null, not zero.
- Tariff history effective by interval start; no retroactive rewrite.
- Commands idempotent, TTL-bound, replay-checked, lockout-aware.

## Database

- Dev: SQLite `node:sqlite` (`apps/api/src/db/schema.ts`).
- Target: PostgreSQL 16 (`database/migrations/001_init.sql`).
- **Gap:** API PostgreSQL adapter not implemented.

## Security

- JWT access/refresh rotation, scrypt, RBAC, tenant scoping.
- MQTT ACL plan; dev broker anonymous only.
- No secure boot/flash encryption/signed OTA yet.

## Tests

```powershell
npm run test
npm run typecheck
npx playwright test
```

See `reports/UNIT_TEST_RESULTS.md`, `INTEGRATION_TEST_RESULTS.md`, `SECURITY_TEST_RESULTS.md`.
