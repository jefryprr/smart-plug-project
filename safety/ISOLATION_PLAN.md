# Isolation Plan — REV_B

**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW`  
**Prinsip:** mains dan SELV tidak boleh tercampur. Optocoupler pada komponen bukan bukti isolasi assembly.

## 1. Boundary map

```
DOMAIN A — MAINS (230 VAC, 50 Hz)
  Plug L/N/PE -> fuse -> MOV -> thermal cutoff -> relay contacts -> socket L/N
  PZEM voltage sense + CT (sisi mains)
  HLK-5M05 input

DOMAIN B — PZEM INTERNAL ISOLATION
  PZEM V4 internal optocouplers (TX/RX) isolate the mains/measurement side
  from the TTL side. The TTL side is powered from the SELV 5 V rail.
  No ADuM1201, no B0505S, no external isolated DC/DC.

DOMAIN C — SELV (5 V / 3.3 V)
  HLK-5M05 output -> carrier -> ESP32-S3, OLED, RTC, button, RGB
  74HCT125 level shifter -> PZEM RX; 10k/20k divider <- PZEM TX
  Relay coil driver (SELV side)

DOMAIN D — SERVICE/USB
  DevKitC-1 USB (SELV, but physically near mains assembly)
  USB access restricted until isolation verified
```

## 2. Barrier components

| Barrier | Komponen | Rating | Bukti | Status |
|---|---|---|---|---|
| PSU AC/DC | Hi-Link HLK-5M05 | Datasheet claims 2500 VAC input-output; batch/hipot unverified | Distributor datasheet; exact batch/certificate required | `DOCUMENTATION_DEFICIENT` |
| UART | **PZEM-004T V4 internal optocouplers** | Vendor/module-level; creepage and batch unverified | Tasmota/Components101/reverse-engineered schematic; hipot required | `DOCUMENTATION_DEFICIENT` |
| PZEM power | **None external** | TTL side powered from SELV 5 V | Carrier 5 V/GND | `ACCEPTED_AS_DESIGN_INPUT` |
| Relay module coil/contact | 2-channel optocoupler module | Optocoupler input/coil; mains contact barrier UNVERIFIED | Module datasheet/batch; creepage review | `DOCUMENTATION_DEFICIENT` |
| PCB slots/barriers | Layout | 100x70 SELV carrier; no mains | Routed, DRC 0 | `ENGINEERING_REVIEW_REQUIRED` |
| Enclosure barrier | Mechanical wall | TBD | Belum diuji | `BLOCKED` |

## 3. Ground policy

| Ground | Koneksi | Aturan |
|---|---|---|
| PE | Plug PE -> dedicated terminal/stud -> socket PE | Tidak melalui relay/fuse/PCB; kontinu |
| Mains N | Relay module CH2 (COM2/NO2) -> socket N | Bukan "GND"; jangan disatukan dengan SELV GND |
| PZEM TTL GND | Carrier GND (SELV) | **Common with ESP32 GND**; isolation is inside PZEM. Do not add a second ground reference. |
| SELV GND | Carrier/ESP32/OLED/RTC | Tidak boleh ke mains |

## 4. Consequences of removing the external barrier

- Single barrier: PZEM internal optocouplers are the only UART isolation.
- A PZEM internal failure can expose the ESP32/carrier to mains.
- The PZEM batch, creepage, and hipot/leakage test are safety-critical.
- USB must not be connected while mains is energized.
- The carrier remains SELV-only; mains modules are off-board.

## 5. Verification

1. Inspect PZEM PCB for optocouplers, creepage, contamination.
2. Hipot/leakage mains-to-TTL.
3. Verify 5 V TTL levels and divider output.
4. Thermal/load test with the enclosure closed.
5. PE continuity and relay contact behavior.
