# 18 — Jalankan Web Next.js

```powershell
npm install
npm run dev:web
```

Buka http://localhost:3000. API harus jalan di port 4000.

## Build

```powershell
npm run build -w @smartplug/web
npm run start -w @smartplug/web
```

## E2E

```powershell
npx playwright test
```

5 tests PASS; screenshots di `docs/ui-ux/screenshots/`.

## Catatan

- Demo data sintetik berlabel.
- Jangan menganggap UI sebagai bukti status fisik.
- API URL rewrite ada di `apps/web/next.config.mjs`.
