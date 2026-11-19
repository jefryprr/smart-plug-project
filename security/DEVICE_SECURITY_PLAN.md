# Device Security Plan — REV_D_CORE_ONLY

**Status:** `DRAFT`
**Scope:** ESP32-S3 device identity, boot, storage, provisioning, OTA, debug.

## 1. Identity and credentials

- Each device must have a unique credential; no shared Wi-Fi/broker password.
- Credential hash stored in backend; device secret never logged.
- Revocation/rotation procedure required before production.
- Pairing code is single-use, expiring, and hashed at rest.
- QR code must not contain a reusable secret.

## 2. Boot and fail-safe

- Relay GPIO forced OFF at boot; external pulldown required.
- `BOOT_SAFE` rejects ON until meter/temperature validity is established.
- Brownout/reset must not energize the relay.
- Boot reason and reset count logged.
- OTA/bootloader must not enable load.

## 3. Flash/secure boot decision

| Control | Status | Note |
|---|---|---|
| Secure Boot v2 | `NOT_ENABLED` | Irreversible eFuse; requires explicit approval, recovery plan, fixture |
| Flash encryption | `NOT_ENABLED` | Irreversible; requires approval and key management |
| NVS encryption | `NOT_ENABLED` | Planned with key partition |
| Anti-rollback eFuse | `NOT_ENABLED` | Requires release process |
| Debug UART/USB | `RESTRICTED_DOCS_ONLY` | No physical interlock implemented |

No eFuse is burned by this project. A destructive/irreversible action requires explicit user approval and a recovery plan.

## 4. Provisioning

- BLE + SoftAP fallback (Q15=C), limited window, unique password, authenticated.
- Pairing requires proof of possession (code) and single ownership.
- Do not write SSID/password to logs/telemetry/analytics.
- Factory reset clears credentials/binding but not physical fault/lockout.

## 5. Network

- Wi-Fi 2.4 GHz; exponential backoff+jitter; local functions continue offline.
- MQTT TLS with certificate validation in production; no insecure TLS disable.
- Per-device topic ACL; no wildcard subscriptions.

## 6. OTA

- Dual OTA partitions; rollback enabled; HTTPS only.
- Signed image and version compatibility required before release.
- Output remains OFF during update unless an approved policy says otherwise.
- Key stored offline/secret manager, never in repo.

## 7. Logging/diagnostics

- Redact tokens, passwords, SSID, pairing codes.
- Diagnostics expose firmware version/hash, sensor health, counters, but no secrets.
- Audit events immutable at application layer.

## 8. Open items

- [ ] Secure boot/flash encryption decision.
- [ ] Device credential provisioning/rotation.
- [ ] Signed OTA implementation and rollback test.
- [ ] Physical debug protection.
- [ ] Factory reset procedure and test.
- [ ] Threat-model review by security engineer.
