# ADR-015 — DevKitC-1 Socket Interface (Two 1×22, 22.86 mm)

**Status:** Accepted (digital correction; physical fit still required)  
**Date:** 2026-11-16  
**Related:** ADR-008, `hardware/kicad/smartplug.kicad_pcb`, `hardware/carrier/netlist.csv`

## Context

The first REV_C_PSU_BOARD carrier used a single `PinSocket_2x22_P2.54mm_Vertical`
footprint. That footprint has two rows **2.54 mm apart**. It is an IDC-style
2×22 socket, not a DevKitC-1 socket.

Espressif's official ESP32-S3-DevKitC-1 v1.1 DXF puts the two header rows at
X = 1.27 mm and X = 24.13 mm: **22.86 mm apart** (9 × 2.54 mm). Each side is a
separate **1×22** header, J1 and J3. A 2.54 mm-row socket cannot physically
accept the board.

## Decision

- Use **two 1×22 female sockets**, one for DevKit J1 (`J1A`) and one for J3
  (`J1B`), with **22.86 mm row spacing**.
- Header pin numbers in the carrier netlist refer to the official J1/J3 tables,
  not odd/even IDC numbering:
  - J1A pin 1/2 = 3V3, pin 4 = GPIO4, pin 5 = GPIO5, pin 7 = GPIO7,
    pin 10 = GPIO17, pin 11 = GPIO18, pin 12 = GPIO8, pin 15 = GPIO9,
    pin 16 = GPIO10, pin 21 = 5V, pin 22 = GND.
  - J1B pin 1/21/22 = GND; other J3 pins are unconnected.
- Place pin 1 of both sockets at the left end and mark the **USB end** at the
  right end of the carrier.
- Keep the carrier SELV-only; mains modules remain off-board.

## Consequences

- Carrier footprint count changes from 21 to **22** (two sockets instead of one).
- The previous `2x22` BOM line becomes one 2×22 strip split into two 1×22 rows
  (or two 1×22 strips). Price is unchanged within estimate.
- DRC is **0 violations / 0 unconnected** at 0.15 mm; routing is F.Cu with a
  continuous B.Cu GND zone.
- Physical fit, socket height, insertion force, and reverse-insertion keying are
  still `HARDWARE_VALIDATION_REQUIRED`.
- Reverse insertion can put 5 V/3.3 V onto GPIOs and destroy the DevKit. Mark
  pin 1/USB end and add a key or blocker before use.

## Evidence

- Espressif ESP32-S3-DevKitC-1 v1.1 user guide, Header Block (J1/J3 1×22 tables).
- Espressif DXF `DXF_ESP32-S3-DevKitC-1_V1.1_20220429.dxf`: header pad rows at
  X = 1.27 mm and 24.13 mm; each row has 22 pads at 2.54 mm pitch.
- `hardware/carrier/netlist.csv` and `reports/kicad/carrier_drc.json`.

## Alternatives

- 2×22 IDC socket: rejected — 2.54 mm row spacing, physically incompatible.
- Two 1×22 pin headers (male): rejected — the DevKit has male pins; female
  sockets are required.
- Ribbon cable/IDC adapter: rejected for the carrier; adds a non-keyed interface
  and does not solve the row spacing.
