# ADR-002 — Metering Architecture

**Status:** Proposed / `DOCUMENTATION_DEFICIENT`
**Date:** 2026-11-15
**Related:** Q09=D, FR-001..005

## Context
The user requested PZEM-004T V4 Open CT but allowed comparison. The exact V4 batch manual, UART levels, isolation, and CT interface are not verified. A 100 A CT rating does not authorize 100 A through the device.

## Decision
- Keep **PZEM-004T V4 100 A CT (closed or split)** as the provisional candidate. Closed CT is selected for prototype price; split CT remains electrically equivalent and easier to install.
- Require an external **UART isolation barrier** (`ADuM1201` + `B0505S-1WR3`) until the module's isolation and UART levels are proven for the purchased batch.
- CT clamps around **one conductor only** (line), never the whole cable.
- If the official batch datasheet cannot be obtained, switch to ADE7953 or another documented metering front-end after user approval.

## Consequences
- Extra BOM/space for the barrier.
- Firmware driver/protocol must be verified, not copied from V3 assumptions.
- Metering readings remain `UNVERIFIED` until physical calibration.
- The final 8 A rating is limited by the relay/rating chain, not the CT.

## Alternatives
- PZEM V3: older docs, not a substitute for V4 evidence.
- ADE7953 + CT: more design/calibration but better traceability.
- HLW8032 + shunt: shunt carries load, thermal/isolation concerns.
