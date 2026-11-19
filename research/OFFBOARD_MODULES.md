# Off-Board Module Study — PZEM-004T and 2-Channel Relay

**Design revision:** `REV_D_CORE_ONLY`
**Status:** `PROVISIONAL` / `DOCUMENTATION_DEFICIENT`
**Scope:** research and mounting study for the two mains-adjacent modules that the
user required **off the PCB**. This is not a mains assembly approval.

## 1. Why these modules are off-board

- The low-voltage carrier stays SELV: ESP32-S3, display, sensors, and logic only.
- The PZEM and relay module carry or sense mains. They live in the mains zone of
  the enclosure on separate brackets.
- No mains trace, terminal, or module pin is routed onto the carrier.
- Off-board does **not** mean safe by itself. Creepage, clearance, strain relief,
  PE bonding, thermal rise, and enclosure material still need engineering review
  and physical tests.

## 2. PZEM-004T V4 (selected direction)

| Item | Finding | Status |
|---|---|---|
| Function | AC voltage, current, active power, energy, frequency, power factor (V3/V4 family) | `TYPICAL` |
| Variant | Use the **100 A CT** version (closed or split) so load current does not pass through the module | `PROVISIONAL` |
| Voltage input | 80–260 VAC L/N terminals | `UNVERIFIED` for purchased batch |
| TTL interface | 4-pin: **5V, RX, TX, GND**; passive interface needs all four | `TYPICAL`, verify batch |
| Logic level | 5 V TTL; ESP32-S3 is 3.3 V — 74HCT125 TX + 10k/20k RX divider required | `PROVISIONAL` |
| Protocol | Modbus-RTU-like UART; exact register map/version must be checked | `UNVERIFIED` |
| CT placement | Clamp around **L only**, never around L and N together | `REQUIRED` |
| Power | Supplied from SELV 5 V; PZEM internal optocouplers isolate mains | `DOCUMENTATION_DEFICIENT` |
| Accuracy | Not revenue-grade; low-current accuracy at 8 A with a 100 A CT is unverified | `UNVERIFIED` |
| Dimensions | ~53 × 89 × 24 mm envelope (approximate, not measured) | `PROVISIONAL` |
| Mounting | Dedicated plate, 58 × 94 × 2 mm, 4× M3, cable-tie slot | `PROVISIONAL` |
| Batch manual | Official Peacefair V4 manual for the exact batch not obtained | `DOCUMENTATION_DEFICIENT` |

### PZEM wiring intent

```
L (mains) ─────────────── PZEM L terminal
N (mains) ─────────────── PZEM N terminal
L load conductor ── CT clamp (one conductor only)
PZEM 5V/RX/TX/GND ── isolation/level barrier ── ESP32 UART
```

The PZEM voltage terminals are mains-referenced even when the CT is split. Treat
the whole module as mains until the isolation barrier is proven.

### PZEM open items

- Confirm the purchased variant is 100 A CT, not the 10 A pass-through version.
- Measure the actual module and CT before printing the bracket.
- Obtain the batch manual; verify pin order, UART baud, register map, and supply.
- Review PZEM internal optocoupler creepage and perform hipot/leakage; no external barrier.
- Calibrate/compare against a reference meter; do not claim billing accuracy.
- Verify CT orientation and that only L passes through the jaw.

## 3. Common 2-channel 5 V optocoupler relay module

| Item | Finding | Status |
|---|---|---|
| Channels | Two independent SPDT relays: COM/NO/NC each | `TYPICAL_MODULE` |
| Inputs | IN1, IN2, VCC, GND; **active-LOW** on the common board | `TYPICAL`, verify batch |
| Coil supply | 5 V; 15–20 mA per channel driver current | `TYPICAL` |
| JD-VCC | Jumper links input VCC to relay coil supply; remove for separate coil supply | `TYPICAL` |
| Contact claim | AC 250 V / 10 A per channel (vendor claim) | `UNVERIFIED` |
| Final load | **8 A / ~1.840 W**, electronics/SMPS only | `PROVISIONAL` |
| Channel linkage | **Not mechanically linked DPST**; one channel can weld/stay closed | `RESIDUAL_RISK` |
| Isolation | Optocoupler isolates input transistor; shared GND defeats galvanic isolation | `REVIEW_REQUIRED` |
| Dimensions | ~50 × 24 × 18 mm envelope (approximate) | `PROVISIONAL` |
| Mounting | Dedicated plate, 55 × 26 × 2 mm, 4× M3, cable-tie slot | `PROVISIONAL` |

### Relay wiring intent

