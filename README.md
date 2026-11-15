# ESP32-S3 IoT Smart Plug — Digital Engineering Package

**Design revision:** `REV_A_PROVISIONAL`
**Project status:** `PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`
**Fabrication:** `NOT_RELEASED` — do not send this repo to a PCB manufacturer.

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
| CadQuery | STEP/STL + renders | PASS |
| KiCad files parse | `kiutils` | PASS |
| npm audit | 0 known npm vulnerabilities | PASS |

## What is blocked

| Area | Reason |
|---|---|
| KiCad ERC/DRC/Gerber | KiCad CLI not installed |
| ESP-IDF build/firmware `.bin` | ESP-IDF not installed |
| Android APK | Android SDK not installed; only Expo Android bundle |
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
.venv\Scripts\python.exe scripts\validate_all.py --e2e
```

Demo login: `demo@example.com` / `demo1234` (local seed only; never production).
Demo pairing code: `123456` (single-use in the API; seed only).

### Local stack

```powershell
npm run dev:api      # API on :4000, SQLite, seeded demo
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
  android/             Expo Android source (APK blocked)
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
research/              component research, candidates, datasheets, unknowns
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

- Decisions: `docs/decisions/USER_ANSWERS.md`, `ASSUMPTION_REGISTER.md`, `ADR-*.md`
- Safety: `safety/ELECTRICAL_RATING_CHAIN.md`, `ISOLATION_PLAN.md`, `CLEARANCE_CREEPAGE_WORKSHEET.md`, `RESIDUAL_RISK_REGISTER.csv`
- Phase 1: `reports/PHASE_1_ENGINEERING_REPORT.md`
- Phase 2: `reports/PHASE_2_SOFTWARE_REPORT.md`
- Handoff: `deliverables/FINAL_ENGINEERING_REPORT.md`, `deliverables/manifest.json`
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

1. Select/verify socket, plug, relay, fuse, PSU, terminal, enclosure, PE hardware.
2. Install KiCad and complete component-level schematic/PCB; run ERC/DRC.
3. Install ESP-IDF/Android SDK; build firmware/APK.
4. Provide lab/engineer for PE/thermal/isolation/load tests.
5. Review safety/regulatory and sign `safety/REVIEW_SIGNOFF_TEMPLATE.md`.
6. Only then consider fabrication/use.
