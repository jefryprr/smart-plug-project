# Frequently Asked Questions

**Design revision:** `REV_C_PSU_BOARD`  
**Status:** digital prototype, `ENGINEERING_REVIEW_REQUIRED`, `NOT_FOR_FABRICATION`

---

## General

### What is this project?

A full digital engineering package for an ESP32-S3 smart plug: hardware research, BOM, KiCad schematic/PCB, wiring, enclosure CAD, firmware core, MQTT contract, Fastify API, Next.js dashboard, Android app, simulator, tests, and a safety dossier.

### Is this a finished product?

No. It is a **digital prototype**. No physical 230 VAC assembly has been built, energized, or tested. See [`SAFETY.md`](SAFETY.md).

### Can I plug it into a wall socket?

**No.** Not until a competent engineer reviews the design and a qualified lab performs insulation/hipot, leakage, PE continuity, thermal, load, and fault tests.

### Is it certified (SNI/CE/UL)?

No. No certification is claimed. The project deliberately does not print certification marks. The current label is `PROTOTYPE — NOT FOR USE`.

### Why are there so many documents?

Because the project separates requirements, decisions, evidence, risks, and claims. A file existing is not proof that the hardware works. The documents let a reviewer verify what was actually tested and what remains blocked.

### What is the final load rating?

**8 A / approximately 1,840 W**, limited to household electronics/SMPS loads such as TVs, routers, chargers, fans, and lamps. It is **not** a rating for heaters, kettles, irons, hair dryers, large motors, or continuous mixed loads above 8 A. The final rating still needs thermal and lifecycle testing.

---

## Hardware

### What are the main boards?

1. **REV_C PSU board** (50 × 65 mm) — 230 VAC input, fuse, MOV, 99 °C TCO, HLK-5M05, and three JST 5 V outputs. It is the mains entry.
2. **SELV carrier** (100 × 70 mm) — ESP32-S3 DevKitC-1 sockets, UART level shift, relay driver, OLED/RTC/button/RGB connectors.

The PZEM, relay module, socket, plug, fuse/MOV/TCO, and PSU are off the carrier. See [`HARDWARE_GUIDE.md`](HARDWARE_GUIDE.md).

### Why is the HLK-5M05 on a separate PCB?

Because it is a 230 VAC module. Putting it on the carrier would bring mains onto a board that is intended to be SELV-only, complicate creepage/clearance, add ~2.1 W of heat near the ESP32, and make PSU replacement harder. The separate board creates a clear mains boundary. See [`../hardware/psu/README.md`](../hardware/psu/README.md).

### Why does the PSU board have three JST outputs?

- J5 → carrier (ESP32/UI)
- J6 → relay module
- J7 → PZEM 5 V (conditional)

J7 is `PROVISIONAL`: it depends on the PZEM batch’s internal isolation and hipot results. If the external ADuM1201/B0505S barrier is restored, PZEM must **not** be fed directly from J7.

### Why is there no external ADuM1201/B0505S?

REV_C uses the PZEM-004T V4’s **internal optocouplers** as the single UART isolation barrier. This is a user decision recorded in `ADR-016`. It is `PROVISIONAL` because the exact batch, creepage, and hipot/leakage performance are unverified. The safer external barrier remains a documented fallback.

### Is the relay module a two-pole disconnect?

No. It is two independent SPDT channels, not a mechanically linked DPST. One channel can weld while the other moves. Do not claim a physical two-pole OFF state.

### Does the PCB have PE?

PE is **not** on the PSU board. It is a dedicated chassis stud: plug PE → stud → socket PE. It is never switched, fused, or routed through a relay. See `safety/POLARITY_AND_EARTH_ASSESSMENT.md`.

### Why 220 × 120 × 70 mm?

That is the enclosure size that passed the coarse digital fit with off-board PZEM, relay, PSU, terminals, and wiring. 150 × 100 × 70 and 180 × 120 × 70 failed the clearance review. Physical fit, sealing, and thermal performance are still unverified.

