# System Schematic Set — Smart Plug ESP32-S3

**Revision:** `REV_D_CORE_ONLY`  
**Status:** `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED` / **NOT_FOR_USE**  
**Main file:** `hardware/schematic/SYSTEM_SCHEMATIC.pdf`

## Files

| File | Isi |
|---|---|
| `SYSTEM_SCHEMATIC.pdf` | 5 halaman: cover + 4 halaman schematic/checklist |
| `system/page1_mains.png/.svg` | Jalur mains 230 VAC: P1, TB1, F1, MOV1, TF1, TB2, K1, X1, PE |
| `system/page2_selv.png/.svg` | Jalur SELV: 5 V protection, ESP32, PZEM UART, relay driver, button |
| `system/page3_pinout.png/.svg` | Pinout konektor, wire colours, pin proteksi PSU |
| `system/page4_safety.png/.svg` | Safety rules, assembly order, pre-power checklist, sign-off |
| `system/SCHEMATIC_CROSSCHECK.md` | Hasil cross-check netlist PSU + carrier |

## Sumber data

- `hardware/psu/netlist.csv`
- `hardware/carrier/netlist.csv`
- `hardware/wiring/main_harness.yaml`
- `hardware/wiring/metering_harness.yaml`
- `hardware/psu/README.md`
- `hardware/carrier/README.md`

## Cara membaca

- Garis berwarna = kabel fisik.
- Label net yang sama = terhubung.
- **Brown** = L (fase), **blue** = N (netral), **green/yellow** = PE.
- **Red** = +5 V, **black** = GND, **orange** = +3.3 V, **purple** = sinyal.
- **Dashed red** = isolation barrier.
- Halaman 1–2 = functional/wiring diagram; halaman 3 = pinout eksak; halaman 4 = checklist.

## Hasil verifikasi

`python hardware/schematic/verify_schematic.py` → **ALL PASS** untuk net membership PSU dan carrier.

Yang **belum** dibuktikan oleh gambar ini:

- Creepage/clearance IEC 60664-1, OVC/pollution degree.
- HLK-5M05 batch isolation, certificate, ripple, thermal.
- PZEM V4 internal isolation, creepage, hipot.
- Fuse/MOV/TCO/terminal/JST ratings and breaking capacity.
- BLX-A holder 6.3 A is the limiting part.
- PCB 2 oz / solder mask barrier / assembly hipot.
- Enclosure flame rating, gasket leak, IP rating, impact.
- Relay contact weld / lifecycle / 6 A thermal rise.
- TCO body/pitch and socket body/depth (measure received parts).
- M4×16 socket screw length vs flange + wall + boss (M4×12 fallback).

## Build notes

- **KF129 vs KF301:** schematic uses the design terminal **KF129-2P 25 A**. The current cart substitute **KF301-2P 15 A** is **PROVISIONAL**; it is adequate for the 6 A provisional load but body/creepage/retention need review.
- **ESP32:** the cart variant may be **unsoldered**; solder two 2×22 headers and verify 22.86 mm row spacing.
- **PZEM CT:** clamp **only L**, arrow toward load. Never N or L+N.
- **JP1:** bridge for PSU operation; **open before USB service power**. Do not connect USB while mains is ON.
- **PE:** direct plug → stud → socket. Never fused, switched, or relayed.
- **Fuse:** 6.3 A time-lag only; never 10 A in the BLX-A holder.

## Safety

230 VAC is lethal. This is **not** a certified wiring diagram and **not** an energization procedure. Do not energize until an engineer reviews the schematic, PCB, enclosure, and harness, and until PE continuity, hipot/leakage, and thermal/load tests pass.
