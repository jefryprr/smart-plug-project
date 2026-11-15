# ADR-012 — No Irreversible eFuse/Secure Boot Action Without Approval

**Status:** Accepted
**Date:** 2026-11-15
**Related:** FR-071, security plan

## Context
Secure boot, flash encryption, and anti-rollback eFuses are irreversible. A mistake can brick devices or block recovery. The project has no hardware/fixture and no user approval for irreversible steps.

## Decision
- Do **not** burn eFuses, enable secure boot, enable flash encryption, or set anti-rollback in this execution.
- Provide a security plan and config flags only.
- Require explicit user approval, recovery plan, hardware fixture, and engineering test before any irreversible action.

## Consequences
- Firmware integrity/OTA security is `PARTIAL`, not production-ready.
- A future release must decide and test the irreversible path.
- No key is stored in the repo.

## Alternatives
- Enable secure boot now: rejected (no hardware/recovery/approval).
- Ignore security: rejected by PRD.
