# ADR-014 — Prototype Procurement Staging and Budget (REV_C_PSU_BOARD)

**Status:** Proposed (procurement decision, not safety approval)  
**Date:** 2026-11-16  
**Related:** ADR-002, ADR-013, `bom/BOM_PROCUREMENT.csv`, `research/PROCUREMENT_INDONESIA.md`

## Context

The user set a prototype BOM budget of **Rp500.000–750.000**. Dated Indonesian
listing research for 57 BOM lines gives:

- electronics core (MCU, meter, PSU, level shift, relay, protection, passives,
  PCB): **Rp433.633**;
- CORE safety/function build including enclosure, connectors, cable, and
  mechanical parts: **Rp717.087** before shipping;
- CORE all-in with an estimated Rp40.000 shipping: **Rp757.087** — under the cap;
- CORE with EasyWare restock prices for ESP32-S3 and PZEM: Rp665.619
  (Rp705.619 all-in);
- FULL build adding OLED, RTC, external RGB, and their connectors:
  **Rp834.687** before shipping, **Rp874.687** all-in.

REV_C_PSU_BOARD removes the **TMP102** and the external **ADuM1201 + B0505S** barrier.
The PZEM-004T V4 internal optocouplers are the galvanic barrier; the carrier
only level-shifts the 5 V TTL UART. There is no firmware temperature sensor;
thermal protection is hardware-only (fuse + one-shot TCO).

## Decision

1. Split procurement into **CORE** and **FULL** stages.
2. Buy CORE first: PSU, PZEM 100 A CT, relay module, fuse/MOV/TCO, terminals,
   PE, socket/plug, enclosure, ESP32-S3 N16R8, 74HCT125 level shift, wiring,
   and basic UI button.
3. Defer OLED, DS3231 RTC, external WS2812B, and their JST connectors until
   CORE passes SELV and initial thermal tests.
4. Prefer EasyWare restock prices for ESP32-S3 and PZEM; if unavailable, accept
   the marketplace price. CORE still fits at marketplace prices.
5. Keep all safety-critical parts `PENDING_APPROVAL`, `DOCUMENTATION_DEFICIENT`,
   or `BLOCKED`. Price does not imply approval.
6. Do not remove fuse, MOV, TCO, PE, terminals, enclosure, relay rating, or
   PZEM internal-isolation review to fit the budget.
7. Do not add a firmware temperature requirement: no sensor is installed.

## Consequences

- CORE is **over** the Rp750.000 cap at current marketplace prices (Rp717.087 + shipping = Rp757.087 all-in). The mechanical addendum raises it to ~Rp785.087; EasyWare restock + addendum is ~Rp733.619, under the cap.
- FULL is about **14% over** the cap and is a later stage.
- The ESP32-S3 compatible board is an explicit Q08=B deviation; official
  Espressif local stock is not confirmed.
- PZEM internal isolation is a **single barrier**. Creepage, batch quality, and
  hipot/leakage must be reviewed; USB must not be connected while mains is live.
- Removing the temperature sensor increases residual thermal risk. The TCO,
  fuse, enclosure thermal test, and load test become mandatory.
- Prices are listings, not quotes. Stock, tax, and shipping can change.
- The prototype remains `NOT_RELEASED` and `NOT_FOR_FABRICATION`.

## Alternatives

- Increase the budget to ~Rp850.000–900.000 for FULL.
- Build CORE only and use web/serial UI; add display/RTC later.
- Restore a temperature sensor (TMP102/MCP9808/DS18B20) and external UART
  isolation as a future safety revision; this adds cost and requires a new
  schematic/PCB revision.

## Sources

- `bom/BOM_PROCUREMENT.csv` (57 lines, dated 2026-11-15/16)
- `research/PROCUREMENT_INDONESIA.md`
- `bom/BOM_SUMMARY.json`
- `research/PZEM_INTERNAL_ISOLATION.md`
