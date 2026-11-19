# Security Test Results — REV_D_CORE_ONLY

**Date:** 2026-11-15
**Scope:** digital API/web/MQTT/firmware core; no production deployment.

## 1. Executed tests

| Test | Method | Result |
|---|---|---|
| Wrong password → generic 401 | Vitest | PASS |
| Missing/tampered access token | Vitest | PASS |
| Refresh rotation + old token replay | Vitest | PASS |
| Logout revokes refresh session | Vitest | PASS |
| Cross-tenant device access → 404 | Vitest | PASS |
| Viewer cannot command/write | Vitest | PASS |
| Owner can command; idempotency replay | Vitest | PASS |
| Idempotency key conflict → 409 | Vitest | PASS |
| Lockout rejects ON; OFF accepted | Vitest + C core | PASS |
| Pairing code single-use/replay | Vitest | PASS |
| Command replay/stale/TTL/wrong device | Vitest + C core | PASS |
| MQTT topic/ACL direction | Vitest | PASS |
| MQTT command non-retained | Unit/contract | PASS |
| Web axe WCAG 2 A/AA (login/dashboard) | Playwright + axe | PASS (no serious/critical) |
| Dependency vulnerabilities | `npm audit --json` | 0 known npm vulnerabilities |

## 2. Negative-path evidence

- API tests include invalid body (422), unauthorized (401), forbidden (403), hidden resource (404), conflict (409), downstream unavailable (503).
- Simulator tests include replay and expired command.
- Firmware core tests include boot/degraded/lockout/meter/temp failure.

## 3. Gaps / findings

| ID | Finding | Severity | Status |
|---|---|---|---|
| SEC-01 | Production TLS/MQTT ACL not executed; dev broker anonymous | High | OPEN |
| SEC-02 | Secure boot/flash encryption not enabled/decided | High | OPEN |
| SEC-03 | No signed OTA/rollback test | High | OPEN |
| SEC-04 | PostgreSQL adapter missing | Medium | OPEN |
| SEC-05 | No revoke-all-sessions | Medium | OPEN |
| SEC-06 | sessionStorage XSS exposure; basic CSP | Medium | OPEN |
| SEC-07 | In-memory rate limits only | Medium | OPEN |
| SEC-08 | No independent pentest/fuzzing | Medium | OPEN |
| SEC-09 | 6-digit pairing entropy | Low | OPEN |
| SEC-10 | APK/push not built | Low | OPEN |

## 4. Secret handling

- `.env`/`.env.docker` are gitignored.
- `.env.example` contains variable names and dev-only defaults, no real tokens.
- Logger redaction covers authorization/password/refresh token.
- No real Telegram/FCM/JWT production secret is present.
- A dedicated secret scanner (gitleaks/trufflehog) is not installed; manual review only.

## 5. Conclusion

Digital security controls are partially implemented and tested. The project is **not** production-secure, and physical safety remains `BLOCKED/ENGINEERING_REVIEW_REQUIRED`.
