# 15 — Flash dan Konfigurasi

**Status:** `BLOCKED` — no board; firmware build exists but has not been flashed.

## Prasyarat

- Board terverifikasi, adaptor USB data, port COM.
- Firmware binary hash.
- Bench low-voltage, relay coil/load simulator.
- Prosedur recovery.

## Flash

```powershell
idf.py -p COMx flash monitor
```

## Setelah flash

- Verifikasi boot log, relay OFF.
- Jangan hubungkan mains.
- Uji tombol/ACK low-voltage.
- Catat firmware version/hash.

## Stop

Jika relay aktif saat boot atau board panas, lepas daya dan debug low-voltage.
