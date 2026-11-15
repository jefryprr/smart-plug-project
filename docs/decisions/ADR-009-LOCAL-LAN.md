# ADR-009 — Local LAN Control

**Status:** Deferred / `NOT_IMPLEMENTED`
**Date:** 2026-11-15
**Related:** Q14=A, Q16=C, FR-014, FR-051

## Context
The device must remain controllable without internet. The PRD forbids unauthenticated LAN endpoints. The current API is cloud/backend-style; no on-device LAN API or local broker gateway exists.

## Decision
- Physical button and local schedule remain the baseline offline controls.
- Do not expose an unauthenticated LAN endpoint.
- Defer the local LAN API/gateway design until the device firmware, provisioning, and TLS/mTLS story are implemented.
- Document that the web/Android app may be offline; it must not claim device state without freshness.

## Consequences
- FR-014/FR-051 are `PARTIAL`, not `PASS`.
- Offline behavior is limited to button/schedule core logic.
- A future ADR must choose authenticated local REST/WebSocket vs local broker/gateway.

## Alternatives
- Local MQTT broker on device: resource/security concerns.
- mTLS local API: possible but needs provisioning.
- Cloud-only: rejected by requirements.
