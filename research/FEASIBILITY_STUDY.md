# Feasibility Study — Smart Plug Inline ESP32-S3

**Design revision:** `REV_C_PSU_BOARD`
**Tanggal:** 15 November 2026
**Input keputusan:** Q01=B (inline), Q02=D (analisis; lean Type E/F), **Q03=8 A final (amendment)**, Q04=B (campuran elektronik/SMPS), Q05=A (tinjau dua kutub), **Q06=220×120×70 CONFIRMED (2026-11-15) karena 150×100 dan 180×120 gagal clearance**, Q07=B (Rp500–750 ribu), Q12=A (prototipe lab), Q26=A (hanya komputer).
**Status keseluruhan:** `FEASIBLE_WITH_CAVEATS` untuk bentuk/prototype digital; `BLOCKED` untuk clearance, isolasi, PE, termal, dan fabrikasi.

> Dokumen ini adalah analisis kelayakan, bukan persetujuan desain. Angka dimensi modul yang bertanda *approx* belum diukur pada sampel fisik. Tidak ada uji mains yang dilakukan.

## 1. Pertanyaan kelayakan dan jawaban

| No | Pertanyaan | Temuan | Status |
|---:|---|---|---|
| 1 | Apakah seluruh modul muat? | Secara volume kasar ya; tetapi PZEM, PSU, relay, socket, fuse, terminal, dan barrier isolasi membuat tata letak padat. Perlu fit-check dengan dimensi terukur. | `GO_WITH_CAVEATS` |
| 2 | Apakah jarak isolasi memadai? | Belum dapat dihitung: pollution degree, overvoltage category, material group, working voltage, dan altitude belum ditetapkan. Tidak boleh menebak angka creepage/clearance. | `BLOCKED` |
| 3 | Apakah ventilasi memadai? | Enclosure 220×120×70 confirmed memberi ruang side-by-side; relay module/terminal/PSU tetap hotspot. Ventilasi dan derating belum diuji. | `BLOCKED` |
| 4 | Apakah pengamanan soket/terminal memadai? | Socket/terminal belum dipilih dan belum diuji retensi/tarikan. | `BLOCKED` |
| 5 | Apakah jalur PE layak? | PE dapat dibuat langsung dari plug input ke socket output tanpa relay/fuse. Tetapi MPN terminal/stud dan uji kontinuitas belum ada. | `BLOCKED` |
| 6 | Apakah pemutusan konduktor dua kutub layak? | Module 2-channel off-board: dua SPDT independen, 10 A class claim; bukan DPST linked. Rating final 8 A. Uji tiap channel. | `PROVISIONAL` |
| 7 | Apakah biaya layak? | Harga sudah dikumpulkan (2026-11-15). Elektronik inti Rp433.633; CORE Rp717.087 (restock Rp665.619); FULL Rp834.687. CORE tidak masuk Rp750.000 tanpa restock (Rp757.087 all-in); restock memberi margin Rp705.619; FULL di atas budget. | `GO_WITH_CAVEATS` / `FULL_OVER_BUDGET` |
| 8 | Apakah suplai DC cukup? | Perkiraan peak ~0.58 A pada 5 V; HLK-5M05 1 A memberi margin ~42%, tetapi efisiensi ~70% dan panas ~2.1 W. Belum diukur. | `GO_WITH_CAVEATS` |
| 9 | Apakah PZEM dan CT dapat dipasang? | Modul besar tetapi mungkin; CT harus mengelilingi satu konduktor. Pinout/isolasi batch belum pasti. | `BLOCKED` |
| 10 | Apakah relay/terminal memadai? | Module 2-channel 10 A class claim (final 8 A); terminal/fuse holder belum rated/verified. | `PROVISIONAL` |
| 11 | Apakah kabel/connector dapat ditahan dari tarikan? | Perlu cable gland, strain relief mekanik, ferrule, dan terminal; belum ada desain final. | `BLOCKED` |
| 12 | Apakah area OLED/tombol bebas dari bagian berbahaya? | Bisa, jika OLED/button ditempatkan di sisi SELV dengan barrier dan kabel pendek. Perlu layout final. | `GO_WITH_CAVEATS` |
| 13 | Bagaimana layanan USB/debug dilindungi saat mains? | USB harus ditutup/dilarang saat mains aktif sampai isolasi tervalidasi. Service cover dan label wajib. | `BLOCKED` |

## 2. Perhitungan ruang

Target kerja: **220 ? 120 ? 70 mm** (confirmed; 150?100 dan 180?120 gagal clearance dengan PZEM + module 2 channel). Asumsi dinding 2.5 mm dan tutup 2.5 mm:

