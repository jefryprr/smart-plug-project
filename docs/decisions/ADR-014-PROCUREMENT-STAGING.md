# ADR-014 — Prototype Procurement Staging and Budget

**Status:** Proposed (procurement decision, not safety approval)  
**Date:** 2026-11-15  
**Related:** ADR-013, `bom/BOM_PROCUREMENT.csv`, `research/PROCUREMENT_INDONESIA.md`

## Context

The user set a prototype BOM budget of **Rp500.000–750.000**. Dated Indonesian
listing research for 48 BOM lines gives:

- electronics core (MCU, meter, PSU, sensor, isolation, relay, protection,
  passives, protoboard): **Rp526.923**;
- CORE safety/function build including enclosure, connectors, cable, and
  mechanical parts: **Rp756.987** before shipping;
- CORE all-in with an estimated Rp40.000 shipping: **Rp796.987**;
- FULL build adding OLED, RTC, external RGB, and their connectors:
  **Rp895.976** before shipping, **Rp935.976** all-in.

CORE can reach **Rp705.519** (Rp745.519 all-in) only if the ESP32-S3 and PZEM
are bought at EasyWare restock prices (Rp103.500 and Rp135.000). Both were out
of stock on 2026-11-15. Marketplace substitutes are Rp139.968 and Rp150.000.

The user also required that safety not be downgraded to meet budget.

## Decision

1. Split procurement into **CORE** and **FULL** stages.
2. Buy CORE first: PSU, PZEM 100 A CT, relay module, fuse/MOV/TCO, terminals,
   PE, socket/plug, enclosure, ESP32-S3 N16R8, temperature sensor, isolation
   barrier, wiring, and basic UI button.
3. Defer OLED, DS3231 RTC, external WS2812B, level shifter, and their JST
   connectors until CORE passes SELV and initial thermal tests.
4. Prefer EasyWare restock prices for ESP32-S3 and PZEM; if unavailable, accept
   the marketplace price or wait. Do not substitute the PZEM 10 A variant.
5. Keep all safety-critical parts `PENDING_APPROVAL`, `DOCUMENTATION_DEFICIENT`,
   or `BLOCKED`. Price does not imply approval.
6. Do not remove fuse, MOV, thermal cutoff, PE, terminals, enclosure, or the
   UART isolation barrier to fit the budget.

## Consequences

- CORE is **slightly over** the Rp750.000 cap at current marketplace prices
  (Rp796.987 all-in), but fits with restock prices (Rp745.519 all-in).
- FULL is about **25% over** the cap and is a later stage.
- The ESP32-S3 compatible board is an explicit Q08=B deviation; official
  Espressif local stock is not confirmed.
- Prices are listings, not quotes. Stock, tax, and shipping can change.
- The prototype remains `NOT_RELEASED` and `NOT_FOR_FABRICATION`.

## Alternatives

- Increase the budget to ~Rp850.000–950.000 for FULL.
- Build CORE only and use web/serial UI; add display/RTC later.
- Use a cheaper sensor/RTC/enclosure, which changes the design and requires a
  new review; not selected because it does not improve safety.

## Sources

- `bom/BOM_PROCUREMENT.csv` (48 lines, dated 2026-11-15)
- `research/PROCUREMENT_INDONESIA.md`
- `bom/BOM_SUMMARY.json`
