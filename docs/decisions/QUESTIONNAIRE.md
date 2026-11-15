# Kuesioner Pra-Eksekusi — Smart Plug ESP32-S3

**Status:** `ANSWERED` — see `USER_ANSWERS.md` (2026-11-15)
**Tanggal:** 15 November 2026
**PRD:** v1.0
**Aturan:** Jawaban boleh ringkas, misalnya `Q01=B; Q02=B; Q03=B; ...`.
Opsi `D` berarti "minta analisis/rekomendasi"; agen akan meneliti dan mengajukan opsi, bukan menetapkan spesifikasi keselamatan secara sepihak.

> **Batas keselamatan:** BOM final dan desain 230 VAC belum ditetapkan. Jawaban di bawah belum merupakan persetujuan komponen atau izin fabrikasi. Semua rekomendasi bertanda `PROVISIONAL` sampai ada keputusan pengguna dan, untuk hal safety-critical, review personel kompeten.

---

## 01.1 Spesifikasi perangkat (wajib, safety-critical)

| ID | Pertanyaan | Opsi | Rekomendasi awal agen |
|---|---|---|---|
| Q01 | Bentuk produk akhir | A. Smart plug menempel dinding; B. Smart outlet inline berkabel; C. Stopkontak pintar meja/ekstensi satu soket; D. Minta rekomendasi | **B** untuk prototipe: ruang lebih lega, servisabel, strain relief jelas. A hanya setelah miniaturisasi tervalidasi. |
| Q02 | Soket output dan plug input | A. Type F/Schuko ber-PE; B. Type E/F kombinasi ber-PE; C. Standar lain; D. Analisis kompatibilitas Indonesia | **D** dengan lean ke **B** (E/F ber-PE) setelah verifikasi produk/standar. Hindari soket "universal" tanpa identitas. |
| Q03 | Arus beban maksimum target | A. 6 A; B. 10 A; C. 16 A; D. Setelah evaluasi part/rating | **B (10 A)** untuk target awal; rating final = nilai terendah rantai plug–socket–relay–PCB–terminal–fuse–thermal. 16 A menaikkan biaya/termal secara signifikan. |
| Q04 | Jenis beban | A. Resistif; B. Campuran elektronik rumah tangga termasuk SMPS; C. Motor/induktif; D. Semua dengan pembatasan eksplisit | **B** dengan batas tertulis. C memerlukan rating inrush/AC category dan uji tersendiri. Jangan menjanjikan "semua beban". |
| Q05 | Konfigurasi pemutusan konduktor | A. Tinjau pemutusan dua kutub karena plug Type F reversibel; B. Satu kutub dengan pembuktian; C. Engineer memilih dari studi standar | **A** untuk ditinjau: dua kutub lebih konservatif pada plug reversibel. PE tidak pernah diputus. |
| Q06 | Batas ukuran fisik target | A. ≤100×100×50 mm; B. ≤150×100×70 mm; C. Fleksibel, utamakan keselamatan/servis; D. Dimensi sendiri | **C** — pengguna mengonfirmasi **220×120×70 mm** pada 2026-11-15 setelah 150×100 dan 180×120 gagal clearance. |
| Q07 | Target biaya BOM | A. Rp350–500 ribu; B. Rp500–750 ribu; C. Fleksibel sampai tervalidasi; D. Anggaran lain | **B**, dengan catatan komponen safety dapat mendorong ke **C**. Harga aktual akan dicatat dengan tanggal dan sumber. |
| Q08 | Status board ESP32-S3 N16R8 | A. Sudah punya (kirim foto); B. Akan beli DevKitC-1 resmi; C. Clone pihak ketiga (kirim model/revisi); D. Belum pasti | **B** (Espressif DevKitC-1 resmi) untuk ketertelusuran. Jika A/C, verifikasi foto, revisi, GPIO RGB, strapping, USB. |
| Q09 | Modul PZEM-004T V4 Open CT | A. Sudah ada (foto); B. Akan beli sumber terverifikasi; C. Terbuka alternatif; D. Butuh perbandingan varian | **D**: bandingkan PZEM V4 split CT vs alternatif metering terisolasi. Jangan mengunci V4 sebelum manual batch nyata diperiksa. |
| Q10 | Relay/pemutus daya | A. Modul optocoupler dua kutub; B. Mekanisme lain yang memenuhi rating; C. Studi dan 2–3 alternatif; D. Sudah punya part tertentu | **C**: ajukan 2–3 alternatif DPST/dua kutub dengan rating kontak, inrush, isolasi, dan driver yang jelas. |
| Q11 | Penempatan modul | A. Carrier PCB untuk modul dilepas; B. Modul pada dudukan mekanik, PCB hanya kontrol LV; C. Hybrid; D. Pilih berdasar isolasi/dimensi/produksi | **D** dengan lean ke **B/C**: modul mains jangan dipaksa ke header biasa tanpa rating. |
| Q12 | Target keselamatan dan penggunaan | A. Prototipe akademik di lab berpengawasan; B. Uji lapangan terbatas setelah verifikasi; C. Produk konsumen; D. Belum ditentukan | **A** untuk lingkup saat ini. Ini berarti klaim berhenti di `ENGINEERING_REVIEW_REQUIRED`/`HARDWARE_VALIDATION_REQUIRED`, bukan produk konsumen. |

## 01.2 Pengalaman pengguna dan software

