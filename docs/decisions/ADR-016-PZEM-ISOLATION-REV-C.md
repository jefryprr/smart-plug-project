# ADR-016 — PZEM Isolation Basis for REV_C

**Status:** Accepted as design basis; batch/assembly isolation `UNVERIFIED`  
**Date:** 2026-11-16  
**Supersedes:** REV_C_PSU_BOARD external ADuM1201 + B0505S requirement; clarifies REV_C_PSU_BOARD/REV_C
**Related:** ADR-002, `research/PZEM_INTERNAL_ISOLATION.md`, `safety/ISOLATION_PLAN.md`

## Context

The repository contains two conflicting PZEM UART isolation statements:

1. **REV_C_PSU_BOARD:** external ADuM1201 + B0505S barrier required; PZEM must not share
   SELV ground.
2. **REV_C_PSU_BOARD:** external barrier removed; PZEM internal optocouplers are the
   barrier; PZEM TTL side is powered from SELV 5 V and shares SELV ground.

This conflict must be closed before the PSU board defines the third 5 V output.
The user selected the PZEM-004T V4 and directed removal of the external barrier.
The module family uses optocouplers between the mains/measurement side and the
TTL side, but the purchased V4 batch, creepage, and withstand are not verified.

## Decision

- **REV_C uses the PZEM-004T V4 internal optocouplers as the only UART
  galvanic barrier.**
- No ADuM1201 and no B0505S are fitted in REV_C.
- PZEM TTL 5 V/GND may be supplied from **PSU OUT3** (JST-XH 2-pin), because the
  TTL side is SELV when the internal isolation is intact.
- PZEM TX/RX go to the carrier J2 level-shift/divider; the carrier remains
  SELV-only and has no mains.
- **OUT3 is conditional:** it is labeled `PROVISIONAL` until the purchased batch
  is inspected for optocouplers/creepage and passes a mains-to-TTL
  hipot/leakage test. If the batch fails, OUT3 must be reworked to an isolated
  B0505S/ADuM barrier and PZEM must **not** be fed directly from the PSU board.
- REV_C_PSU_BOARD external-barrier statements are historical and **superseded** for
  REV_C. They are not an alternative build inside the same revision.

## Consequences

- Single barrier: a PZEM internal failure can expose the ESP32/carrier to mains.
- PZEM batch inspection, creepage review, and hipot/leakage are safety-critical.
- PZEM 5 V/GND and TTL share SELV ground by design; do not add a second ground
  reference or an external isolated supply in REV_C.
- The PSU board OUT3 must be clearly labeled and controlled; do not use it for
  an unknown module.
- USB must not be connected while mains is energized.

## Alternatives

- **External ADuM1201 + B0505S:** safer second barrier, but the user removed it;
  would require a new carrier/PSU revision, isolated 5 V, and different wiring.
- **ADE7953 or another documented metering front-end:** more traceable, but
  requires a new design and calibration.
- **No PZEM / external meter:** not selected.

## Evidence

- Tasmota PZEM documentation (RX optocoupler series resistor).
- Components101 PZEM-004T block diagram (optocoupler).
- Community reverse-engineered PZEM-004T schematics.
- `research/PZEM_INTERNAL_ISOLATION.md`.

## Status

`ACCEPTED_AS_DESIGN_INPUT` for REV_C. This is **not** a safety approval. PZEM
batch and assembly remain `DOCUMENTATION_DEFICIENT` until inspected and tested.
