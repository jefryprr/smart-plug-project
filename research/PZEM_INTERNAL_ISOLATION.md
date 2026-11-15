# PZEM-004T Internal Isolation — Evidence and Limits

**Date:** 2026-11-16  
**Status:** `ACCEPTED_AS_DESIGN_INPUT` / `ASSEMBLY_HIPOT_STILL_REQUIRED`  
**Decision:** Remove external ADuM1201 + B0505S; use the PZEM module's internal
optocouplers as the UART galvanic barrier.

## 1. Why the external barrier was removed

The PZEM-004T V3/V4 TTL interface is not a direct mains-referenced UART. The
module uses optocouplers between the mains/measurement side and the TTL side.
The TTL side is powered by the host 5 V and is SELV relative to mains when the
module's internal isolation is intact.

Evidence:

- Tasmota PZEM documentation explicitly discusses the **RX optocoupler series
  resistor** and its 5 V design value:
  https://tasmota.github.io/docs/PZEM-0XX/
- Components101 PZEM-004T functional block diagram shows an **optocoupler**
  between the AC measurement side and the TTL output:
  https://components101.com/modules/pzem-004t-energy-meter-module-pinout-datasheet
- Community reverse-engineering/schematics show optocouplers on the UART:
  https://github.com/TheHWcave/Peacefair-PZEM-004T-

The ADuM1201 + B0505S added a second barrier, but it also added cost, space, and
a floating PZEM-side supply. The user directed removal. The PZEM internal
barrier is now the only galvanic barrier for UART.

## 2. What is still required

The internal optocouplers are a **component-level** isolation feature, not a
certificate for the assembled product. Before mains use:

1. Verify the purchased V4 batch has the expected optocouplers and creepage.
2. Inspect the PZEM PCB for contamination, solder bridges, and damaged parts.
3. Perform hipot/leakage test between mains terminals and the TTL side.
4. Keep the PZEM in the mains zone; keep the TTL cable short and away from
   mains wiring.
5. Do not connect USB to the ESP32 while mains is energized.
6. Treat a damaged/ counterfeit PZEM as a mains hazard, not a cheap module.

## 3. Level shifting (not isolation)

The TTL side is 5 V. The ESP32-S3 is 3.3 V.

- **PZEM TX (5 V) → ESP32 RX (3.3 V):** 10 kΩ series + 20 kΩ to GND divider
  (≈3.33 V). Add 100 nF at the ESP32 pin if noise is observed.
- **ESP32 TX (3.3 V) → PZEM RX (5 V):** 74HCT125 powered from 5 V. The 74HCT
  input threshold is TTL-compatible; the output swings 5 V.
- **PZEM VCC/GND:** 5 V/GND from the carrier. The TTL side is SELV via the
  internal optocouplers.
- **No ADuM1201, no B0505S.**

## 4. Consequences

- Single barrier: if the PZEM optocouplers or creepage fail, mains can reach
  the ESP32. The PZEM batch and assembly must be treated as safety-critical.
- The 5 V/GND connection means the TTL side is not floating relative to the
  ESP32; that is intended because the isolation is inside the PZEM.
- The carrier PCB is SELV-only; mains terminals remain off-board.

## 5. Status

`ACCEPTED_AS_DESIGN_INPUT` for the prototype, but **not** a safety approval.
The assembly remains `ENGINEERING_REVIEW_REQUIRED` and
`HARDWARE_VALIDATION_REQUIRED` until hipot/leakage and creepage review pass.
