# ADR-006 — Android Stack

**Status:** Accepted (Q24=A)
**Date:** 2026-11-15

## Context
The Android app needs API login, device list, ON/OFF with ACK, readings, schedules, and future BLE provisioning/push. Expo Go cannot access every native module.

## Decision
- **React Native + Expo SDK 58** with a development build/prebuild.
- SecureStore for the access token.
- Local TypeScript types mirror the API contract; shared package bundling is not configured for Metro.
- Debug APK build is `PASS` (`arm64-v8a`, v2 debug signature); it is not installed/tested on a device, not release-signed, and not a production artifact.

## Consequences
- `npx expo export --platform android` succeeds (596 modules).
- No APK/emulator test; no BLE/push implementation.
- Android app uses the same REST API and error semantics as web.
- A future dev build can add BLE/push without Expo Go constraints.

## Alternatives
- RN CLI/bare: more native control but more setup; deferred.
- Expo Go only: rejected for native BLE/push limits.
