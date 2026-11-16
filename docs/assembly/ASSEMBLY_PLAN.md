# Assembly Plan — REV_C_PSU_BOARD

**Status:** `DIGITAL_PLAN_ONLY`; no physical assembly performed.  
**Design revision:** `REV_C_PSU_BOARD`  
**Safety:** mains work is qualified-personnel/lab only. This plan is not an energization procedure.

## Three separate scopes

1. **Mechanical assembly, no energy** — trained person with basic tools.
2. **Low-voltage assembly** — trained person, ESD/solder QC.
3. **Mains assembly and test** — qualified personnel only, lab procedure, engineer sign-off.

Never combine scope 3 with scope 1/2 in one unsupervised session. PE is never switched or fused.

## 1. Incoming inspection

1. Photograph every module and label the bag with lot/serial.
2. Verify ESP32-S3 DevKitC-1 **N16R8**, two 1×22 headers, **22.86 mm row spacing**, USB ports and pin 1.
3. Verify PZEM-004T **V4 100 A CT**, optocouplers, TTL pin order, CT ratio.
4. Verify HLK-5M05 marking, 5 V/1 A, isolation claim, AC pin order.
5. Verify relay module is 2-channel, active-LOW, two independent SPDT channels, not a linked DPST.
6. Verify fuse 10 A 250 VAC ceramic, holder rating, MOV 275 VAC, TCO 99 °C one-shot, terminals, socket/plug, PE hardware.
7. Verify enclosure 220×120×70, wall, flame grade, lid screws, gasket, M16 gland, M12 vent.
8. Quarantine any mismatch; update `parameters.yaml`/`components.py` and re-run fit if dimensions differ.

## 2. Mechanical preparation (no energy)

1. Print/acquire body, lid, gasket, USB cover, DevKit key, PZEM/relay/PSU brackets.
2. Install 4× M3 heat-set inserts in the lid bosses; install module inserts where used.
3. Deburr the socket, gland, vent, USB, and top cutouts.
4. Test-fit the gasket frame on the body rim; verify it is not pinched.
5. Mount the carrier on the four standoffs with M3×8 screws; do not over-torque.
6. Install the DevKit key on the two left carrier holes. Insert the DevKit **pin 1 / USB end** per the silkscreen; confirm the key blocks a reversed board.
7. Install the RTC module near J5, the OLED/button/RGB on the lid, and route their JST cables with service loops.
8. Mount the **PSU board** on its 3 standoffs (H1/H3/H4), the relay on the printed cantilever shelf above it, and PZEM, CT, socket, gland, and PE stud on their brackets/bosses. The HLK/fuse/MOV/TCO/terminals are already on the PSU board.
9. Install the PE stud and bond hardware; PE must be a dedicated metal path, not a plastic boss alone.
10. Install the M16 gland, M12 vent, and USB cover; check thread engagement and gasket seating.

## 3. Low-voltage assembly

1. Solder/assemble the SELV carrier: two 1x22 sockets, JST connectors, 74HCT125, divider, pullups, MOSFET, passives, fiducials. The PTC/TVS are on the PSU board, not the carrier.
2. Inspect for bridges, tombstones, wrong values, and damaged pads.
3. Verify 74HCT125 pin 1, MOSFET pinout, JST keying, and PZEM divider values. On the PSU board verify F2 PTC/D1 TVS orientation, TF1 SF96E marking (96 °C), F1 10 A, MOV S10K275, TB1/TB2 pin order, and J5/J6/J7 keying. PSU board soldering is a mains assembly item, not low-voltage bench work.
4. Continuity/ESD check: +5V, +3V3, GND, UART, I2C, relay gate; no short between rails.
5. Connect J8 (5 V), J2 (PZEM TTL), J3 (relay), J4 (OLED), J5 (RTC), J6 (button), J7 (RGB).
6. Keep PZEM/relay/5 V cables away from the mains side except through the barrier grommets.
7. Do **not** connect USB while mains is present.

## 4. Mains assembly (qualified personnel only)

1. Follow the lab procedure and `safety/` documents; do not improvise.
2. Use ferrules, correct wire gauge, strain relief, and torque per terminal datasheet.
3. Wire plug L/N to PSU TB1, PSU TB2 L/N to relay contacts and socket, PZEM voltage sense/CT, relay coil from PSU J6, and the PE stud. Fuse/MOV/TCO/HLK are on the PSU board; do not bypass them.
4. PE: plug PE → dedicated stud/terminal → socket PE; no relay, fuse, or switch in the PE path.
5. Keep SELV and mains separated by the barrier; all crossings through grommets.
6. Inspect clearance/creepage, loose strands, contamination, and terminal retention.
7. Install the lid gasket and lid; tighten 4× M3×16 screws evenly.
8. Verify the USB cover is closed and labelled “MAINS OFF”.

## 5. Inspection before any energy

- PE continuity and bond torque.
- No L/N–PE short; no SELV–mains short.
- PSU board assembly, F1/MOV1/TF1 orientation, TB1/TB2 pin order, J5/J6/J7 keying, relay/socket/terminal ratings.
- Barrier intact; no cable bypass.
- Gasket seating; lid screws; gland/vent/socket retention.
- Labels: 8 A limit, 230 VAC, PE, “no USB with mains”, model/revision.
- Record photos and measurements.

## 6. Lab tests (qualified lab only)

1. Isolation/hipot and leakage, including PZEM internal barrier.
2. PE continuity and earth bond.
3. Thermal rise at 8 A in the closed enclosure, ambient 40 °C.
4. Load/inrush, relay lifecycle, fuse/TCO coordination.
5. EMC/pre-compliance as required.
6. Only after pass and engineer sign-off consider `F4 FABRICATION_RELEASED` / `READY_FOR_USE`.

## Stop conditions

- PE not continuous.
- Clearance/creepage not reviewed.
- Relay/fuse/terminal/socket rating unverified.
- Enclosure not rated/certified.
- Any doubt about isolation.
- No engineer/lab.

## Evidence to record

- Component photos/serials/lots.
- Torque values, wire gauge/ferrules.
- PE continuity and insulation results.
- Thermal/load curves.
- Firmware version/hash.
- Photos of final assembly.
- Signed checklist.