- Internal kasar: 215 ? 115 ? 65 mm = **1.607 cm?**.
- Volume envelope komponen (approx, belum terukur):
  - PZEM-004T V4: 89 × 53 × 24 mm ≈ 113 cm³
  - Hi-Link HLK-5M05: 38 ? 23 ? 18 mm ? 15.7 cm?
  - DevKitC-1: 68.6 × 25.4 × 10 mm ≈ 17 cm³
  - Modul relay 2 channel: 50 ? 24 ? 18 mm ? 21.6 cm?
  - Socket internal: 50 × 50 × 20 mm ≈ 50 cm³
  - OLED + button + RGB ≈ 5 cm³
  - Fuse/MOV/terminal/PCB/wiring ≈ 65 cm³
  - **Total ? 288 cm? (18% volume internal).**
- Kesimpulan: volume tidak mustahil, tetapi **clearance, barrier, bend radius, dan akses servis** mengurangi ruang efektif. Fit-check final harus memakai dimensi terukur, bukan *approx*.

**Keputusan:** `GO_WITH_CAVEATS`; jika fit-check gagal, Q06 berubah menjadi C (dimensi fleksibel) atau Q01 berubah, bukan memaksa clearance turun.

## 3. Arsitektur listrik yang layak secara konsep

```
Plug Type F (L,N,PE)
  ├─ L → fuse 10 A → MOV (L-N) → thermal cutoff → relay module CH1 (COM1/NO1) → socket L
  ├─ N → relay module CH2 (COM2/NO2) → socket N
  └─ PE ────────────────────────────────────────→ socket PE (tidak diputus)

L/N → PZEM voltage sense + CT around one conductor
L/N ? HLK-5M05 PSU ? 5 V SELV ? carrier ? ESP32/OLED/relay coils
PZEM UART → ADuM1201 barrier + B0505S isolated 5 V → ESP32 UART
```

**Catatan:**
- CT harus mengelilingi **satu** konduktor (L), bukan kabel utuh yang berisi N/PE.
- PE tidak boleh melalui relay, fuse, atau PCB trace sebagai satu-satunya jalur.
- PZEM sisi tegangan tetap mains-referenced; isolasi internal PZEM wajib diverifikasi (creepage + hipot). Tidak ada barrier eksternal.
- Relay dua kutub harus memutus L dan N; PE tetap kontinu.
- Fuse 10 A adalah backup, bukan izin 10 A kontinu.

## 4. Rating arus dan termal

| Elemen | Target/klaim | Bukti | Status |
|---|---|---|---|
| Socket | 16 A class | MPN belum dipilih | `UNVERIFIED` |
| Plug | 16 A class | MPN belum dipilih | `UNVERIFIED` |
| Relay module | 2-channel 10 A class claim; final 8 A | Datasheet vendor | `PENDING` |
| Fuse | 10 A time-lag | Datasheet seri | `PENDING` |
| Terminal | 10 A class | MPN/rating belum | `UNVERIFIED` |
| Kabel | 1.5 mm² H05VV-F | Perlu perhitungan/derating | `UNVERIFIED` |
| PCB | tidak membawa mains | low-voltage carrier | `GO` |
| Target kontinu | **8 A / 1.840 W** | Dipilih pengguna; thermal test required | `PROVISIONAL` |

**Rekomendasi:** gunakan **8 A/1.840 W** sebagai rating final, electronics/SMPS only. Module 2-channel bukan DPST linked; uji tiap channel. Jangan memberi label 10 A atau safety-DPST.

## 5. Power budget SELV

| Beban | Typical | Peak (estimasi) |
|---|---:|---:|
| ESP32-S3 DevKitC-1 + Wi-Fi | 180 mA | 350 mA |
| OLED | 15 mA | 20 mA |
| PZEM sisi terisolasi | 10 mA | 15 mA |
| Modul relay 2 channel (coil + LED) | 140 mA | 160 mA |
| WS2812 + level shifter | 10 mA | 30 mA |
| RTC DS3231 | 2 mA | 3 mA |
| **Total** | **~357 mA** | **~578 mA** |

Dengan HLK-5M05 1 A, peak ~58% (estimasi ~0.58 A); margin ~42%, tetapi efisiensi hanya ~70% dan panas ~2.1 W pada full load. Thermal/ripple/startup wajib diukur. Tambahkan 100 ?F bulk dan 100 nF decoupling.

## 6. Isolasi dan clearance

Input yang belum tersedia:
- Kategori overvoltage (II/III?) dan pollution degree (2?).
- Material group enclosure/PCB.
- Working voltage, rated impulse voltage, altitude.
- Apakah PZEM V4 benar-benar isolated pada batch yang dibeli.
- Konfigurasi PE dan jarak barrier.

