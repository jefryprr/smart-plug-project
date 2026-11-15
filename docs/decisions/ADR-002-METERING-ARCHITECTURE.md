# ADR-002 — Metering Architecture (REV_B)

**Status:** Proposed / `DOCUMENTATION_DEFICIENT`  
**Date:** 2026-11-16  
**Related:** Q09=D, FR-001..005, `research/PZEM_INTERNAL_ISOLATION.md`

## Context

The user selected PZEM-004T V4 with a 100 A CT and directed removal of the
external ADuM1201 + B0505S barrier. The PZEM TTL side is SELV via the module's
internal optocouplers. The exact V4 batch manual, creepage, and isolation
withstand are still not verified. A 100 A CT rating does not authorize 100 A
through the device.

## Decision

- Use **PZEM-004T V4 100 A CT** (closed or split). Closed CT is selected for
  prototype price; split CT is electrically equivalent and easier to install.
- **No external UART isolation barrier.** Use the PZEM internal optocouplers as
  the galvanic barrier.
- Level-shift only:
  - PZEM TX 5 V → 10 kΩ/20 kΩ divider → ESP32 GPIO18 (3.3 V).
  - ESP32 GPIO17 (3.3 V) → 74HCT125 (5 V) → PZEM RX.
- CT clamps around **one conductor only** (line), never the whole cable.
- If the official batch datasheet cannot be obtained, switch to ADE7953 or
  another documented metering front-end after user approval.

## Consequences

- No extra BOM/space for an external barrier; lower cost.
- **Single barrier:** PZEM internal optocoupler/creepage failure can expose the
  ESP32 to mains. Batch inspection and hipot/leakage are mandatory.
- Firmware driver/protocol must be verified, not copied from V3 assumptions.
- Metering readings remain `UNVERIFIED` until physical calibration.
- The final 8 A rating is limited by the relay/rating chain, not the CT.

## Alternatives

- PZEM V3: older docs, not a substitute for V4 evidence.
- ADE7953 + CT: more design/calibration but better traceability.
- HLW8032 + shunt: shunt carries load, thermal/isolation concerns.
- Restore ADuM1201 + B0505S as a future redundant barrier; requires a new
  schematic/PCB revision.
