# Key Rotation

| Secret | Rotation trigger | Procedure |
|---|---|---|
| JWT signing secret | Suspected leak, scheduled | Rotate, invalidate sessions, redeploy, verify login |
| Refresh tokens | Logout/leak | Revoke session rows; rotate on refresh |
| Device MQTT credentials | Device replacement/leak | Revoke credential, issue new, update broker ACL |
| Telegram bot token | Leak/change | Revoke via BotFather, update secret store, test |
| TLS certificate | Expiry/leak | Renew via ACME/manual, reload proxy |
| Database password | Leak/scheduled | Rotate role password, update secret, restart API |
| Firmware signing key | Compromise | Offline procedure, revoke release, publish new key |

## Rules

- Never put secrets in git, logs, telemetry, screenshots, or chat.
- Rotate one secret at a time and verify service health.
- After rotation, test negative auth and ACL cases.
- Record rotation date, owner, and affected services.
