# ESP32-S3 IoT Smart Plug — Digital Engineering Package

**Design revision:** `REV_A_PROVISIONAL`
**Project status:** `PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`
**Fabrication:** `NOT_RELEASED` — do not send this repo to a PCB manufacturer.

**Latest amendment (2026-11-15):**
- Final load rating: **8 A / ~1.840 W**, electronics/SMPS only (not heaters/motors).
- PZEM-004T V4 and a **common 2-channel 5 V optocoupler relay module** are **off-board**, with enclosure brackets. The module is two independent SPDT channels, **not** a mechanically linked DPST.
- **150×100×70 and 180×120×70 fail** the clearance review with the off-board modules; **220×120×70 recommended** pending user confirmation. The earlier 180×120 “PASS” only stacked the relay above the PZEM with a 0.5 mm gap and ignored brackets; that is rejected.
- **KiCad 10.0.8 CLI installed**; ERC 0 on the text-only block schematic, DRC 0 on the placement-only PCB, provisional Gerber/drill exported. Component-level schematic/routing remains blocked.

> **Safety first.** This repository contains a digital prototype, not a certified or physically validated mains product. No 230 VAC assembly was built, energized, or tested. Do not connect mains to a 3D-printed enclosure or an unapproved prototype. PE must remain continuous and is never switched. See `safety/` and `docs/tutorials/00_READ_FIRST.md`.

---

## What this is

A full digital engineering package for an inline ESP32-S3 smart outlet:
research, BOM, safety analysis, GPIO map, wiring harnesses, KiCad block/placement files,
CadQuery enclosure, portable firmware core, backend API, MQTT contract, web dashboard,
Android source, device simulator, tests, and handoff documentation.

The PRD is the contract: `PRD.md`.

## What is actually verified

| Area | Evidence | Status |
|---|---|---|
| Domain logic | 34 Vitest tests | PASS |
| MQTT contract | 11 tests | PASS |
| API + simulator | 38 tests incl. full command→ACK | PASS |
| Firmware C core | 74 checks, Zig host build | PASS |
| Web | Next build + 5 Playwright tests + axe | PASS |
| Static wiring/GPIO/BOM | Python crosscheck | PASS |
| WireViz | 6 harnesses rendered | PASS |
| CadQuery | STEP/STL + renders + brackets | PASS (digital) |
| KiCad CLI | 10.0.8, ERC/DRC/Gerber run | PASS (block/placement) |
| ESP-IDF build | v6.1, target esp32s3, 192,464-byte `.bin` | PASS (build only) |
| Android debug APK | 46,852,340-byte arm64-v8a APK, v2 signature verified | PASS (debug, not installed) |
| npm audit | 0 known npm vulnerabilities | PASS |

## What is blocked

| Area | Reason |
|---|---|
| Component-level schematic/routing | Block/placement only; no approved MPNs/footprints |
| Firmware integration/flash | Build exists; PZEM/OLED/Wi-Fi/MQTT/OTA and boot-waveform tests are absent |
| Android device test | APK exists; not installed on emulator/device; debug/arm64 only |
| PostgreSQL/Docker deployment | Docker/Postgres not installed; API Postgres adapter missing |
| MQTT TLS/ACL production | Not deployed/tested |
| Physical fit/thermal/PE/isolation/load | No hardware/lab/engineer |
| Engineering/regulatory sign-off | No qualified reviewer |

See `reports/FAILURES.md`, `reports/VALIDATION_SUMMARY.json`, and `deliverables/manifest.json`.

---

## Quick start (digital, no mains)

```powershell
npm install
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe pyyaml kiutils wireviz cadquery trimesh matplotlib numpy pillow reportlab svglib

npm run test
npm run build -w @smartplug/web
npx playwright test
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1
.venv\Scripts\python.exe scripts\validate_all.py --e2e
```

Demo login: `demo@example.com` / `demo1234` (local seed only; never production).
Demo pairing code: `123456` (single-use in the API; seed only).

### Local stack

```powershell
npm run api:dev      # API on :4000, SQLite, seeded demo
npm run sim:dev      # device simulator (needs MQTT broker)
npm run web:dev      # Next.js on :3000
```

For a self-contained E2E stack (broker + simulator + API), use `node scripts/e2e_api.mjs` and the Playwright config.

---

## Repository map

```
apps/
  api/                 Fastify API, SQLite adapter, tests
  web/                 Next.js dashboard
  device-simulator/    MQTT device simulator
  android/             Expo Android source + generated project (debug APK built)
packages/
  domain/              command/energy/schedule rules
  api-contract/        OpenAPI + Zod schemas
  mqtt-contract/       topics + schemas + fixtures
firmware/              portable C core + ESP-IDF skeleton
hardware/
  kicad/               native block schematic + placement PCB
  wiring/              6 WireViz harnesses + renders
  interfaces/          GPIO map
  mechanical/          CadQuery enclosure + exports/renders
  manufacturing/       provisional, NOT released
  pcb/render/          placement preview (not a KiCad plot)
research/              component research, off-board module study, candidates, datasheets
bom/                   BOM master + tools + approvals (unpriced)
safety/                rating chain, isolation, clearance, FMEA, PE, standards
security/              threat model, authorization, MQTT ACL, SBOM, audit
database/              PostgreSQL migrations + dev seed
infrastructure/        Docker/Mosquitto/Caddy templates
docs/                  decisions, tutorials, UI/UX, operations, hardware
validation/            connectivity/GPIO/BOM crosschecks
reports/               phase reports, test matrix, failures, logs
deliverables/          manifest + final report
```

---

## Key documents

- Off-board modules: `research/OFFBOARD_MODULES.md`
- Decisions: `docs/decisions/USER_ANSWERS.md`, `ASSUMPTION_REGISTER.md`, `ADR-*.md`
- Safety: `safety/ELECTRICAL_RATING_CHAIN.md`, `ISOLATION_PLAN.md`, `CLEARANCE_CREEPAGE_WORKSHEET.md`, `RESIDUAL_RISK_REGISTER.csv`
- Phase 1: `reports/PHASE_1_ENGINEERING_REPORT.md`
- Phase 2: `reports/PHASE_2_SOFTWARE_REPORT.md`
- Handoff: `deliverables/FINAL_ENGINEERING_REPORT.md`, `deliverables/manifest.json`
- Build evidence: `reports/FIRMWARE_BUILD.md`, `reports/ANDROID_BUILD.md`, `reports/AMENDMENT_8A_OFFBOARD.md`
- Tutorials: `docs/tutorials/README.md` (26 files)
- Test gate: `reports/TEST_MATRIX.csv`, `reports/VALIDATION_SUMMARY.json`

---

## Claims we do **not** make

- `READY_FOR_FABRICATION`
- `READY_FOR_USE`
- certified, SNI-compliant, or consumer-safe
- real energy measurement/calibration
- HIL or PLN test success
- production deployment, TLS, or Android APK
- that a mock/simulator result is a physical result

## Next human actions

1. Confirm the **220×120×70** enclosure change (Q06=C) and select/verify socket, plug, 2-channel relay module, fuse, PSU, terminal, PE hardware.
2. Complete the component-level KiCad schematic/PCB with approved footprints; run ERC/DRC on the real circuit.
3. Flash the built firmware on a verified board; complete PZEM/OLED/Wi-Fi/MQTT/OTA integration and boot-waveform tests. Install the debug APK on an emulator/device and test the API flow.
4. Provide lab/engineer for PE/thermal/isolation/load tests.
5. Review safety/regulatory and sign `safety/REVIEW_SIGNOFF_TEMPLATE.md`.
6. Only then consider fabrication/use.