**Metode yang akan dipakai:** IEC 60664-1 worksheet, dengan nilai diturunkan dari tabel standar yang sah, bukan angka default. Sampai itu selesai, schematic/PCB hanya `PROVISIONAL`, dan **tidak ada klaim isolasi**.

## 7. PZEM/CT dan UART

- PZEM V4 100 A split CT: CT rating bukan rating output.
- CT harus di sekitar L; arah arus ditandai.
- UART TTL PZEM tidak boleh langsung ke ESP32 tanpa bukti level/isolasi.
- REV_C_PSU_BOARD: PZEM internal optocoupler sebagai barrier; 74HCT125 + divider untuk level 5V/3.3V. Tidak ada ADuM/B0505S.
- Pinout aktual, baud, parity, register, dan CRC harus diverifikasi dari batch.
- Jika manual resmi tidak diperoleh, ganti ke ADE7953 atau metering lain setelah persetujuan.

**Status:** `BLOCKED`.

## 8. Relay, fuse, MOV, thermal cutoff

- Module 2-channel optocoupler: dua SPDT independen, 10 A class claim; bukan DPST. Perlu uji lifecycle per channel dan temperature rise.
- Fuse 10 A: perlu breaking capacity, holder rating, time-current curve, dan koordinasi.
- MOV 275 VAC: perlu surge study, thermal fuse coordination, dan end-of-life mode.
- Thermal cutoff 99 °C 10 A: perlu datasheet batch, clamping, dan uji trip. Jangan mengandalkan firmware.
- Tidak ada klaim proteksi lengkap sebelum pengujian lab.

## 9. PE dan mekanik

- PE path: plug PE → dedicated terminal/stud → socket PE; tidak melalui relay/fuse/PCB.
- Gunakan lock washer, torsi, dan test point kontinuitas.
- Cable gland M16 + internal anchor; kabel tidak boleh membebani solder/header.
- Socket harus ditahan mekanik agar tidak berputar/tercabut.
- Enclosure 3D print hanya prototipe mekanik; bukan enclosure listrik tersertifikasi.
- OLED/button/RGB di sisi SELV, dengan kabel dan barrier yang jelas.

## 10. USB/debug

- USB DevKitC-1 adalah SELV, tetapi PZEM/relay/PSU berada di sisi mains.
- Sampai isolasi assembly tervalidasi, **USB tidak boleh dihubungkan saat mains aktif**.
- Rencana: service cover dengan label, atau USB hanya untuk bench low-voltage.
- Jangan menaruh port USB di panel depan tanpa interlock/review.

## 11. Biaya dan pengadaan

- Harga sudah dikumpulkan untuk 57 baris: `bom/BOM_PROCUREMENT.csv`; 40 listing-verified, 17 `ESTIMATED`.
- Elektronik inti Rp433.633; CORE Rp717.087 (Rp757.087 dengan ongkir); CORE + mechanical addendum ~Rp745.087 (Rp785.087 dengan ongkir); CORE restock Rp665.619 (Rp705.619 dengan ongkir); CORE restock + addendum ~Rp693.619 (Rp733.619); FULL Rp834.687 (Rp874.687 dengan ongkir).
- Komponen safety yang mendorong biaya: PZEM 100 A Rp150.000, ESP32 Rp139.968, enclosure Rp99.684, HLK-5M05 Rp49.000, fuse/MOV/TCO Rp36.295, terminal/PE Rp29.360, PCB carrier Rp15.000.
- Target B (Rp500–750 ribu) **tidak tercapai** untuk CORE marketplace (Rp757.087 all-in) atau CORE + addendum (Rp785.087). CORE restock + addendum ~Rp733.619, hanya di bawah cap. FULL jauh di atas. Jangan menurunkan safety untuk memaksa budget.
- Beberapa komponen (PZEM, socket, enclosure, HLK, TCO) `DOCUMENTATION_DEFICIENT`; perlu sampel dan inspeksi.

## 12. Kesimpulan dan gate

**Boleh dilanjutkan secara digital:** schematic block, wiring, GPIO provisional, CAD parametrik, firmware mock, BOM riset.

**Tidak boleh dilanjutkan ke fabrikasi/energisasi:** sampai:
1. Q02 socket/plug dipilih dengan MPN/rating.
2. Relay/rating/fuse/terminal/PE/enclosure disetujui engineer.
3. Clearance/creepage dihitung dari standar.
4. Isolasi PZEM/UART dibuktikan.
5. Fit-check memakai dimensi terukur.
6. Uji fisik low-voltage dan lab dilakukan.

**Gate saat ini:** `F0 REQUIREMENTS_FROZEN` tercapai untuk arah kerja; `F1 PARTS_APPROVED` **belum**; `F2 ELECTRICAL_ARCH_APPROVED` **belum**; `F4 FABRICATION_RELEASED` **belum**.
