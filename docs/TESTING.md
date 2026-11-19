# Testing and Validation

**Design revision:** `REV_D_CORE_ONLY`  
**Last digital gate:** 2026-11-19 — **27 PASS / 11 BLOCKED / 0 FAIL**  
**Fabrication:** `NOT_RELEASED`

This page explains how to reproduce the digital tests and how to read the evidence. It does not authorize mains testing.

---

## 1. Test layers

| Layer | Command | What it proves | What it does not prove |
|---|---|---|---|
| TypeScript typecheck | `npm run typecheck` | Types are consistent across workspaces | Runtime behavior |
| Domain tests | `npm test` (includes workspace tests) | Command/energy/tariff/schedule rules | Hardware behavior |
| MQTT contract | included in `npm test` | Topics/schemas/fixtures | Broker TLS/ACL production |
| API + simulator | included in `npm test` | Auth, RBAC, commands, ACK, telemetry | Real device integration |
| Web build | `npm run build -w @smartplug/web` | Next.js production build | Browser behavior |
| Playwright + axe | `npx playwright test` | UI flows and basic accessibility | Physical button/onboard RGB |
| Firmware host tests | `powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1` | C safety-core logic | Flashed firmware |
| ESP-IDF build | `powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1` | Target compiles | Flash/boot/OTA |
| Static hardware checks | `.venv\Scripts\python.exe scripts\validate_all.py --e2e` | Wiring/GPIO/BOM/PSU consistency | Creepage, hipot, thermal |
| KiCad ERC/DRC | included in validation | Schematic/PCB rule checks | Functional circuit correctness |
| CadQuery/WireViz | included in validation | CAD/harness artifacts regenerate | Physical fit/continuity |

---

## 2. Reproduce the digital gate

### Prerequisites

- Node.js 22+
- Python 3.11 virtual environment at `.venv`
- Optional: KiCad 10 portable under `tools/kicad`, ESP-IDF v6.1 under `tools/esp-idf`

### Commands

```powershell
npm ci
npm run typecheck
npm test
npm run build -w @smartplug/web
npx playwright test
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1
.venv\Scripts\python.exe scripts\validate_all.py --e2e
```

The full validation gate writes:

- [`../reports/VALIDATION_SUMMARY.json`](../reports/VALIDATION_SUMMARY.json)
- [`../reports/TEST_MATRIX.csv`](../reports/TEST_MATRIX.csv)
- [`../reports/FAILURES.md`](../reports/FAILURES.md)
- [`../reports/logs/`](../reports/logs/)

Every claimed command must have an exit code and a log. Do not report a test as PASS without evidence.

---

## 3. Current results

Source: [`../reports/VALIDATION_SUMMARY.json`](../reports/VALIDATION_SUMMARY.json).

| Result | Count |
|---|---:|
| PASS | 27 |
| BLOCKED | 11 |
| FAIL | 0 |

Examples of PASS:

- 36 domain tests
- 12 MQTT contract tests
- 43 API tests
- 6 simulator tests
- 75 firmware host checks
- Next.js build + 5 Playwright tests + axe
- static wiring/GPIO/BOM/PSU crosschecks
- KiCad ERC 0, carrier DRC 0/0, PSU DRC 0/0
- WireViz 3 harnesses, CadQuery exports

Examples of BLOCKED:

- mains isolation review
- PE continuity
- thermal/fuse/surge
- boot-safe waveform
- physical load/temperature
- PostgreSQL migration
- production MQTT auth/ACL
- offline router/cloud test
- Android device/emulator test
- deployment clean-room
- full system HIL

---

## 4. What `PASS` means (and does not mean)

`PASS` means the specific command ran and exited successfully in the recorded environment. It does **not** mean:

- the hardware is safe;
- the PCB is functional;
- the isolation is sufficient;
- the enclosure fits;
- the firmware runs on a real board;
- the Android app works on a phone;
- the system is production-ready.

Static checks cannot prove creepage, clearance, dielectric strength, PE continuity, thermal rise, or EMC. Those require a lab and a competent engineer.

---

## 5. Evidence policy

- Every test claim points to a log in `reports/logs/` or a report in `reports/`.
- Mock/simulator results are labeled as such and never reported as HIL or PLN tests.
- A missing/blocked test is listed in [`../reports/FAILURES.md`](../reports/FAILURES.md), not silently omitted.
- Values that are not verified are marked `UNKNOWN`, `UNVERIFIED`, or `BLOCKED`.
- Do not invent test results, screenshots, or logs.

---

## 6. CI

The GitHub Actions workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs:

- `npm ci`
- `npm run typecheck`
- `npm test`
- `npm run build -w @smartplug/web`

Playwright, firmware, KiCad, and CAD steps are not in CI because they require browsers/toolchains/hardware that are not part of the default runner. They remain reproducible locally and are documented above.

---

## 7. Physical tests (not performed)

The following require a qualified lab/engineer and are **not** authorized by this repository for laypeople:

- insulation resistance / hipot / leakage
- PE continuity and fault-current
- 8 A thermal rise in the closed enclosure
- fuse/MOV/TCO coordination and trip test
- relay lifecycle and per-channel weld test
- inrush and load behavior
- EMC/regulatory tests
- enclosure flammability/impact/IP

See [`../safety/REVIEW_SIGNOFF_TEMPLATE.md`](../safety/REVIEW_SIGNOFF_TEMPLATE.md) and [`../reports/FAILURES.md`](../reports/FAILURES.md).
