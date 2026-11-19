# ADR-005 — Backend and Database Stack

**Status:** Accepted (Q22=A, Q17=C)
**Date:** 2026-11-15

## Context
The system needs auth, tenant isolation, device commands with idempotency/ACK, telemetry, energy math, schedules, audit, and notifications. The user chose Next.js + separate TypeScript backend and hybrid local/cloud.

## Decision
- **Next.js 16** for web.
- **Fastify 5 + TypeScript** for the API.
- **SQLite (`node:sqlite`)** for local tests/demo to keep the environment reproducible.
- **PostgreSQL 16** is the target deployment database; schema/migrations exist, but the API PostgreSQL adapter is **not implemented**.
- MQTT broker: Mosquitto in deployment; `aedes` in tests.
- Docker Compose + Caddy for deployment templates (not executed).

## Consequences
- API tests run without Docker/Postgres (43 tests).
- The SQLite/Postgres divergence is a real gap; no production DB claim.
- Fastify routes use prepared SQL and Zod validation.
- Energy math lives in `packages/domain` and is shared with the device simulator.

## Alternatives
- Next.js API monolith: simpler but less testable separation.
- Managed cloud: deferred until credentials/cost approval.
