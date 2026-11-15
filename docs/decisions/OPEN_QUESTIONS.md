# OPEN_QUESTIONS — Setelah Keputusan Pengguna

**Status:** `REQUIREMENTS_CONFIRMED` (Q01–Q28 dijawab 2026-11-15)
**Sumber keputusan:** `docs/decisions/USER_ANSWERS.md/.yaml`
**Keputusan:** pengguna memilih seluruh rekomendasi agen.

## 1. Pertanyaan kuesioner

Tidak ada Q01–Q28 yang masih `OPEN`. Beberapa jawaban adalah **arah** (D) yang tidak otomatis menjadi persetujuan MPN:

| ID | Jawaban | Status | Catatan |
|---|---|---|---|
| Q02 | D (analisis; lean Type E/F) | `CONFIRMED_DIRECTION` | Produk socket/plug belum dipilih |
| Q09 | D (bandingkan metering) | `CONFIRMED_DIRECTION` | PZEM V4 belum final |
| Q10 | C (studi relay) | `CONFIRMED_DIRECTION` | Relay final belum disetujui |
| Q11 | D (pilih modul) | `CONFIRMED_DIRECTION` | Arsitektur modul belum final |

## 2. Blocker yang masih terbuka (bukan pertanyaan kuesioner)

| ID | Severity | Blocker | Owner | Tindakan |
|---|---|---|---|---|
| B-001 | `BLOCKER_SAFETY` | Socket/plug Type F/E-F MPN, sertifikasi, PE, retensi | Hardware engineer | Pilih produk terlacak; ukur/uji |
| B-002 | `BLOCKER_SAFETY` | Relay DPST 10 A tidak tersedia; provisional 8 A | Hardware engineer | Turunkan rating atau ganti contactor/enclosure |
| B-003 | `BLOCKER_SAFETY` | PZEM V4 batch datasheet/pinout/isolation | Hardware engineer | Dapatkan manual batch; ukur |
| B-004 | `BLOCKER_SAFETY` | PE hardware/enclosure material | Mechanical engineer | Pilih part rated; uji kontinuitas |
| B-005 | `BLOCKER_SAFETY` | Clearance/creepage inputs/standard | Engineer | Isi worksheet; review |
| B-006 | `BLOCKER_SAFETY` | No lab/engineer/physical tests | Project owner | Sediakan fasilitas |
| B-007 | `BLOCKER_DESIGN` | KiCad CLI/ERC/DRC/Gerber | Hardware engineer | Install KiCad; selesaikan schematic/PCB |
| B-008 | `BLOCKER_DESIGN` | ESP-IDF build | Firmware engineer | Install toolchain; build/test |
| B-009 | `BLOCKER_DESIGN` | Android SDK/APK | Mobile engineer | Install SDK; build APK |
| B-010 | `BLOCKER_DESIGN` | PostgreSQL adapter/Docker deployment | Backend engineer | Implement/adapter; test |
| B-011 | `BLOCKER_DESIGN` | MQTT TLS/ACL production | Backend/security | Deploy staging; negative tests |
| B-012 | `BLOCKER_DESIGN` | Signed OTA/rollback | Firmware/security | Implement/test |
| B-013 | `NON_BLOCKER` | BOM prices/stock | Project owner | Get dated quotes |
| B-014 | `NON_BLOCKER` | Telegram/FCM credentials | Project owner | Provide via secret store/approval |
| B-015 | `NON_BLOCKER` | Regulatory/SNI classification | Project owner | Consult regulator/lab |

## 3. Aturan

1. Blocker safety tidak ditutup dengan asumsi.
2. Setiap perubahan Q02/Q03/Q04/Q05/Q08/Q09/Q10/Q12/Q25 memicu impact analysis.
3. `READY_FOR_FABRICATION`/`READY_FOR_USE` tidak diberikan sampai gate F4/F5/F6.
4. BOM tetap `UNPRICED`/`UNAPPROVED` sampai ada kutipan dan persetujuan.
