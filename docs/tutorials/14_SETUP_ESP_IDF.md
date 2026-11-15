# 14 — Setup ESP-IDF

**Status lingkungan:** `BLOCKED: ESP_IDF_NOT_INSTALLED`

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

74 checks PASS. Ini bukan bukti build ESP-IDF.

## Jangan

- Jangan mengklaim `.bin` jika build belum jalan.
- Jangan mengaktifkan secure boot/eFuse tanpa approval.
