# Provisioning Security — REV_C_PSU_BOARD

**Status:** `DESIGN` / firmware provisioning not implemented.

## 1. Flow (intended)

1. Device boots unprovisioned, relay OFF, BLE/SoftAP window opens for a limited time.
2. User proves physical possession with a single-use code (printed on label or shown on OLED).
3. Device receives Wi-Fi credentials over an authenticated, encrypted channel.
4. Device connects to MQTT using a unique credential.
5. User claims the device in web/Android with the pairing code.
6. Pairing window closes; code is consumed; audit event recorded.

## 2. Threats and controls

| Threat | Control | Status |
|---|---|---|
| Brute-force pairing code | 6–10 digits, rate limit, short expiry, lockout | API partly; firmware pending |
| Replay code | Single-use hash, `claimed_at`, expiry | API implemented/tested |
| Double ownership | Transactional claim, unique device claim | API implemented/tested |
| Rogue AP / MITM | BLE pairing + TLS to backend; verify certificates | Design only |
| QR/code leak | QR contains one-time code, not long-lived secret | Design only |
| SSID/password leak | No logging/telemetry; redact | Design only |
| Unauthorized provisioning | Physical presence + user confirmation | Design only |
| Provisioning while load connected | Require relay OFF and warn; do not auto-ON | Design only |

## 3. SoftAP fallback

- WPA2/3 with unique password, not open.
- Captive portal bound to a short window.
- No internet passthrough.
- Close AP after success/timeout.
- Do not expose API tokens in URLs.

## 4. BLE

- Pairing only in provisioning mode.
- Authenticated characteristic; no plaintext Wi-Fi write.
- Close advertising after window/timeout.
- Test replay/unauthorized pairing.

## 5. Tests required

- [ ] Expired code rejected.
- [ ] Replayed code rejected.
- [ ] Wrong code rate-limited.
- [ ] Double claim rejected.
- [ ] Provisioning window closes.
- [ ] SSID/password absent from logs.
- [ ] Device credential revoked on factory reset.

Current API pairing test: `PASS` for single-use/expiry/replay. Firmware/BLE/SoftAP: `NOT_IMPLEMENTED`.
