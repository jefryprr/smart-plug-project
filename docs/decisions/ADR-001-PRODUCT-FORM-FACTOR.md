# ADR-001 — Product Form Factor and Safety Scope

**Status:** Accepted (user decisions Q01=B, Q12=A)
**Date:** 2026-11-15

## Context
The user wants an ESP32-S3 inline smart outlet, not a wall-mounted mini plug, and chose a supervised academic lab prototype as the safety/use target.

## Decision
- Form factor: **inline corded outlet** with a Type F/E-F socket (Q02 analysis pending).
- Safety scope: **academic lab prototype**, supervised, not a consumer product.
- Target enclosure: 150×100×70 mm (original Q06=B) **fails**; 180×120×70 was **rejected** because PZEM/relay/socket only fit by stacking with an inadequate gap. **220×120×70 is CONFIRMED** by the user on 2026-11-15 (Q06=C).
- No `READY_FOR_USE` or `READY_FOR_FABRICATION` claim.

## Consequences
- More room for PZEM/relay/PSU than a wall plug.
- Mains cable, gland, strain relief, and PE are mandatory.
- Consumer certification/regulatory claims are out of scope.
- All physical tests remain `BLOCKED` until lab/personnel exist.

## Alternatives
- Wall plug (Q01=A): rejected for prototype serviceability/space.
- Consumer product (Q12=C): rejected without regulatory/engineering capacity.
