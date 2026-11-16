# Security Audit Report — REV_C_PSU_BOARD

**Date:** 15 November 2026
**Scope:** digital artifacts in this repository; no production deployment or physical device.
**Status:** `PARTIAL` — controls tested where possible; high-risk gaps remain.

## 1. Evidence executed

| Test | Method | Result |
|---|---|---|
| API auth/login/refresh/logout | Vitest + Fastify inject | PASS |
| RBAC/tenant isolation | Owner/viewer/other-home tests | PASS |
| Command replay/stale/TTL/lockout | API + domain + C core tests | PASS |
| Pairing single-use/expiry | API test | PASS |
| MQTT contract/ACL direction | Vitest | PASS |
| Full command → MQTT → simulator ACK | aedes + MqttBridge + simulator | PASS |
| Web E2E | Playwright 5 tests | PASS |
| Accessibility (login/dashboard) | axe WCAG 2 A/AA serious/critical | PASS |
| Firmware core safety logic | 74 C checks | PASS |
| Dependency vulnerabilities | `npm audit --json` | 0 known npm vulnerabilities |
| Secret scan | Manual pattern review + `.gitignore` | PARTIAL (no gitleaks/trufflehog installed) |

## 2. Findings

| ID | Severity | Finding | Status |
|---|---|---|---|
| SEC-01 | High | Production TLS/MQTT ACL was not executed; dev broker is anonymous | OPEN |
| SEC-02 | High | Device secure boot/flash encryption not enabled or decided | OPEN |
| SEC-03 | High | No signed OTA image or rollback test | OPEN |
| SEC-04 | Medium | API uses SQLite dev adapter; PostgreSQL path not integrated/tested | OPEN |
| SEC-05 | Medium | Refresh token/session revocation is per-session; no revoke-all-sessions endpoint | OPEN |
| SEC-06 | Medium | Web stores token in sessionStorage; XSS would expose it; CSP is basic | OPEN |
| SEC-07 | Medium | In-memory rate limits are per-instance; no distributed limit | OPEN |
| SEC-08 | Medium | No independent penetration test or fuzzing | OPEN |
| SEC-09 | Low | Pairing code entropy is 6 digits; rate limiting helps but proof-of-possession is weak | OPEN |
| SEC-10 | Low | Android APK/push not built; mobile token storage only SecureStore design | OPEN |

## 3. Positive controls

- Passwords hashed with scrypt; timing-safe compare.
- JWT HS256 with issuer/audience; refresh token hash stored, rotation/revoke tested.
- Generic login failure; no user enumeration in tested responses.
- Tenant scoping returns 404 for other-tenant devices.
- Commands require idempotency, TTL, sequence/replay checks, lockout safety.
- UI never claims `observed_output` without feedback; synthetic data labeled.
- `npm audit` reports 0 known npm vulnerabilities at audit time.
- No secrets committed in tracked files (manual review; `.env` ignored).

## 4. Residual risk

- Physical mains safety is outside software scope and remains `BLOCKED`.
- Cloud compromise could issue authorized-looking commands; local lockout and independent protection are essential.
- No production monitoring/alerting/backup execution.
- No security review by a qualified engineer.

## 5. Next actions

1. Implement PostgreSQL adapter and run migrations/contract tests.
2. Deploy staging with TLS/MQTT ACL and run negative tests.
3. Decide secure boot/flash encryption with recovery plan.
4. Implement signed OTA + rollback test.
5. Add revoke-all-sessions and device credential rotation.
6. Run dependency/secret scanning in CI.
7. Independent security review before production.
