# Threat Model — REV_D_CORE_ONLY

**Status:** `DRAFT` / `ENGINEERING_REVIEW_REQUIRED`
**Scope:** device, local network, MQTT, backend API, web, Android, OTA, deployment.
**Out of scope:** formal penetration test, third-party cloud, physical lab attack, regulatory certification.

## 1. Assets

| Asset | Impact if compromised |
|---|---|
| Device MQTT credentials | Unauthorized telemetry/commands, cross-device access |
| Device identity / pairing code | Device takeover, false ownership |
| User password / session / refresh token | Account takeover, unauthorized ON/OFF |
| MQTT broker / ACL | Spoofed commands, data leak |
| Firmware signing key | Malicious OTA, persistent compromise |
| Telemetry/energy data | Privacy leak, billing disputes |
| Tariff/budget/automation config | Wrong cost, unexpected switching |
| Audit/event log | Loss of accountability |
| Physical debug/UART | Firmware extraction, command injection |

## 2. Actors and trust boundaries

| Actor | Trust | Notes |
|---|---|---|
| Homeowner/user | Authenticated, role-scoped | Can be malicious or compromised |
| Device | Authenticated via unique credential | Physical access may be attacker-controlled |
| Backend API | Trusted service | Must enforce all authorization |
| MQTT broker | Trusted transport with ACL | Dev broker is anonymous; prod must be TLS+ACL |
| Web/Android client | Untrusted input | Never enforce authorization only in UI |
| LAN attacker | Untrusted | LAN is not a trust boundary |
| Cloud/provider | External | TLS, least privilege, no secret sharing |
| Supply chain | Untrusted | Dependencies, firmware, libraries |

## 3. Attack trees (summary)

### 3.1 Unauthorized ON/OFF
- Steal access token → replay command.
- Reuse idempotency key / command ID → duplicate ON.
- Publish directly to MQTT command topic → spoof device command.
- Bypass lockout via API/cloud.
- Retained ON command replayed after reconnect.

**Controls:** short-lived JWT, refresh rotation, rate limit, RBAC/tenant checks, command TTL/sequence/replay, non-retained command, lockout enforced in API + firmware, MQTT ACL, audit. **Residual:** cloud/API compromise, stolen device credential.

### 3.2 MITM
- Rogue AP during provisioning.
- Plain MQTT on LAN.
- Invalid TLS certificate accepted.

**Controls:** BLE/SoftAP window, unique code, TLS verification config, no insecure TLS disable in production, certificate validation. **Residual:** dev broker is anonymous; no live TLS test.

### 3.3 Pairing takeover
- Brute-force 6-digit code.
- Replay claim.
- Double ownership.
- QR/code leak.

**Controls:** single-use hash, expiry, rate limit, claim transaction, audit. **Residual:** no hardware proof-of-possession; 6-digit entropy is limited.

### 3.4 Session/token theft
- XSS/CSRF.
- localStorage theft.
- Refresh replay.

**Controls:** sessionStorage on web, httpOnly not used for API token, refresh rotation/revoke, CORS, helmet headers, no token logging. **Residual:** XSS in web app would expose sessionStorage; CSP is basic.

### 3.5 MQTT ACL/wildcard leak
- Device subscribes to `#` or another device's topic.
- Retained command attack.

**Controls:** topic builder, ACL template, no wildcard device ID, command non-retained, QoS policy. **Residual:** broker config not executed/tested in production.

### 3.6 OTA
- Unsigned/malicious image.
- Downgrade.
- Boot loop/relay ON.

**Controls:** dual partitions, rollback config, HTTPS-only OTA, planned signature, default OFF. **Residual:** no signed image/build/test; secure boot/flash encryption not enabled.

### 3.7 Secret leakage
- Hardcoded Wi-Fi password/token.
- Logs/screenshots.
- `.env` committed.

**Controls:** `.gitignore`, `.env.example`, logger redaction, no secrets in fixtures. **Residual:** provider tokens not configured; future operator error.

### 3.8 DoS / data growth
- Telemetry flood.
- Notification spam.
- Large analytics queries.

**Controls:** rate limit, bounded query range, dedup, outbox, pagination. **Residual:** no load test, no per-device quota.

### 3.9 Physical/debug
- UART/USB access while mains connected.
- Firmware extraction.
- Factory reset abuse.

**Controls:** service cover, isolation plan, debug restriction, reset procedure. **Residual:** no hardware interlock, no secure boot.

## 4. Trust boundary diagram

```
[User browser/app] --HTTPS--> [Reverse proxy] --> [API] --TLS--> [MQTT] <--TLS--> [Device]
        |                              |                    |
        |                              +--> [PostgreSQL]    +--> [Telemetry/commands]
        |                              +--> [Notification provider]
        +-- untrusted input ------------------------------> API validation/authz
```

## 5. Security requirements mapping

| Requirement | Control | Evidence | Status |
|---|---|---|---|
| FR-073 | scrypt, JWT, refresh rotation | API tests | PASS (software) |
| FR-074 | RBAC + tenant scoping | API tests | PASS (software) |
| FR-075 | TLS config, no insecure disable | docs/config | PARTIAL |
| FR-076 | single-use pairing | API test | PASS |
| FR-077 | command validation | core/domain/API tests | PASS |
| FR-078 | audit log | API tests | PASS |
| FR-069/070/071 | OTA/rollback/integrity | config only | PARTIAL/BLOCKED |
| FR-072 | watchdog | config only | PARTIAL |

## 6. Residual risks

- Physical mains safety is not a software problem and remains `BLOCKED`.
- No production TLS/MQTT ACL execution.
- No independent penetration test.
- No secure boot/flash encryption decision.
- No signed OTA artifact.
- Android APK/push not built/tested.
- SQLite dev adapter is not the production database; Postgres adapter missing.

**Conclusion:** digital security controls are partially implemented and tested. The system is **not** production-secure or safety-certified.
