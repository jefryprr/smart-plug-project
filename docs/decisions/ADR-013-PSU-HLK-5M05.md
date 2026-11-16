# ADR-013 — PSU Selection: Hi-Link HLK-5M05

**Status:** Accepted (user-selected), component `PENDING_APPROVAL`
**Date:** 2026-11-15
**Supersedes:** Mean Well IRM-05-5 selection in the prototype BOM

## Context

The prototype needs a 5 V SELV rail for the ESP32-S3, display, sensors, and the
off-board 2-channel relay module. The previous choice was the Mean Well
IRM-05-5 (5 V / 1 A / 5 W, ~53.5 × 28.5 × 19 mm, ~78% efficiency).

The user instructed replacement with the **Hi-Link HLK-5M05**: 5 V / 1 A / 5 W,
**38 × 23 × 18 mm**, four pins, 90–264 VAC input. It is smaller and cheaper, but
its datasheet efficiency is only ~70% at 220 V full load and its certification
is weaker.

## Decision

- Use **HLK-5M05** as the prototype PSU, mounted on the separate **REV_C PSU board** in the mains zone (50 x 65 mm, TB1/TB2, fuse/MOV/TCO, 3x JST 5 V outputs).
- Keep the Mean Well IRM-05-5 as the fallback if thermal/isolation review fails.
- Treat the PSU as `PENDING_APPROVAL`, not as a certified isolation barrier.
- Require batch certificate/pin marking, ripple/startup/load, temperature rise,
  hipot/leakage, and creepage review before approval.
- Keep fuse, MOV, and thermal cutoff upstream on the same PSU board; the PSU is not a substitute. PE stays on a dedicated chassis stud, not on the PSU board.

## Consequences

- Footprint shrinks from ~53.5 × 28.5 × 19 mm to 38 × 23 × 18 mm, freeing space.
- Heat rises from ~1.4 W to **~2.1 W at 5 W output** (70% efficiency). Enclosure
  thermal margin is reduced; the 60 °C case limit needs measurement.
- Isolation is only a datasheet claim (2500 VAC). The official page does not
  expose a batch certificate; the local datasheet is a 3-page distributor copy.
- The 1 A output has ~42% margin against the estimated 0.58 A peak, but this is
  not measured. Wi-Fi bursts and relay inrush still need bench verification.
- The mains creepage around the four-pin module must be reviewed; AC and DC pins
  are close together.

## Alternatives

- **Mean Well IRM-05-5**: better documentation and thermal margin, larger and
  more expensive. Fallback.
- **Recom RAC01-05SC**: only 0.2 A, rejected.
- **Hi-Link HLK-PM01**: 0.6 A, documentation/batch quality weaker; rejected for
  this load budget.
- **Mean Well IRM-10-5**: 2 A, larger; possible if thermal margin is needed.

## Sources

- Official product/docs page: https://www.hlktech.net/index.php?id=1243
- Local distributor datasheet: `research/datasheets/hlk-5m05_distributor.pdf`
- Full study: `research/PSU_HLK_5M05.md`
- Indonesian listing: Shopee / Marnov Electronic Rp49.000 (2026-11-15); CNC Store Bandung Rp63.300 out of stock.

**Safety:** this ADR records a user-selected prototype part. It is not a safety
approval or a production release.
