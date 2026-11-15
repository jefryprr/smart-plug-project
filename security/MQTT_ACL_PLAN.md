# MQTT ACL Plan — REV_A_PROVISIONAL

**Status:** `DESIGN` / production broker not executed.

## Topic matrix

| Topic | Device publish | Device subscribe | Backend publish | Backend subscribe | Retain |
|---|---|---|---|---|---|
| `smartplug/v1/{id}/telemetry` | yes (own) | no | no | yes | no |
| `smartplug/v1/{id}/state` | yes (own) | no | no | yes | yes (reported) |
| `smartplug/v1/{id}/event` | yes (own) | no | no | yes | no |
| `smartplug/v1/{id}/availability` | yes (own) | no | no | yes | yes (LWT) |
| `smartplug/v1/{id}/command` | no | yes (own) | yes | no | **no** |
| `smartplug/v1/{id}/ack` | yes (own) | no | no | yes | no |
| `smartplug/v1/{id}/diag` | yes (own) | no | no | yes | no |
| `smartplug/v1/{id}/config/desired` | no | yes (own) | yes | no | **no** |
| `smartplug/v1/{id}/config/reported` | yes (own) | no | no | yes | yes |

## Rules

1. `device_id` is opaque and validated with `^[A-Za-z0-9_-]{1,64}$`; wildcards are rejected.
2. Device credentials are unique; no shared password.
3. Command and desired-config messages are **never retained** (retained ON is dangerous).
4. ACL must deny cross-device publish/subscribe. Test with valid and invalid clients.
5. QoS: telemetry/diag 0; state/event/availability/ack/command/config 1. Do not claim delivery to the device from broker QoS alone.
6. LWT marks availability `offline`; it does not prove relay OFF.
7. Backend ACL is separate from device ACL; backend cannot be impersonated by a device.

## Test cases (to run when broker/TLS are available)

- [ ] Device A cannot publish to Device B telemetry.
- [ ] Device A cannot subscribe to Device B command.
- [ ] Anonymous connection rejected in production.
- [ ] Expired/revoked credential rejected.
- [ ] Command retained flag is false (broker inspect).
- [ ] Duplicate command ID/sequence rejected by firmware.
- [ ] Broker restart does not replay a stale ON command.

Current dev broker (`mosquitto.dev.conf`) allows anonymous connections. It is **not** production configuration and was not executed in this environment.
