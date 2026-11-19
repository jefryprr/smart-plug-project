# Integration Test Results — REV_D_CORE_ONLY

**Gate:** `PASS` for the tested digital path
**Generated:** 2026-11-15

## 1. Full command path

Test: `T-SW-005` — `apps/api/test/integration.test.ts`

```
POST /commands → API validation/idempotency → MQTT publish → simulator subscribes
→ safety decision → state + ACK → MQTT bridge → command APPLIED → GET status
```

Result: **PASS** for 4 integration cases:
- valid ON → APPLIED, device commanded ON.
- simulator fault lockout → API rejects ON, accepts OFF, OFF APPLIED.
- telemetry ingestion → API telemetry `data_available`.
- simulator availability offline → API device OFFLINE.

## 2. MQTT contract

- 12 tests: topic build/parse, device ID validation, ACL direction, retain policy, telemetry/command/ACK schemas, JSON decode errors.
- Result: **PASS**.

## 3. Web E2E

Test: `T-SW-011` — Playwright, 5 tests, 1 worker.

- Login → dashboard.
- Device tabs: analytics, schedules, automation, events, diagnostics, settings.
- ON/OFF → simulator → APPLIED.
- axe WCAG 2 A/AA on login/dashboard: no serious/critical.
- Mobile 390×844 dashboard/device.
- Result: **PASS**; screenshots in `docs/ui-ux/screenshots/`.

## 4. Static connectivity

Test: `T-HW-003` — `scripts/validate_connectivity.py`.

- PE path: PASS (P1:PE ↔ X1:PE, no relay/fuse).
- Relay contacts separate: PASS.
- Relay coil SELV: PASS.
- UART isolator sides not shorted: PASS.
- Mains/SELV static net separation: PASS.
- GPIO map vs firmware defines: PASS (11 defines; board revision still unverified).
- BOM PCBA refs present in master: PASS.
- Result: **PASS** static; not a KiCad netlist/ERC/DRC.

## 5. Wiring/CAD/KiCad artifacts

- 3 WireViz harnesses rendered to GV/SVG/PNG/PDF: **PASS**.
- CadQuery STEP/STL + assembly + renders: **PASS** (file generation, not physical fit).
- Native KiCad files parse with `kiutils`: **PASS**; ERC/DRC/Gerber **BLOCKED**.

## 6. Not integration-tested

| Path | Status | Reason |
|---|---|---|
| PostgreSQL migrations | `BLOCKED` | Postgres/Docker not installed; API Postgres adapter missing |
| MQTT TLS/ACL production | `BLOCKED` | Broker/TLS/certs not deployed |
| Cloud deploy | `BLOCKED` | No VPS/domain/credentials |
| Android APK/emulator | `BLOCKED` | Android SDK not installed |
| Hardware/HIL/PLN | `BLOCKED` | No board/lab |
| Power loss/OTA rollback | `BLOCKED` | No ESP-IDF build/board |
