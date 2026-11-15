# 16 — Local Mock Test

## Jalankan simulator + API + broker

Cara termudah: gunakan script E2E yang menjalankan aedes + simulator + API:

```powershell
node scripts\e2e_api.mjs
```

Atau manual:
```powershell
npm run dev:api
npm run sim:dev
```

## Uji

- Login demo.
- ON/OFF → pending → APPLIED.
- Inject fault (simulator) → ON rejected.
- Telemetry/analytics.
- Event history.

## Batas

- Ini simulator, bukan HIL/PLN.
- Jangan menyalin hasil mock ke laporan fisik.
