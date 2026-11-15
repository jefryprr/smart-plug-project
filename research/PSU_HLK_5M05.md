# Hi-Link HLK-5M05 — PSU Specification Study

**Status:** `SPECIFICATIONS_AVAILABLE` / `PENDING_APPROVAL`
**Date:** 2026-11-15
**Selected by:** user instruction, replacing Mean Well IRM-05-5
**Local datasheet:** `research/datasheets/hlk-5m05_distributor.pdf` (3-page distributor copy)
**Source page:** https://www.hlktech.net/index.php?id=1243

## 1. What it is

The HLK-5M05 is a small AC/DC switching power module: **90–264 VAC input,
5 VDC / 1 A (5 W) output**, four pins. It is much smaller and cheaper than the
Mean Well IRM-05-5, but its efficiency is lower and its certification/isolation
evidence is weaker. It is selected for the prototype BOM, not approved for
production.

## 2. Electrical specifications

| Parameter | Value | Source/status |
|---|---|---|
| Rated input | 100–240 VAC | datasheet |
| Input range | 90–264 VAC | datasheet |
| Max input voltage | ≤270 VAC | datasheet |
| Max input current | ≤0.2 A | datasheet |
| Inrush current | ≤10 A | datasheet |
| Startup time | ≤50 ms | datasheet |
| Output | 5 VDC, 1 A continuous, 5 W | datasheet |
| Short-term output current | ≤1.2 A | datasheet |
| Output tolerance | ±0.1 V rated, ±0.2 V full load | datasheet |
| Ripple/noise | ≤70 mVp-p (20 MHz BW, 10 µF + 0.1 µF load caps) | datasheet |
| Efficiency | ≥69% at 110 VAC; **≥70% at 220 VAC, full load** | datasheet |
| No-load loss | <0.1 W | datasheet |
| Over-current protection | 150–200% of max load | datasheet |
| Short-circuit protection | auto-recovery after removal | datasheet |
| Isolation voltage | **2500 VAC input–output** (claim) | datasheet; batch/hipot unverified |
| Insulation resistance | >100 MΩ at 500 VDC | datasheet |
| Safety/EMC | “designed to meet” UL1012, EN60950, UL60950; EN55011/EN55022; ESD IEC/EN 61000-4-2 level 4 | datasheet; **not a certificate** |
| MTBF | ≥100,000 h (claim) | datasheet |

At 5 W output and 70% efficiency, input power is about **7.1 W**, so the module
dissipates roughly **2.1 W** at full load. This is higher than the IRM-05-5 and
must be included in the enclosure thermal test.

## 3. Physical specifications

| Parameter | Value |
|---|---|
| Body dimensions | **38 × 23 × 18 mm** (drawing) |
| Weight | 32 ± 1 g |
| Pins | 4 pins, 0.8 mm diameter |
| Pin 1 | AC |
| Pin 2 | AC |
| Pin 3 | −Vo (0 V) |
| Pin 4 | +Vo (+5 V) |
| Pin spacing | 35.8 mm and 20.5 mm across; 14.5/8.5 mm reference dims |
| Cooling | radiation, no fan |
| Operating temperature | −20 to +60 °C |
| Storage temperature | −40 to +80 °C |
| Humidity | 5–95% RH |
| Altitude | ≤2000 m |
| Vibration | 10–500 Hz, 2 G, 60 min/axis |

The module is **off-board**, not on the low-voltage carrier. It sits in the
mains zone with a dedicated mount/standoff and a barrier from SELV wiring.

## 4. Pinout and wiring

```
Pin 1  AC L  ── fuse/MOV/thermal-cutoff input side
Pin 2  AC N  ── mains neutral
Pin 3  -Vo   ── SELV 0 V
Pin 4  +Vo   ── SELV +5 V
```

The AC pins are mains. Keep a clear creepage slot/barrier between AC pins and
the DC pins; do not route SELV wires across the AC pins. Add a 100 µF bulk
capacitor and 100 nF decoupling at the carrier input, and verify startup with
the ESP32 Wi-Fi burst.

## 5. Power budget and derating

| Load | Typical | Peak |
|---|---:|---:|
| ESP32-S3 + Wi-Fi | 180 mA | 350 mA |
| OLED | 15 mA | 20 mA |
| PZEM isolated side | 10 mA | 15 mA |
| 2-channel relay module coils/LEDs | 140 mA | 160 mA |
| RGB/level shifter | 10 mA | 30 mA |
| RTC DS3231 | 2 mA | 3 mA |
| **Total** | **~357 mA** | **~578 mA** |

The 1 A output gives roughly **42% margin at the estimated peak**, but:
- the estimate is not measured;
- Wi-Fi bursts and relay inrush can be shorter/higher;
- the module runs at only ~70% efficiency, so heat is significant;
- the 60 °C case limit is close to a 40 °C enclosure ambient plus rise.

Therefore the HLK-5M05 is **`PENDING_APPROVAL`**, not a validated 1 A supply for
this enclosure. Measure 5 V ripple, startup, temperature rise, and brownout at
the real load before approving it.

## 6. Safety and certification caveats

1. The datasheet says “designed to meet” UL/CE standards; it does **not** show a
   certificate, UL file number, or batch test report.
2. The 2500 VAC isolation is a datasheet claim, not a hipot result for the
   purchased unit.
3. The module has AC and DC pins close together; creepage/clearance and the
   barrier must be reviewed in the actual assembly.
4. The PCB is small and the module is often sold as a low-cost commodity. Batch
   quality, capacitor brand, and workmanship can vary.
5. It is not a medical/industrial certified supply. Do not use it as the sole
   safety barrier without engineer review and hipot/leakage tests.
6. Keep the fuse, MOV, and thermal cutoff upstream. The PSU is not a substitute
   for them.

## 7. Comparison with IRM-05-5

| Item | HLK-5M05 | IRM-05-5 |
|---|---|---|
| Output | 5 V / 1 A / 5 W | 5 V / 1 A / 5 W |
| Input | 90–264 VAC | 90–264 VAC |
| Efficiency | ~70% at 220 V full load | ~78% (series data) |
| Size | 38 × 23 × 18 mm | ~53.5 × 28.5 × 19 mm |
| Heat at 5 W | ~2.1 W | ~1.4 W |
| Documentation | distributor copy; certification unverified | official series datasheet |
| Certification | claims UL/CE design compliance | vendor documentation; exact model still to verify |
| Selection | **user-selected for prototype** | fallback if HLK fails review |

## 8. Verdict

**Use HLK-5M05 in the BOM as the selected prototype PSU**, but keep it
`PENDING_APPROVAL` and require:
- batch datasheet/certificate and pin marking check;
- 5 V ripple/startup/brownout test at the real load;
- thermal test in the closed 220×120×70 enclosure at 40 °C ambient;
- hipot/leakage/isolation review;
- creepage/clearance review around the AC pins;
- fallback to IRM-05-5 if any of these fail.

Do not claim the PSU is safe, certified, or production-ready.

## 9. Indonesian sourcing (2026-11-15)

| Seller | Price | Stock | Note |
|---|---:|---|---|
| Shopee / Marnov Electronic | Rp49.000 | listed | Priced prototype unit. |
| Shopee / Das_store22 | Rp49.900 | listed | Similar listing. |
| CNC Store Bandung | Rp63.300 | **out of stock** | Local retailer page, useful reference. |

The price spread (Rp49.000–Rp63.300) is large enough that counterfeit or
different-batch units are likely. Buy from a seller with batch marking and
photos, and reject unmarked modules. Price is not approval.
