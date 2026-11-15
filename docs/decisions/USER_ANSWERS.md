# USER_ANSWERS — Keputusan Pengguna

**Status:** `CONFIRMED`
**Tanggal keputusan:** 15 November 2026
**Cara menjawab:** pengguna memilih seluruh rekomendasi agen pada kuesioner pra-eksekusi.
**PRD:** v1.0
**Catatan:** Jawaban `D` berarti pengguna meminta analisis/rekomendasi. Rekomendasi agen yang dipilih dicatat sebagai arah kerja `PROVISIONAL`, bukan persetujuan MPN final atau izin fabrikasi.

| ID | Keputusan | Status | Alasan/batasan |
|---|---|---|---|
| Q01 | **B** — Smart outlet *inline* berkabel | CONFIRMED | Ruang lebih lega, servisabel, strain relief jelas; bukan plug dinding mini. |
| Q02 | **D** — Analisis kompatibilitas Indonesia; lean **B** (Type E/F kombinasi ber-PE) | CONFIRMED (arah), PROVISIONAL (produk) | Produk soket/plug belum dipilih; wajib identitas model, rating, dan datasheet. |
| Q03 | **8 A final** (amendment pengguna, 2026-11-15; sebelumnya target 10 A) | CONFIRMED | 8 A × 230 V ≈ 1.840 W. Cukup untuk elektronik/SMPS rumah tangga; bukan pemanas/motor besar. Rating final tetap nilai terendah rantai + uji termal. |
| Q04 | **B** — Campuran elektronik rumah tangga termasuk SMPS | CONFIRMED | Beban motor/induktif/pemanas tidak dijanjikan; perlu penilaian terpisah. |
| Q05 | **A** — Tinjau pemutusan dua kutub | CONFIRMED | Plug Type F reversibel; PE tidak pernah diputus. |
| Q06 | **C** — Fleksibel; **220×120×70 CONFIRMED** (amandemen pengguna 2026-11-15) | CONFIRMED | 150×100 gagal fit; 180×120 ditolak karena PZEM/relay/socket hanya bisa di-stack dengan gap tidak layak. 220×120 PASS coarse; validasi fisik tetap wajib. |
| Q07 | **B** — BOM Rp500.000–750.000 | CONFIRMED | Optimasi, bukan alasan menurunkan komponen keselamatan. |
| Q08 | **B** — Beli ESP32-S3-DevKitC-1 resmi | CONFIRMED | Ketertelusuran board dan revisi; N16R8. |
| Q09 | **D** — Bandingkan varian metering; **PZEM off-board** | CONFIRMED (arah), PROVISIONAL (modul) | PZEM-004T V4 split CT jadi kandidat, bukan final, sampai manual batch diperiksa. Modul berdiri sendiri di enclosure, tidak di PCB. |
| Q10 | **2-channel optocoupler relay module umum**, off-board | CONFIRMED (arah), PROVISIONAL (part) | Modul 2 channel 5 V, kontak 10 A class (klaim umum), active-low, tidak di PCB; mounting di enclosure. Bukan DPST mekanis; risiko channel tidak linked harus ditinjau. |
| Q11 | **D** — Pilih berdasar isolasi/dimensi/produksi; lean B/C; PZEM + relay off-board | CONFIRMED (arah), PROVISIONAL (arsitektur) | Modul mains tidak dipaksa ke header biasa; bracket/standoff mekanik. |
| Q12 | **A** — Prototipe akademik di lab berpengalaman | CONFIRMED | Bukan produk konsumen; klaim berhenti di engineering/hardware validation. |
| Q13 | **A** — OLED I²C kecil 0,96" | CONFIRMED | SSD1306 128×64, 3,3 V. |
| Q14 | **C** — NeoPixel built-in + LED RGB panel | CONFIRMED | LED panel untuk visibilitas saat enclosure tertutup. |
| Q15 | **C** — BLE + fallback SoftAP | CONFIRMED | Jendela provisioning terbatas dan berautentikasi. |
| Q16 | **C** — Wi-Fi LAN + fisik + jadwal dengan RTC tervalidasi | CONFIRMED | RTC/SNTP dengan status validitas jam. |
| Q17 | **C** — Hybrid lokal + cloud | CONFIRMED | Implementasi awal self-host Docker Compose; cloud publik perlu izin. |
| Q18 | **D** — Sederhana sekarang, siap evolusi | CONFIRMED | Model data tenant-ready, RBAC dasar. |
| Q19 | **A** — Telegram sebagai notifikasi utama | CONFIRMED | Android push menjadi roadmap; tanpa akun Firebase pada MVP. |
| Q20 | **A** — MQTT Discovery | CONFIRMED | Home Assistant opsional, tetap tunduk lockout. |
| Q21 | **A** — Histori lokal pendek + cloud panjang | CONFIRMED | Ring buffer lokal terbatas; histori panjang di backend. |
| Q22 | **A** — Next.js + backend TypeScript terpisah; **C** untuk deployment | CONFIRMED | Docker Compose self-host. |
| Q23 | **A** — ESP-IDF | CONFIRMED | OTA rollback, partisi, provisioning, keamanan. |
| Q24 | **A** — React Native + Expo development build | CONFIRMED | Build lokal/prebuild; EAS berbayar tidak dipakai tanpa izin. |
| Q25 | **C** — Pengaturan pengguna, default **OFF** | CONFIRMED | Opsi ON otomatis tidak diaktifkan tanpa review. |
| Q26 | **A** — Hanya komputer, belum ada alat lab | CONFIRMED | Semua uji fisik/mains `BLOCKED`; tidak ada klaim HIL. |
| Q27 | **C** — Kedua fase digital paralel, safety gate tetap | CONFIRMED | Fabrikasi tetap menunggu F4 dan sign-off. |
| Q28 | **B** — Belum memiliki komponen | CONFIRMED | BOM dimulai dari nol; pembelian belum dilakukan. |

