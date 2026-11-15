# 21 — Telegram / Push

## Telegram (MVP)

- Buat bot melalui BotFather (akun pengguna, izin).
- Set `TELEGRAM_BOT_TOKEN` dan `TELEGRAM_CHAT_ID` di environment/secret store.
- Jangan commit token.
- Test: `POST /devices/{id}/notifications/test`.
- Tanpa token, backend memakai mock dan menandai `provider=mock`.

## Android push

- Belum diimplementasikan.
- Butuh FCM/Expo credentials, token lifecycle, opt-out, revoke.
- Tombol aksi tidak boleh bypass auth/lockout.

## Rate limit

- Test notification 2/min; alert dedup di backend.