```
SELV: ESP32 GPIO ── gate of N-channel MOSFET ── module IN1 + IN2
      100k pulldown on gate; source to SELV GND
      5V and GND to module VCC/GND (JD-VCC jumper fitted for prototype)

MAINS: L → fuse → MOV → thermal cutoff → COM1
       NO1 → socket L
       N → COM2
       NO2 → socket N
       PE → dedicated terminal/stud → socket PE (never switched)
```

`NC1`/`NC2` are left unconnected and insulated. The firmware never claims a
physical OFF state: there is no contact feedback, and the two channels are not
linked.

### Important electrical caveat

The common module has an optocoupler, but with VCC/GND shared between the ESP32
side and the module input side, the input is **not galvanically isolated**. The
relay contacts still provide functional separation, but the module PCB is not a
certified isolation barrier. Keep the entire module in the mains zone, do not
route its wiring across the SELV carrier, and do not describe it as "isolated"
or "safety-rated" without evidence.

### Relay open items

- Verify active-LOW behavior, pin order, JD-VCC jumper, and contact arrangement
  on the exact batch.
- Verify contact rating, inrush capability, and lifecycle; the 10 A claim is not
  an 8 A continuous rating.
- Test each channel separately for weld/stuck-closed failure.
- Measure coil current and 5 V supply margin with both channels energized.
- Measure module and terminal temperature at 8 A in the closed enclosure.
- Decide whether a separate isolated coil supply is required; if yes, the input
  side must be rewired and the barrier reviewed.

## 4. Enclosure placement

The **180 × 120 × 70 mm** recommended preset passes the coarse AABB fit. The
150 × 100 × 70 target fails with the off-board modules.

| Item | Placement intent |
|---|---|
| PZEM | Mains zone, on its 58 × 94 mm plate, voltage terminals accessible, CT nearby |
| Relay module | Mains zone, on its 55 × 26 mm plate, contact screws accessible, away from PZEM CT |
| SELV carrier | Opposite side of the barrier; no mains conductor crosses it |
| PE | Dedicated stud/terminal; continuous to socket PE; never through relay/fuse |
| Service access | Modules removable without desoldering; strain relief on all mains wires |
| Thermal | Keep PZEM/relay/PSU separated; no stacked modules; verify air volume |

The brackets are prototype geometry only. They are not an electrical enclosure
rating, not a flammability certificate, and not a tolerance-stack validation.

## 5. Verification checklist

- [ ] Photograph and measure the exact PZEM and relay module.
- [ ] Record batch markings and download the matching manuals.
- [ ] Verify PZEM pin order, UART levels, baud, register map, and CT type.
- [ ] Verify relay active-LOW inputs, JD-VCC behavior, and COM/NO/NC continuity.
- [ ] Build/measure the confirmed 220 × 120 × 70 enclosure and print both brackets.
- [ ] Test-fit with actual modules and cable bend radius.
- [ ] Review creepage/clearance and the SELV/mains barrier.
- [ ] Run thermal, load, inrush, and per-channel weld tests in a qualified lab.
- [ ] Update the rating label only after the tests pass.

## 6. Sources

- Handsontec, *2 Channel 5V Optical Isolated Relay Module* user guide:
  https://www.handsontec.com/dataspecs/module/2Ch-relay.pdf
  (local: `research/datasheets/handsontec_2ch_relay.pdf`).
- DigiKey, *TS0010D 2-channel relay module datasheet*:
  https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/5773/TS0010D%20DATASHEET.pdf
  (local: `research/datasheets/digikey_ts0010d_2ch_relay.pdf`; encrypted PDF,
  text extraction incomplete).
- Peacefair PZEM-004T historical archive (V1.0 specification, **not** a V4
  manual): https://github.com/im-0/pzem-004t-original-docs
  (local: `research/datasheets/pzem_004t_specification_archive.docx`).
- PZEM-004T pinout/wiring reference (secondary source, not a datasheet):
  https://components101.com/modules/pzem-004t-energy-meter-module-pinout-datasheet
- PZEM-004T CT wiring note (secondary source):
  https://shillehtek.com/blogs/shillehtek-product-manuals/pzem-004t-ac-energy-meter-current-transformer-manual
- PZEM-004T V3 user manual (historical reference, not V4):
  https://innovatorsguru.com/wp-content/uploads/2019/06/PZEM-004T-V3.0-Datasheet-User-Manual.pdf

**Conclusion:** the modules are studied and mechanically placed, but both remain
`DOCUMENTATION_DEFICIENT`. No mains assembly, rating, or fabrication release is
claimed.
