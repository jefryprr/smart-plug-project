# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses a pre-1.0 prototype version.

**Design revision:** `REV_D_CORE_ONLY`  
**Status:** digital prototype, not for fabrication

---

## [Unreleased]

### Planned

- Component-level KiCad schematic and footprint review.
- Physical fit, thermal, PE, hipot/leakage, and 8 A load tests.
- Firmware flash and PZEM/OLED/Wi-Fi/MQTT/OTA integration.
- Android device/emulator test and production signing.
- PostgreSQL adapter, Docker deployment, MQTT TLS/ACL.
- Regulatory/standards review.

---

## [0.1.0] — 2026-11-16

### Added

- Complete digital engineering package: PRD, requirements traceability, BOM, research, safety dossier, KiCad block schematic, routed SELV carrier, routed mains-entry PSU board, wiring harnesses, CadQuery enclosure, firmware core, ESP-IDF skeleton, Fastify API, MQTT contract, Next.js dashboard, Android source, device simulator, tests, and reports.
- **REV_D_CORE_ONLY separate mains-entry PSU board** (50 × 65 mm): TB1/TB2 terminal blocks, 10 A fuse, 275 VAC MOV, SF96E 99 °C TCO, HLK-5M05, 1.1 A PTC + SMBJ5.0A TVS, 3× JST-XH 5 V outputs (carrier/relay/PZEM-conditional).
- **REV_D_CORE_ONLY SELV carrier** (100 × 70 mm): ESP32-S3 DevKitC-1 sockets, 74HCT125 + 10k/20k UART level shift, AO3400A relay driver, OLED/RTC/button/RGB connectors.
- 220 × 120 × 70 mm enclosure with 60 mm body + 10 mm lid, gasket, USB cover, DevKit reverse-insertion key, PZEM/relay/PSU brackets, and mechanical barrier.
- Research evidence table for the PSU board, including terminal/fuse/MOV/TCO/JST ratings, IPC-2221 trace calculation, creepage guidance, and conflicts resolved.
- 16 ADRs, 26 tutorials, 12 UI screenshots, and a full safety case.
- Professional repository documentation: README (EN/ID), start-here guide, FAQ, glossary, architecture, hardware/software guides, testing, status, contributing, security, support, roadmap, license, and notices.
- GitHub issue/PR templates, CODEOWNERS, Dependabot, and a CI workflow for typecheck/tests/web build.

### Changed

- Final load target: **8 A / ~1,840 W**, limited to electronics/SMPS loads.
- PZEM-004T V4 and 2-channel relay module are **off-board**.
- **TMP102 removed**; thermal protection is fuse + one-shot TCO.
- PZEM UART uses the module’s **internal optocouplers** in REV_D_CORE_ONLY; external ADuM1201 + B0505S removed, with fallback documented.
- Enclosure corrected to **220 × 120 × 70 mm**; 150 × 100 and 180 × 120 rejected.
- TCO corrected from SF169E (172 °C) to **SF96E (99 °C RFT, 84 °C holding)**.

### Fixed

- Terminal block BOM corrected to MKDS 1,5/2-5,08 to match the routed footprint; 250 V vs ≥300 V gap documented.
- Fuse holder BOM corrected to Littelfuse 111 clips to match the routed footprint.
- Software documentation commands corrected to `api:dev`/`web:dev`/`sim:dev`.

### Security

- No real secrets committed; `.env` ignored.
- JWT access/refresh rotation, scrypt, RBAC, tenant scoping, logger redaction.
- MQTT ACL plan; production TLS/ACL not deployed.
- No signed OTA/secure boot yet (`ADR-012`).

### Known limitations

- No physical 230 VAC assembly, energization, or lab test.
- No hipot/leakage/PE/thermal/8 A load evidence.
- No firmware flash/integration test.
- Android APK is debug-only and not device-tested.
- PostgreSQL adapter and Docker deployment not implemented.
- No certification/regulatory sign-off.

---

## Earlier history

The repository contains earlier commits for the initial digital package, off-board amendment, and REV_D_CORE_ONLY PSU board. See `git log` and [`reports/CHANGELOG.md`](reports/CHANGELOG.md) for commit-level rationale.
