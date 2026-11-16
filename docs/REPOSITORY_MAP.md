# Repository Map

This page explains what every top-level file and directory is for. It is a human-readable companion to [`deliverables/manifest.json`](../deliverables/manifest.json), which is the curated 26-category inventory with SHA-256 hashes.

> The working tree also contains local-only directories such as `node_modules/`, `.venv/`, `tools/`, `firmware/build/`, `apps/web/.next/`, and generated test output. They are intentionally excluded from git; see [`.gitignore`](../.gitignore).

---

## Root files

| Path | Purpose |
|---|---|
| `README.md` | English landing page |
| `README.id.md` | Indonesian landing page for a general audience |
| `LICENSE` | MIT license + safety notice |
| `NOTICE.md` | Third-party trademarks/datasheet notice |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTING.md` | Contribution rules and PR checklist |
| `CODE_OF_CONDUCT.md` | Community behavior |
| `SECURITY.md` | Private vulnerability reporting |
| `SUPPORT.md` | Where to get help and what maintainers cannot do |
| `CHANGELOG.md` | Release/change history |
| `ROADMAP.md` | Evidence gates F0–F8 |
| `AGENTS.md` | Operating rules for AI coding agents |
| `PRD.md` | Product Requirements Document (the contract) |
| `package.json` | Root npm workspace scripts/dependencies |
| `package-lock.json` | Reproducible npm lockfile |
| `playwright.config.ts` | Playwright configuration |
| `tsconfig.base.json` | Shared TypeScript configuration |
| `.env.example` | Environment variable names and dev-only defaults (no real secrets) |
| `.editorconfig` | Editor formatting rules |
| `.gitattributes` | Line-ending normalization for reproducible hashes |
| `.gitignore` | Excluded dependencies, builds, secrets, local tools, PDFs, etc. |

---

## Top-level directories

| Directory | Purpose |
|---|---|
| `apps/` | Runnable applications: Fastify API, Next.js web, device simulator, Android/Expo |
| `packages/` | Shared TypeScript packages: domain rules, API contract, MQTT contract |
| `firmware/` | Portable C safety core + ESP-IDF v6.1 skeleton |
| `hardware/` | KiCad schematic/PCB, PSU board, carrier, wiring, interfaces, mechanical CAD, manufacturing files |
| `research/` | Component research, feasibility, procurement, PSU evidence, datasheet manifest, risk/unknowns |
| `bom/` | Engineering BOM, procurement matrix, approvals, tools/consumables, summary |
| `safety/` | Isolation plan, rating chain, protection coordination, creepage worksheet, thermal, FMEA, PE, residual risks |
| `security/` | Threat model, authorization matrix, MQTT ACL plan, SBOM, dependency audit, security audit |
| `database/` | PostgreSQL migrations and development seed |
| `infrastructure/` | Docker Compose, Mosquitto/Caddy templates, deployment README |
| `docs/` | Start-here, FAQ, glossary, architecture, hardware/software/testing/safety guides, decisions, tutorials, UI/UX, operations |
| `validation/` | Derived wiring/netlist/GPIO/PSU/isolation crosschecks |
| `reports/` | Test matrix, validation summary, phase reports, build logs, research log, failures |
| `deliverables/` | Final engineering report, manifest, checksums |
| `tests/` | Playwright end-to-end tests and helpers |
| `scripts/` | Build, validation, generation, export, and manifest scripts |
| `data/` | Local runtime data (ignored; not committed) |
| `tools/` | Local portable toolchains (ignored; not committed) |
| `node_modules/`, `.venv/` | Local dependencies (ignored) |
| `test-results/`, `reports/playwright-report/` | Test output (ignored) |
| `hardware/manufacturing/released/` | Release gate directory; intentionally not populated |

---

## Where to look for a specific topic

| Topic | Start here |
|---|---|
| Product requirements | `PRD.md` |
| User decisions | `docs/decisions/USER_ANSWERS.md` |
| Why the design looks like this | `docs/decisions/ADR-INDEX.md` |
| Component choice / BOM | `bom/BOM_MASTER.md`, `research/COMPONENT_RESEARCH.md` |
| Indonesian prices/stock | `research/PROCUREMENT_INDONESIA.md`, `bom/BOM_PROCUREMENT.md` |
| PSU board (HLK-5M05) | `hardware/psu/README.md`, `research/PSU_BOARD_EVIDENCE.md` |
| SELV carrier | `hardware/carrier/README.md`, `hardware/kicad/README.md` |
| Wiring/connectors | `hardware/wiring/README.md`, `hardware/interfaces/gpio_map.md` |
| Enclosure | `hardware/mechanical/README.md`, `hardware/mechanical/FIT_ANALYSIS.md` |
| Safety case | `docs/SAFETY.md`, `safety/ISOLATION_PLAN.md`, `safety/RESIDUAL_RISK_REGISTER.csv` |
| Firmware | `firmware/README.md`, `reports/FIRMWARE_BUILD.md` |
| API/MQTT | `docs/SOFTWARE_GUIDE.md`, `packages/api-contract/openapi.yaml`, `packages/mqtt-contract/src/index.ts` |
| Web UI | `apps/web/`, `docs/ui-ux/`, `docs/ui-ux/screenshots/` |
| Android | `apps/android/`, `apps/android/README_BUILD_APK.md`, `reports/ANDROID_BUILD.md` |
| Tests/evidence | `reports/TEST_MATRIX.csv`, `reports/VALIDATION_SUMMARY.json`, `reports/FAILURES.md` |
| Contribution rules | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` |
| Beginner path | `docs/START_HERE.md`, `docs/FAQ.md`, `docs/GLOSSARY.md` |

---

## What is intentionally not committed

| Path | Why |
|---|---|
| `node_modules/`, `.venv/` | Dependencies are reproducible from lockfiles |
| `tools/` | Portable KiCad/ESP-IDF/Zig binaries are large and platform-specific |
| `firmware/build/`, `apps/web/.next/`, `dist/` | Generated build output |
| `data/*.db`, `data/*.db-wal`, `data/*.db-shm` | Local runtime database |
| `.env`, `.env.*` (except examples) | Secrets |
| `apps/android/.../debug.keystore`, `*.jks`, `*.keystore` | Signing material |
| `research/datasheets/*.pdf` | Third-party datasheets; links + SHA-256 are in `research/datasheets/MANIFEST.md` |
| `hardware/manufacturing/released/` | Release gate; must not be populated before F4 |
| `hardware/kicad/*.kicad_prl`, `*.lck` | Local KiCad state/locks |
| Test output | Regenerated by test commands |

If a file is missing from the manifest but should be tracked, add it to the appropriate category in `scripts/generate_manifest.mjs` and run `npm run manifest`.
