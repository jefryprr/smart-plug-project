# OPEN_QUESTIONS — Pra-Eksekusi

**Status:** `AWAITING_USER_DECISIONS`
**Terakhir diperbarui:** 2026-11-15
**Sumber:** `PRD.md` Bagian 01 dan 29

Semua pertanyaan di bawah masih `OPEN`. Tidak ada BOM final, design freeze, atau klaim kesiapan mains sampai pertanyaan safety-critical dijawab dan diverifikasi.

## Ringkasan severity

| Severity | ID | Dampak gate |
|---|---|---|
| `BLOCKER_SAFETY` | Q01, Q02, Q03, Q04, Q05, Q08, Q09, Q10, Q12, Q25 | BOM final, schematic mains, rating chain, isolasi, relay/fuse, state machine power-restore, fabrikasi |
| `BLOCKER_DESIGN` | Q06, Q11, Q15, Q16, Q17, Q18, Q21, Q22, Q23, Q24, Q26, Q27 | CAD, PCB architecture, firmware/backend/Android architecture, test scope |
| `NON_BLOCKER` | Q07, Q13, Q14, Q19, Q20, Q28 | Optimasi BOM/UI/notifikasi; dapat diputuskan kemudian dengan status `PROVISIONAL` |

## Daftar pertanyaan terbuka

| ID | Pertanyaan | Severity | Status | Catatan |
|---|---|---|---|---|
| Q01 | Bentuk produk akhir | BLOCKER_SAFETY | OPEN | Menentukan enclosure, strain relief, akses plug |
| Q02 | Soket output/plug input | BLOCKER_SAFETY | OPEN | Perlu analisis kompatibilitas Indonesia dan identitas produk |
| Q03 | Arus beban target | BLOCKER_SAFETY | OPEN | Rating final = nilai terendah rantai, bukan target |
| Q04 | Jenis beban | BLOCKER_SAFETY | OPEN | Induktif/inrush memerlukan penilaian terpisah |
| Q05 | Pemutusan konduktor | BLOCKER_SAFETY | OPEN | Plug Type F reversibel; PE tidak diputus |
| Q06 | Batas ukuran | BLOCKER_DESIGN | OPEN | Target mekanik, bukan izin memadatkan komponen berbahaya |
| Q07 | Anggaran BOM | NON_BLOCKER | OPEN | Optimasi, bukan alasan menurunkan safety |
| Q08 | Status board ESP32-S3 | BLOCKER_SAFETY | OPEN | Revisi board menentukan GPIO/RGB/strapping |
| Q09 | Status PZEM V4 | BLOCKER_SAFETY | OPEN | Manual batch nyata dan isolasi belum diverifikasi |
| Q10 | Relay/pemutus | BLOCKER_SAFETY | OPEN | Perlu 2–3 alternatif dan rating kontak |
| Q11 | Penempatan modul | BLOCKER_DESIGN | OPEN | Header hanya untuk modul LV yang cocok |
| Q12 | Target keselamatan | BLOCKER_SAFETY | OPEN | Menentukan klaim dan regulatory plan |
| Q13 | Layar | NON_BLOCKER | OPEN | Dapat `PROVISIONAL` |
| Q14 | Indikator | NON_BLOCKER | OPEN | Dapat `PROVISIONAL` |
| Q15 | Provisioning awal | BLOCKER_DESIGN | OPEN | BLE/SoftAP dan keamanan pairing |
| Q16 | Mode offline | BLOCKER_DESIGN | OPEN | RTC/time validity dan scheduler |
| Q17 | Cloud | BLOCKER_DESIGN | OPEN | Self-host/managed/hybrid |
| Q18 | Model akun | BLOCKER_DESIGN | OPEN | Single/multi-user/multi-tenant |
| Q19 | Notifikasi utama | NON_BLOCKER | OPEN | Telegram/push |
| Q20 | Home Assistant | NON_BLOCKER | OPEN | MQTT Discovery |
| Q21 | Histori | BLOCKER_DESIGN | OPEN | Lokal/cloud/retensi |
| Q22 | Stack backend | BLOCKER_DESIGN | OPEN | Perlu ADR |
| Q23 | Stack firmware | BLOCKER_DESIGN | OPEN | ESP-IDF vs Arduino-ESP32 |
| Q24 | Android | BLOCKER_DESIGN | OPEN | Expo dev build vs bare |
| Q25 | Power restore | BLOCKER_SAFETY | OPEN | Default OFF; opsi lain perlu review |
| Q26 | Fasilitas uji | BLOCKER_DESIGN | OPEN | Menentukan uji fisik `BLOCKED` atau tidak |
| Q27 | Urutan fase | BLOCKER_DESIGN | OPEN | Fase 1 dulu atau digital paralel |
| Q28 | Komponen dimiliki | NON_BLOCKER | OPEN | Memengaruhi BOM dan verifikasi |

## Aturan penyelesaian

1. Jawaban pengguna dicatat di `USER_ANSWERS.md` dan `USER_ANSWERS.yaml`.
2. Jawaban yang bertentangan ditandai `INCOMPATIBLE` dan dijelaskan, bukan dipaksa menjadi satu keputusan.
3. Jawaban `D` memicu riset opsi dan tabel perbandingan; bukan finalisasi otomatis.
4. Pertanyaan safety-critical tetap `OPEN` sampai ada keputusan eksplisit dan, bila relevan, review personel kompeten.
5. Setelah gate G0 (`REQUIREMENTS_CONFIRMED`), pekerjaan digital dapat berjalan; fabrikasi tetap menunggu F4.
