# 14 — Setup ESP-IDF

**Status lingkungan:** `PASS: ESP_IDF_6.1_INSTALLED`

## Instalasi

1. Ikuti dokumentasi resmi Espressif untuk Windows.
2. Pin versi stabil (catat commit/versi).
3. Target `esp32s3`.
4. Pastikan Python/CMake/Ninja/toolchain sesuai.

```powershell
idf.py --version
idf.py set-target esp32s3
```

## Build

```powershell
cd firmware
idf.py build
```

Jika berhasil, catat hash binary dan ukuran.

## Host core tests (tersedia sekarang)

```powershell
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
```

75 checks PASS. Target build ESP-IDF v6.1 juga PASS; lihat `reports/FIRMWARE_BUILD.md`. Ini bukan bukti flash/bench.

## Jangan

- Jangan mengklaim `.bin` jika build belum jalan.
- Jangan mengaktifkan secure boot/eFuse tanpa approval.
