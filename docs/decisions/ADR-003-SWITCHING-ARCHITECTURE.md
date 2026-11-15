# ADR-003 — Switching and Two-Pole Disconnection

**Status:** Proposed / rating lower than target
**Date:** 2026-11-15
**Related:** Q03=B (10 A target), Q05=A (review two-pole), Q10=C

## Context
Type F plugs are reversible, so a single-pole switch can leave a live conductor. The target is 10 A, but the provisional DPST-NO relay (TE RT2 class) is 8 A / 250 VAC IEC class. A latching relay is not fail-safe.

## Decision
- Review **two-pole disconnection** (L and N) with PE continuous.
- Provisional relay: **TE RT2 `RT444005` DPST-NO, 5 V coil, 8 A class**, pending exact MPN/rating verification.
- Final continuous rating: **8 A or lower** after thermal/derating; do not label 10 A.
- Reject single SPDT, two unlinked relays, and latching relays as the sole disconnect.
- If 10 A must be retained, use a 2P 16 A contactor and a larger enclosure (Q06=C) after approval.

## Consequences
- Target 10 A is not met by the provisional relay.
- Thermal/lifecycle/inrush tests are required.
- PE never goes through the relay/fuse.
- Firmware cannot claim physical OFF without contact feedback.

## Alternatives
- Omron G2R-2A (5 A): lower rating.
- Schneider Acti9 iCT 2P 16 A: safer rating but large/DIN.
- Two G5LE-1A: not mechanically linked; rejected for two-pole safety.
