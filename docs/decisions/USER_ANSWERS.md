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
| Q03 | **B** — Target 10 A | CONFIRMED | Rating final = nilai terendah rantai komponen dan hasil uji termal. |
| Q04 | **B** — Campuran elektronik rumah tangga termasuk SMPS | CONFIRMED | Beban motor/induktif tidak dijanjikan; perlu penilaian terpisah. |
| Q05 | **A** — Tinjau pemutusan dua kutub | CONFIRMED | Plug Type F reversibel; PE tidak pernah diputus. |
| Q06 | **B** — Target ≤150×100×70 mm | CONFIRMED | Target mekanik; keselamatan dan servisabilitas menang bila tidak muat. |
| Q07 | **B** — BOM Rp500.000–750.000 | CONFIRMED | Optimasi, bukan alasan menurunkan komponen keselamatan. |
| Q08 | **B** — Beli ESP32-S3-DevKitC-1 resmi | CONFIRMED | Ketertelusuran board dan revisi; N16R8. |
| Q09 | **D** — Bandingkan varian metering | CONFIRMED (arah), PROVISIONAL (modul) | PZEM-004T V4 split CT jadi kandidat, bukan final, sampai manual batch diperiksa. |
| Q10 | **C** — Studi 2–3 alternatif relay/pemutus | CONFIRMED (arah), PROVISIONAL (part) | Perlu rating kontak, inrush, isolasi, driver, fail-mode. |
| Q11 | **D** — Pilih berdasar isolasi/dimensi/produksi; lean B/C | CONFIRMED (arah), PROVISIONAL (arsitektur) | Modul mains tidak dipaksa ke header biasa. |
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

## Konflik yang diperiksa

Tidak ada konflik eksplisit antarjawaban. Dua ketegangan yang dicatat:

- **Q01=B (inline) vs Q06=B (≤150×100×70)** — PZEM-004T, relay dua kutub, PSU, fuse, terminal, dan socket ber-PE mungkin tidak muat dengan clearance memadai. Bila fit-check gagal, Q06 berubah menjadi **C** (fleksibel) setelah analisis, bukan memaksa komponen berbahaya menjadi rapat.
- **Q03=B (10 A) vs Q07=B (Rp500–750 rb)** — Relay dua kutub 10 A, PSU tersertifikasi, fuse holder, terminal, dan socket ber-PE dapat mendorong biaya di atas target. Keselamatan diprioritaskan; harga aktual akan dilaporkan.

## Persetujuan

| Peran | Nama | Tanggal | Catatan |
|---|---|---|---|
| Pemilik requirement | Pengguna proyek | 2026-11-15 | Memilih seluruh rekomendasi agen |
| Review keselamatan | **BELUM ADA** | — | Wajib untuk F2/F4/F5; bukan tanggung jawab agen |
| Review regulasi | **BELUM ADA** | — | Diperlukan bila klaim pasar konsumen dipertimbangkan |