| ID | Pertanyaan | Opsi | Rekomendasi awal agen |
|---|---|---|---|
| Q13 | Layar | A. OLED I²C kecil; B. OLED lebih besar; C. Layar lain; D. Perbandingan teknis/biaya | **A** (0,96" SSD1306 I²C, 128×64) untuk prototipe. |
| Q14 | Indikator | A. NeoPixel built-in; B. LED RGB eksternal panel; C. Keduanya; D. Pilih berdasar akses visual | **C** bila board memiliki NeoPixel; minimal **B** agar terlihat saat enclosure tertutup. |
| Q15 | Pengaturan koneksi pertama | A. BLE; B. SoftAP; C. BLE + fallback SoftAP; D. Rekomendasi keamanan/UX | **C**: BLE untuk pairing, SoftAP fallback; keduanya berjendela waktu dan berautentikasi. |
| Q16 | Mode lokal offline | A. Wi-Fi LAN + aplikasi; B. Kontrol fisik + jadwal tersimpan; C. A+B dengan RTC tervalidasi; D. Desain paling tangguh | **C**: tombol fisik + jadwal lokal + RTC/SNTP dengan status validitas jam. |
| Q17 | Akses internet/cloud | A. Self-host VPS; B. Managed cloud; C. Hybrid lokal + cloud; D. Bandingkan biaya/keamanan | **C** untuk arsitektur; implementasi awal **A** (Docker Compose self-host), cloud publik hanya setelah izin/kredensial. |
| Q18 | Akun pengguna | A. Single-user; B. Multi-user satu rumah dengan peran; C. Multi-tenant; D. Mulai sederhana, siap evolusi | **D** dengan model data tenant-ready dan RBAC dasar. |
| Q19 | Notifikasi utama | A. Telegram; B. Android push; C. Keduanya; D. Lihat biaya/kelayakan | **A** untuk MVP (tanpa akun Firebase); **C** sebagai roadmap. |
| Q20 | Home Assistant | A. MQTT Discovery; B. Integrasi API spesifik; C. Keduanya; D. Opsional akhir | **A** (MQTT Discovery) sebagai jalur utama. |
| Q21 | Kebutuhan histori | A. Lokal pendek + cloud panjang; B. Hanya lokal; C. Cloud + backup; D. Rekomendasi durasi/biaya | **A**: ring buffer lokal terbatas + histori panjang di backend. |
| Q22 | Stack backend | A. Next.js + backend TypeScript terpisah; B. Next.js API monolit; C. Self-host Docker Compose; D. ADR | **A** dengan **C** untuk deployment; final lewat ADR. |
| Q23 | Stack firmware | A. ESP-IDF; B. Arduino-ESP32; C. Bandingkan; D. Sudah punya basis | **A** (ESP-IDF) untuk OTA rollback, partisi, provisioning, dan kontrol. |
| Q24 | Android | A. React Native + Expo development build; B. RN CLI/bare; C. Pilih berdasar BLE/notifikasi/APK lokal | **A** dengan local build/prebuild; hindari ketergantungan EAS berbayar. |
| Q25 | Penyalaan kembali setelah listrik pulih | A. Selalu OFF; B. Kondisi sebelumnya; C. Pengaturan pengguna, default OFF; D. Analisis risiko | **C**, default **OFF**. Opsi ON otomatis tidak diaktifkan tanpa review. |
| Q26 | Kapasitas engineering/fasilitas uji | A. Hanya komputer; B. Multimeter + beban uji aman; C. Lab + pembimbing kompeten; D. Rinci fasilitas | **A** berdasarkan environment saat ini. Semua uji fisik akan `BLOCKED` sampai fasilitas tersedia. |
| Q27 | Persetujuan tahapan | A. Fase 1 dulu; B. Fase 1, sign-off lalu Fase 2; C. Kedua fase digital paralel, safety gate tetap; D. Atur ulang | **C** untuk memaksimalkan artefak digital; keputusan keselamatan dan fabrikasi tetap terpisah. |
| Q28 | Komponen yang sudah dimiliki | A. Daftar/nomor model; B. Belum ada; C. Minta inventaris awal; D. Belum diketahui | **B** kecuali Anda sudah punya; jika A, kirim daftar/MPN/foto. |

---

## Format jawaban ringkas

Salin dan isi:

```text
Q01=B; Q02=D; Q03=8A_final; Q04=B; Q05=A; Q06=C_220x120x70; Q07=B; Q08=B;
Q09=D; Q10=C; Q11=D; Q12=A; Q13=A; Q14=C; Q15=C; Q16=C;
Q17=C; Q18=D; Q19=A; Q20=A; Q21=A; Q22=A; Q23=A; Q24=A;
Q25=C; Q26=A; Q27=C; Q28=B
```

Untuk jawaban `D` atau yang memerlukan penjelasan, tambahkan catatan, misalnya:

```text
Q02=D (prioritas kompatibilitas steker rumah Indonesia)
Q09=D (utamakan alternatif yang punya datasheet resmi)
Q26=A (belum punya alat lab)
```

## Setelah jawaban diterima

1. Jawaban dicatat ke `docs/decisions/USER_ANSWERS.md` dan `.yaml` dengan status `CONFIRMED`, `OPEN`, atau `INCOMPATIBLE`.
2. Konflik dan pertanyaan yang belum terjawab dicatat ke `docs/decisions/OPEN_QUESTIONS.md` dengan severity.
3. Riset komponen dimulai; **BOM belum final** dan **desain mains belum dinyatakan siap produksi**.
4. Untuk Q01–Q05, Q08–Q10, dan Q12, agen tidak melangkah ke manufacturing final tanpa jawaban dan review.
5. Setelah keputusan tersedia, Sprint 0–8 dijalankan secara otonom untuk pekerjaan digital; uji fisik tetap `BLOCKED` bila hardware/lab tidak ada.
