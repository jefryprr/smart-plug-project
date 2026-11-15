# ADR-007 — Deployment and Cloud Posture

**Status:** Accepted direction (Q17=C, Q22=C); not deployed
**Date:** 2026-11-15

## Context
The user wants hybrid local/cloud, self-host first. No VPS/domain/TLS credentials are available. Docker is not installed.

## Decision
- Provide **Docker Compose** dev/staging templates and a **Caddy** reverse proxy template.
- Production deployment requires user approval, domain/DNS, TLS, secrets, and a PostgreSQL adapter.
- Dev broker is anonymous only for local simulator; production broker requires TLS + password file + ACL.
- No paid provider, VPS, domain, EAS, or Firebase is activated.

## Consequences
- Deployment is `BLOCKED`/`CONFIG_ONLY`; no URL is claimed.
- Secrets are `.env`/secret manager, never repo.
- Local-first behavior remains the design goal.
- Backups/monitoring/runbooks are documented but not executed.

## Alternatives
- Managed cloud: deferred until cost/security comparison.
- Single VPS with manual TLS: possible after approval.
