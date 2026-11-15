# 20 — Pair Device

## Demo lokal

- Buka `/onboarding/pair-device`.
- Kode demo `123456` (seed).
- Kode sekali pakai, expiry 30 hari di seed.

## Alur produksi (rencana)

1. Device unprovisioned, relay OFF.
2. BLE/SoftAP window.
3. Kode pairing sekali pakai.
4. Wi-Fi credential aman.
5. Claim di web/Android.
6. Window ditutup; audit.

## Keamanan

- Jangan menulis kode/SSID/password ke log.
- Jangan memakai kode demo di produksi.
- Pairing bukan bukti keselamatan listrik.
