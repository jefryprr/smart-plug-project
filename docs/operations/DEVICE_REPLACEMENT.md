# Device Replacement

1. Put the old device in a safe OFF state if possible; do not assume.
2. Revoke ownership/credentials via the API (`POST /devices/{id}/revoke`).
3. Remove the old device from MQTT ACL and broker credentials.
4. Provision the replacement with a new single-use pairing code.
5. Claim the new device with the correct user/home.
6. Verify telemetry, state, diagnostics, and command ACK before use.
7. Archive old device data per retention policy; do not merge counters silently.

## Data continuity

- Energy counters belong to a physical meter/device. Do not sum old and new counters as one continuous meter without a segment boundary.
- Create a new energy counter segment and mark the gap.
- Preserve audit history for the old device.

## Safety

- Replacement does not reset a physical fault/lockout.
- Inspect the installation and enclosure before re-energizing.
- A new device must pass the same safety gates.
