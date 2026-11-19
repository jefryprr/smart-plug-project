# Security Policy

## Supported versions

This repository is a **digital prototype**. There is no production release and no long-term support window yet.

| Version | Supported |
|---|---|
| `master` (REV_D_CORE_ONLY) | Best-effort security fixes |
| Older revisions | Not supported |

## Reporting a vulnerability

**Do not open a public issue with vulnerability details, real secrets, tokens, private keys, or personal data.**

Use GitHub’s private vulnerability reporting:

1. Go to the repository’s **Security** tab.
2. Choose **Report a vulnerability**.
3. Include:
   - affected version/commit;
   - component (API, web, Android, firmware, MQTT, infrastructure);
   - reproduction steps or proof of concept;
   - impact assessment;
   - suggested fix, if known.

If private reporting is unavailable, contact the maintainer via GitHub ([@jefryprr](https://github.com/jefryprr)) and ask for a private channel. Do not include the exploit details in the first public message.

## What to report

- Authentication/authorization bypass, tenant isolation break, RBAC flaws.
- Command replay, TTL bypass, idempotency bypass, lockout bypass.
- Secret leakage in logs, telemetry, screenshots, fixtures, or git history.
- MQTT topic/ACL escalation.
- OTA/signing key handling flaws.
- Dependency vulnerabilities with a realistic exploit path.
- Unsafe defaults that could lead to mains/PE/relay bypass.

## What not to report here

- General hardware safety questions → use [`SUPPORT.md`](SUPPORT.md) and read [`docs/SAFETY.md`](docs/SAFETY.md).
- Physical mains safety incidents → stop, disconnect safely if qualified, and follow your lab’s incident procedure. This repository cannot provide emergency assistance.
- Claims that the prototype is not certified → that is documented, not a vulnerability.

## Security posture

Current controls:

- JWT access tokens with short TTL; refresh token rotation/revoke.
- scrypt password hashing; timing-safe comparison.
- RBAC and tenant scoping on API routes.
- Logger redaction for authorization/password/refresh token fields.
- MQTT ACL plan; dev broker anonymous only for local simulation.
- No real secrets in tracked files; `.env` ignored.
- SBOM and dependency audit artifacts.

Known gaps:

- No production MQTT TLS/ACL deployment.
- No signed OTA/secure boot/flash encryption.
- Web stores tokens in `sessionStorage`; XSS would expose them.
- No dedicated secret scanner in CI (manual review + `.gitignore`).
- Android debug APK only; no production signing/device test.
- PostgreSQL adapter and production deployment not implemented.

See [`security/SECURITY_AUDIT_REPORT.md`](security/SECURITY_AUDIT_REPORT.md) and [`security/THREAT_MODEL.md`](security/THREAT_MODEL.md).

## Safe harbor

Good-faith security research that respects privacy, avoids data destruction, and does not test against live third-party systems is welcome. Do not access other users’ data, do not degrade service, and do not publish exploit details before a fix is available.

## Secrets in the repository

If you find a real secret committed:

1. Do not repeat it in a public issue.
2. Report it privately.
3. The maintainer must rotate/revoke it, remove it from the working tree, and decide whether history rewriting is required.
4. Assume any exposed credential is compromised even after deletion.
