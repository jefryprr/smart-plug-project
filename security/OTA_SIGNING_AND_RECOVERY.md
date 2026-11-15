# OTA Signing and Recovery — REV_A_PROVISIONAL

**Status:** `DESIGN_ONLY` / `BLOCKED`
**Why:** ESP-IDF toolchain not installed; no signed image or rollback test was performed.

## 1. Requirements

- Dual OTA partitions (`ota_0`, `ota_1`) and `otadata`.
- HTTPS-only download with certificate validation; no insecure TLS.
- Image integrity via SHA-256/signature; version compatibility check.
- Anti-rollback policy must be explicit; eFuse anti-rollback is irreversible and requires approval.
- Output remains OFF during update (or approved fail-safe policy).
- Rollback on boot failure; retain a recovery path (USB/serial or factory partition).
- Signing key in offline/secret manager, never in repo.
- Release metadata: version, channel, hash, signature, min version, notes.

## 2. Current configuration

`firmware/sdkconfig.defaults` sets:
- `CONFIG_APP_ROLLBACK_ENABLE=y`
- `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE=y`
- `CONFIG_ESP_HTTPS_OTA_ALLOW_HTTP=n`
- `CONFIG_ESP_HTTPS_OTA_CHECK_CERT=y`
- 16 MB flash, dual 6 MB app partitions.

These are configuration only. No build/test evidence exists.

## 3. Image verification (planned)

1. Build reproducibly from a tagged commit.
2. Compute SHA-256.
3. Sign the image/hash with an offline key.
4. Publish release metadata; API verifies signature and channel.
5. Device verifies signature before marking the image bootable.
6. Device reports version/hash in telemetry/diagnostics.
7. On failure, bootloader rolls back; relay stays OFF.

## 4. Recovery

- USB/serial recovery must not require opening a mains-energized enclosure.
- Factory partition or ROM download mode procedure documented.
- If secure boot/flash encryption is enabled, recovery keys and eFuse plan must be tested first.
- Never rely on OTA to fix a device that is physically unsafe.

## 5. Tests (blocked)

- [ ] Valid signed image updates and boots.
- [ ] Corrupted image rejected.
- [ ] Wrong signature rejected.
- [ ] Downgrade rejected (or explicitly allowed with policy).
- [ ] Power loss during update rolls back.
- [ ] Watchdog/reboot does not turn load ON.
- [ ] Release key rotation.

**Conclusion:** OTA is not implemented beyond partition/config and an API request event. No production OTA claim.