## Konsekuensi langsung

1. **BOM belum final.** Harga, MPN, dan ketersediaan akan dicatat dengan tanggal riset; nilai tidak diketahui dibiarkan kosong.
2. **Desain mains tetap provisional.** Schematic/PCB/CAD boleh dibuat sebagai artefak digital, tetapi tidak boleh berlabel `READY_FOR_FABRICATION` atau `READY_FOR_USE`.
3. **Uji fisik tidak diklaim.** Karena Q26=A, tidak ada HIL, uji beban, uji termal, uji dielektrik, atau uji PLN yang dijalankan.
4. **Fase 2 digital boleh berjalan** dengan device simulator dan fixtures sintetik, sesuai Q27=C.
5. **Perubahan pada Q03/Q04/Q05/Q08/Q09/Q10/Q12/Q25** wajib memicu impact analysis dan regresi artefak terkait.

## Amendments 2026-11-15 (setelah eksekusi awal)

Pengguna memberi instruksi baru dan saya catat sebagai amendment, bukan jawaban kuesioner baru:

| Item | Sebelum | Sesudah | Dampak |
|---|---|---|---|
| Rating | Target 10 A | **8 A final** | Module 2 channel 10 A class; label 1.840 W; batas beban eksplisit |
| Relay | DPST-NO PCB relay | **Modul optocoupler 2 channel off-board** | Dua channel L/N, active-low, bukan DPST mekanis; butuh bracket + driver MOSFET |
| PZEM | Off-board (sudah) | **Eksplisit off-board + bracket** | Tidak masuk PCB; mounting di enclosure |
| Enclosure | Target 150×100×70 | **220×120×70 CONFIRMED** | 150/180 gagal clearance; pengguna menyetujui Q06=C pada 2026-11-15 |
| PSU | Mean Well IRM-05-5 | **Hi-Link HLK-5M05** | 5 V 1 A / 5 W, 38×23×18 mm; efficiency ~70%, isolation/cert batch unverified |
| KiCad | Block/placement, CLI absent | **KiCad CLI 10.0.8 terpasang** | ERC/DRC/Gerber provisional dijalankan |
| Toolchain | Belum ada | **Sedang dipasang** | ESP-IDF/Android mengikuti batas disk |
| Sensor suhu | GY-TMP102 | **Dihapus** | Tidak ada sensor suhu; proteksi termal hardware (fuse/TCO) |
| Isolasi UART | ADuM1201 + B0505S | **Dihapus** | PZEM internal optocoupler; level shift 74HCT125 + divider |
| PCB | Placement-only 75x50 | **Routed SELV carrier 100x70 REV_B** | DRC 0/0, Gerber/drill; belum difabrikasi |
| Komponen/procurement | BOM unpriced | **Daftar belanja Indonesia 2026-11-16** | 43 baris listing-verified, 11 estimated; CORE Rp698.297 (restock Rp646.829), FULL Rp815.897; safety tetap unapproved |

## Konflik yang diperiksa

Tidak ada konflik eksplisit antarjawaban. Dua ketegangan yang dicatat:

- **Q01=B (inline) vs Q06=C (220×120×70)** — Dengan PZEM off-board + module relay 2 channel, 150×100 gagal dan 180×120 tidak memberi clearance layak. Pengguna mengonfirmasi **220×120×70**; jangan memaksa clearance turun.
- **Q03=8 A vs Q07=B (Rp500–750 rb)** — Harga listing 2026-11-15: elektronik inti Rp433.633; CORE lengkap Rp698.297 (Rp738.297 dengan ongkir); FULL Rp815.897 (Rp855.897 dengan ongkir). CORE masuk Rp750.000 bahkan tanpa restock (Rp698.297 + ongkir Rp40.000 = Rp738.297); restock memberi margin Rp686.829. Keselamatan diprioritaskan; FULL tidak dipaksa masuk budget dengan menurunkan fuse/MOV/TCO/PE/enclosure/isolasi.

## Persetujuan

| Peran | Nama | Tanggal | Catatan |
|---|---|---|---|
| Pemilik requirement | Pengguna proyek | 2026-11-15 | Memilih seluruh rekomendasi agen |
| Review keselamatan | **BELUM ADA** | — | Wajib untuk F2/F4/F5; bukan tanggung jawab agen |
| Review regulasi | **BELUM ADA** | — | Diperlukan bila klaim pasar konsumen dipertimbangkan |
