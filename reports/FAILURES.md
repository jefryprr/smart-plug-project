# Failures and Blockers

Generated: 2026-11-24T14:08:27.058398+00:00

Overall: **FAIL**

| Test | Area | Status | Note | Log |
|---|---|---|---|---|
| T-SW-001B | TypeScript API | FAIL | API typecheck | reports\logs\T-SW-001B-20261124T140827Z.log |
| T-SW-001C | TypeScript web | FAIL | Web typecheck | reports\logs\T-SW-001C-20261124T140827Z.log |
| T-SW-001D | TypeScript simulator | FAIL | Simulator typecheck | reports\logs\T-SW-001D-20261124T140827Z.log |
| T-SW-005 | API + simulator integration | FAIL | 43 API tests incl. time + aedes+simulator ACK | reports\logs\T-SW-005-20261124T140827Z.log |
| T-SW-004B | Simulator tests | FAIL | 6 simulator tests incl. time | reports\logs\T-SW-004B-20261124T140827Z.log |
| T-SW-001E | Next.js build | FAIL | Next production build | reports\logs\T-SW-001E-20261124T140827Z.log |
| T-HW-003 | Connectivity crosscheck | FAIL | Wiring/GPIO/BOM static diff | reports\logs\T-HW-003-20261124T140827Z.log |
| T-HW-020 | PSU static crosscheck | FAIL | PSU nets/BOM/8A traces | reports\logs\T-HW-020-20261124T140827Z.log |
| T-SW-011 | Playwright E2E | BLOCKED | Run with --e2e to start API/web/simulator |  |
| T-HW-017 | ESP-IDF target build | FAIL | ESP-IDF v6.1, esp32s3, set-target + build; no flash | reports\logs\T-HW-017-20261124T140827Z.log |
| T-HW-011 | Mains isolation review | BLOCKED | No qualified reviewer/lab evidence |  |
| T-HW-012 | PE continuity | BLOCKED | No hardware/lab |  |
| T-HW-013 | Thermal/fuse/surge | BLOCKED | No lab |  |
| T-HW-014 | Boot-safe waveform | BLOCKED | No board/scope |  |
| T-HW-019 | Physical load/temperature | BLOCKED | No lab |  |
| T-SW-002 | PostgreSQL migration | BLOCKED | PostgreSQL/Docker not installed |  |
| T-SW-003 | MQTT broker auth/ACL | BLOCKED | Production broker/TLS not executed |  |
| T-SW-010 | Offline router/cloud test | BLOCKED | No deployed network stack |  |
| T-SW-013 | Android device/emulator test | BLOCKED | Debug APK built; no device/emulator install or UI test |  |
| T-SW-020 | Deployment clean-room | BLOCKED | Docker/Postgres not installed |  |
| T-SW-025 | Full system HIL | BLOCKED | No hardware/lab |  |