### Can I use a different PSU or relay?

Only after a new review. The HLK-5M05, fuse, MOV, TCO, terminal blocks, JST connectors, and relay module are `PENDING_APPROVAL` or `PROVISIONAL`. Substitutions can change isolation, thermal, and protection coordination.

---

## Software

### How do I run the demo?

```powershell
npm ci
npm run api:dev
npm run web:dev
```

Open `http://localhost:3000` and log in with `demo@example.com` / `demo1234`. This is a local seed only. See [`SOFTWARE_GUIDE.md`](SOFTWARE_GUIDE.md).

### Does it work without internet?

The local button and schedule core logic are designed to continue without internet. The LAN API is deferred (`ADR-009`), so web/Android may be offline and must show stale data. Auto ON requires a valid clock; an invalid clock blocks it.

### Is the Android APK production-ready?

No. A debug arm64-v8a APK was built, but it was not installed on a device/emulator, is not release-signed, and still needs UI/device tests. See `reports/ANDROID_BUILD.md`.

### Is the backend production-ready?

No. The API has a SQLite development adapter. The PostgreSQL adapter, Docker/PostgreSQL deployment, production MQTT TLS/ACL, and clean-room deploy are still blocked.

### What is the difference between `commanded_output` and `observed_output`?

`commanded_output` is what the device was told to do. `observed_output` requires verified feedback. The UI shows `APPLIED` only after a device ACK. The API stores a shadow; it does not invent an observed state.

### Why do mock and simulator tests not count as hardware tests?

Because they do not exercise real mains, real isolation, real thermal rise, real relay contacts, real sensors, or real timing. The project explicitly refuses to report mock results as HIL or PLN tests.

---

## Safety and testing

### What tests are still blocked?

Physical fit, thermal, PE continuity, hipot/leakage, 8 A load, relay lifecycle, firmware flash/boot waveform, Android device test, PostgreSQL/Docker, and production MQTT TLS/ACL. See [`../reports/FAILURES.md`](../reports/FAILURES.md).

### What does `PASS` mean in this repo?

`PASS` means the specific digital check ran and exited successfully. It does **not** mean the hardware is safe, certified, or ready. Static checks do not prove creepage, clearance, dielectric strength, PE continuity, or thermal safety.

### What do the status labels mean?

| Status | Meaning |
|---|---|
| `PASS` | The specific test ran and passed. Digital only unless stated. |
| `FAIL` | The test ran and failed. |
| `BLOCKED` | The test cannot run yet (no hardware/lab/tool/approval). |
| `UNVERIFIED` | A value or claim has not been checked. |
| `PROVISIONAL` | A design choice exists but may change after review/test. |
| `DIGITAL_COMPLETE` | Digital artifacts exist; no physical validation. |
| `ENGINEERING_REVIEW_REQUIRED` | A competent engineer must review before fabrication/use. |
| `HARDWARE_VALIDATION_REQUIRED` | Physical lab tests are still required. |
| `READY_FOR_FABRICATION` | Not used. Gate F4 not passed. |
| `READY_FOR_USE` | Not used. |

### Can I help with the physical tests?

Only if you are a qualified person working under a lab procedure with engineer supervision. The repository does not provide mains energization instructions for laypeople.

---

## Contributing and licensing

### How can I contribute?

Read [`../CONTRIBUTING.md`](../CONTRIBUTING.md). Good first contributions: documentation fixes, translations, test coverage, datasheet corrections, screenshot updates, and reproducing the digital validation gate.

### How do I report a security issue?

Use GitHub Security Advisories as described in [`../SECURITY.md`](../SECURITY.md). Do not open a public issue containing a real secret, token, or private key.

### What license applies?

Code and original documentation are MIT. Third-party trademarks and datasheets remain with their owners. See [`../LICENSE`](../LICENSE) and [`../NOTICE.md`](../NOTICE.md).
