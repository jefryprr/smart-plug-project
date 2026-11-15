# ADR-003 — Switching and Two-Pole Disconnection (Amended)

**Status:** Accepted direction; component/rating `PROVISIONAL`
**Date:** 2026-11-15 (amended after user instruction)
**Related:** Q03=8 A final, Q05=A (two-pole review), Q10=2-channel optocoupler relay module.

## Context
The user changed the rating from target 10 A to **8 A final** and selected a
**common 2-channel 5 V optocoupler relay module**, mounted off-board in the
enclosure. This is a change from the earlier TE RT2 DPST-NO PCB relay concept.
The module is typically two independent SPDT relays, not a mechanically linked
DPST. It must not be treated as a safety-rated two-pole disconnect without
evidence.

## Decision
- Use a **2-channel 5 V optocoupler relay module**, off-board, with mechanical
  mounting in the enclosure.
- Channel 1 switches **L**, channel 2 switches **N**. PE remains continuous and
  is never switched.
- Module inputs are assumed **active-LOW** (common module); a MOSFET on the
  carrier pulls both IN1/IN2 low when commanded ON. At boot the MOSFET is off
  (pulldown), so module inputs are high and relays are OFF.
- Final continuous rating: **8 A / ~1.840 W at 230 V**, limited to
  electronics/SMPS loads. No heaters, kettles, irons, hair dryers, or large
  motors.
- Do not label the module as DPST, safety-rated, or mechanically linked.
- If the module cannot be verified or one channel welds, the design remains
  `ENGINEERING_REVIEW_REQUIRED`; do not claim two-pole safety.

## Consequences
- Module is larger than a PCB relay and needs a bracket/standoff, cable routing,
  and clearance from PZEM/PSU.
- Two independent channels reduce some single-channel failure modes but are not
  a guarantee of simultaneous opening.
- The module's 10 A claim is not a validated 8 A continuous rating; thermal and
  lifecycle tests are required.
- The optocoupler isolates coil/input, but the module PCB may not provide mains
  creepage; keep it in the mains zone, off the SELV carrier.
- `observed_output` remains null; no contact feedback.

## Alternatives
- TE RT2 DPST-NO 8 A PCB relay: better mechanical linkage, smaller, but changed
  by user instruction.
- 2P 16 A contactor: larger, better rating, requires enclosure change.
- Two separate relays: rejected as not mechanically linked.

## Sources
- Handsontec 2-channel 5 V optical isolated relay module datasheet (10 A class,
  low-level input, 15–20 mA/channel): `research/datasheets/handsontec_2ch_relay.pdf`.
- DigiKey TS0010D 2-channel relay module datasheet:
  `research/datasheets/digikey_ts0010d_2ch_relay.pdf`.
- Envistia product documentation (active-LOW, JD-VCC jumper; availability/candidate
  source, not a safety certificate).
