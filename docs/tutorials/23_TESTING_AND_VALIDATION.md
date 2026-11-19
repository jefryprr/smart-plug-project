# 23 — Testing dan Validasi

## Jalankan

```powershell
npm run test
npm run typecheck
npm run build -w @smartplug/web
npx playwright test
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
.venv\Scripts\python.exe scripts\validate_connectivity.py
```

## Status saat ini

- Domain 34 tests PASS.
- MQTT 12 tests PASS.
- API 43 tests PASS (incl. simulator integration).
- Firmware core 74 checks PASS.
- Web 5 Playwright tests PASS; axe login/dashboard PASS.
- Static connectivity PASS.
- KiCad ERC 0 and routed carrier DRC 0/0 PASS; physical validation still BLOCKED.
- ESP-IDF v6.1 target build and Android debug APK PASS; Docker/Postgres remain BLOCKED.

## Arti status

- `PASS` digital ≠ HIL/PLN.
- `BLOCKED` bukan PASS.
- Jangan menghapus warning untuk membuat PASS.
