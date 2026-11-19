# Roadmap

**Current revision:** `REV_D_CORE_ONLY`  
**Current stage:** end of digital engineering (F3) → engineering review (F4)  
**Fabrication:** `NOT_RELEASED`

The roadmap is organized by **evidence gates**, not dates. A gate opens only when its evidence exists.

---

## F0 — Concept and requirements

**Status:** PASS (digital)

- PRD and 80 functional requirements.
- User decisions Q01–Q28.
- Assumptions, open questions, risk register.
- Product form factor and load class.

---

## F1 — Component selection and evidence

**Status:** PARTIAL

- [x] Candidate research and BOM.
- [x] HLK-5M05 study and PSU evidence table.
- [x] PZEM/relay off-board study.
- [x] Indonesian procurement matrix.
- [ ] Batch certificates for HLK, PZEM, relay, fuse, MOV, TCO, terminal, JST, socket/plug.
- [ ] Vendor footprint review and approved MPNs.
- [ ] Counterfeit inspection procedure executed on purchased samples.

**Exit:** every safety-relevant part has a source, rating, batch evidence, and approval status.

---

## F2 — Schematic, PCB, and mechanical design review

**Status:** PARTIAL

- [x] System block schematic.
- [x] Routed SELV carrier, DRC 0/0.
- [x] Routed PSU board, DRC 0/0.
- [x] Wiring harnesses and enclosure CAD.
- [ ] Component-level production schematic.
- [ ] Creepage/clearance calculation with licensed standard and engineer.
- [ ] Thermal calculation at 8 A in the closed enclosure.
- [ ] PE/polarity/protection coordination review.
- [ ] Engineer sign-off.

**Exit:** a competent engineer signs the schematic, layout, creepage, thermal, PE, and protection review.

---

## F3 — Digital build and test

**Status:** PASS (digital, 27 PASS / 11 BLOCKED / 0 FAIL)

- [x] Domain, MQTT, API, simulator, firmware host, web tests.
- [x] ESP-IDF target build.
- [x] KiCad ERC/DRC, Gerber/drill/POS provisional.
- [x] WireViz/CadQuery artifacts.
- [x] Static wiring/GPIO/BOM/PSU crosschecks.
- [x] Android debug APK build.
- [ ] Reproduce on a clean machine/CI (CI covers Node tests; full gate is local).

**Exit:** reproducible digital evidence with logs and exit codes.

---

## F4 — Fabrication release

**Status:** BLOCKED

- [ ] F1–F3 complete.
- [ ] Engineer sign-off.
- [ ] Manufacturing review of Gerber/drill/POS.
- [ ] 2 oz copper fabrication capability verified.
- [ ] Assembly/test plan approved.

**Exit:** `READY_FOR_FABRICATION` (not used yet).

> Do not send the provisional Gerber files to a fab as a functional board before F4.

---

## F5 — Bench low-voltage validation

**Status:** BLOCKED

- [ ] Flash firmware on a verified DevKitC-1.
- [ ] Verify 5 V/3.3 V rails and ripple.
- [ ] Verify UART level shift, PZEM communication, OLED, RTC, button, RGB.
- [ ] Verify relay driver boot-safe OFF and active-LOW behavior.
- [ ] Verify Wi-Fi/MQTT/API/ACK/telemetry.
- [ ] Boot waveform and watchdog tests.

**Exit:** low-voltage bench evidence, no mains.

---

## F6 — Mains and thermal lab validation

**Status:** BLOCKED

- [ ] PE continuity and fault-current.
- [ ] Hipot/insulation resistance/leakage.
- [ ] 8 A thermal rise in the closed enclosure.
- [ ] Fuse/MOV/TCO coordination and trip test.
- [ ] Relay lifecycle and per-channel weld test.
- [ ] Inrush/load tests.
- [ ] EMC pre-scan.

**Exit:** qualified lab report and engineer sign-off.

---

## F7 — Pilot and regulatory

**Status:** BLOCKED

- [ ] Enclosure material/flame/impact/IP review.
- [ ] Socket/plug certification.
- [ ] Regulatory classification (SNI/CE/UL as applicable).
- [ ] Manufacturing test procedure.
- [ ] Field pilot with logging and incident process.

**Exit:** pilot approval; no consumer sale yet.

---

## F8 — Production

**Status:** NOT STARTED

- [ ] Certification.
- [ ] Production test fixture and traceability.
- [ ] Supply-chain/quality plan.
- [ ] Support and incident response.
- [ ] Labeling and documentation.

**Exit:** `READY_FOR_USE` (not used yet).

---

## Near-term priorities

1. Resolve the terminal block 250 V vs ≥300 V gap and fuse-clip thermal margin.
2. Get batch evidence for HLK, PZEM, relay, fuse, MOV, TCO, terminal, JST, socket/plug.
3. Complete the component-level schematic and footprint review.
4. Build a low-voltage bench fixture and flash the firmware.
5. Book a qualified lab for PE/hipot/thermal/load tests.
6. Keep the documentation and manifest in sync with every change.

---

## How to help

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The highest-value contributions are primary-source datasheets, footprint review, test coverage, beginner documentation, and Indonesian translations.
