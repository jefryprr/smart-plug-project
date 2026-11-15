# Feasibility Study — Smart Plug Inline ESP32-S3

**Design revision:** `REV_A_PROVISIONAL`
**Tanggal:** 15 November 2026
**Input keputusan:** Q01=B (inline), Q02=D (analisis; lean Type E/F), Q03=B (target 10 A), Q04=B (campuran elektronik/SMPS), Q05=A (tinjau dua kutub), Q06=B (≤150×100×70 mm), Q07=B (Rp500–750 ribu), Q12=A (prototipe lab), Q26=A (hanya komputer).
**Status keseluruhan:** `FEASIBLE_WITH_CAVEATS` untuk bentuk/prototype digital; `BLOCKED` untuk clearance, isolasi, PE, termal, dan fabrikasi.

> Dokumen ini adalah analisis kelayakan, bukan persetujuan desain. Angka dimensi modul yang bertanda *approx* belum diukur pada sampel fisik. Tidak ada uji mains yang dilakukan.

## 1. Pertanyaan kelayakan dan jawaban

| No | Pertanyaan | Temuan | Status |
|---:|---|---|---|
| 1 | Apakah seluruh modul muat? | Secara volume kasar ya; tetapi PZEM, PSU, relay, socket, fuse, terminal, dan barrier isolasi membuat tata letak padat. Perlu fit-check dengan dimensi terukur. | `GO_WITH_CAVEATS` |
| 2 | Apakah jarak isolasi memadai? | Belum dapat dihitung: pollution degree, overvoltage category, material group, working voltage, dan altitude belum ditetapkan. Tidak boleh menebak angka creepage/clearance. | `BLOCKED` |
| 3 | Apakah ventilasi memadai? | Enclosure 150×100×70 memberi ruang, tetapi relay/terminal/PSU adalah hotspot. Ventilasi dan derating belum diuji. | `BLOCKED` |
| 4 | Apakah pengamanan soket/terminal memadai? | Socket/terminal belum dipilih dan belum diuji retensi/tarikan. | `BLOCKED` |
| 5 | Apakah jalur PE layak? | PE dapat dibuat langsung dari plug input ke socket output tanpa relay/fuse. Tetapi MPN terminal/stud dan uji kontinuitas belum ada. | `BLOCKED` |
| 6 | Apakah pemutusan konduktor dua kutub layak? | Relay DPST-NO 8 A tersedia secara komersial, tetapi target 10 A tidak tercapai. Perlu turunkan rating atau ganti contactor/enclosure. | `REDESIGN` |
| 7 | Apakah biaya layak? | Harga belum dikumpulkan. Komponen safety (PSU tersertifikasi, relay dua kutub, socket/plug ber-PE, enclosure flame-retardant) dapat melewati target B. | `REDESIGN_PENDING_QUOTES` |
| 8 | Apakah suplai DC cukup? | Perkiraan peak ~0.7 A pada 5 V; IRM-05-5 1 A memberi margin ~30%. Belum diukur. | `GO_WITH_CAVEATS` |
| 9 | Apakah PZEM dan CT dapat dipasang? | Modul besar tetapi mungkin; CT harus mengelilingi satu konduktor. Pinout/isolasi batch belum pasti. | `BLOCKED` |
| 10 | Apakah relay/terminal memadai? | Relay 8 A < target 10 A; terminal/fuse holder belum rated/verified. | `REDESIGN` |
| 11 | Apakah kabel/connector dapat ditahan dari tarikan? | Perlu cable gland, strain relief mekanik, ferrule, dan terminal; belum ada desain final. | `BLOCKED` |
| 12 | Apakah area OLED/tombol bebas dari bagian berbahaya? | Bisa, jika OLED/button ditempatkan di sisi SELV dengan barrier dan kabel pendek. Perlu layout final. | `GO_WITH_CAVEATS` |
| 13 | Bagaimana layanan USB/debug dilindungi saat mains? | USB harus ditutup/dilarang saat mains aktif sampai isolasi tervalidasi. Service cover dan label wajib. | `BLOCKED` |

## 2. Perhitungan ruang

Target eksternal: 150 × 100 × 70 mm. Asumsi dinding 2.5 mm dan tutup 2.5 mm:

- Internal kasar: 145 × 95 × 65 mm = **895 cm³**.
- Volume envelope komponen (approx, belum terukur):
  - PZEM-004T V4: 89 × 53 × 24 mm ≈ 113 cm³
  - Mean Well IRM-05-5: 53.5 × 28.5 × 19 mm ≈ 29 cm³
  - DevKitC-1: 68.6 × 25.4 × 10 mm ≈ 17 cm³
  - Relay RT2: 29 × 12.7 × 15.7 mm ≈ 6 cm³
  - Socket internal: 50 × 50 × 20 mm ≈ 50 cm³
  - OLED + button + RGB ≈ 5 cm³
  - Fuse/MOV/terminal/PCB/wiring ≈ 65 cm³
  - **Total ≈ 285 cm³ (32% volume internal).**
- Kesimpulan: volume tidak mustahil, tetapi **clearance, barrier, bend radius, dan akses servis** mengurangi ruang efektif. Fit-check final harus memakai dimensi terukur, bukan *approx*.

**Keputusan:** `GO_WITH_CAVEATS`; jika fit-check gagal, Q06 berubah menjadi C (dimensi fleksibel) atau Q01 berubah, bukan memaksa clearance turun.

## 3. Arsitektur listrik yang layak secara konsep

```
Plug Type F (L,N,PE)
  ├─ L → fuse 10 A → MOV (L-N) → thermal cutoff → relay pole 1 → socket L
  ├─ N → relay pole 2 → socket N
  └─ PE ────────────────────────────────────────→ socket PE (tidak diputus)

L/N → PZEM voltage sense + CT around one conductor
L/N → IRM-05-5 PSU → 5 V SELV → carrier → ESP32/OLED/relay coil
PZEM UART → ADuM1201 barrier + B0505S isolated 5 V → ESP32 UART
```

**Catatan:**
- CT harus mengelilingi **satu** konduktor (L), bukan kabel utuh yang berisi N/PE.
- PE tidak boleh melalui relay, fuse, atau PCB trace sebagai satu-satunya jalur.
- PZEM sisi tegangan tetap mains-referenced; barrier UART wajib sampai isolasi modul dibuktikan.
- Relay dua kutub harus memutus L dan N; PE tetap kontinu.
- Fuse 10 A adalah backup, bukan izin 10 A kontinu.

## 4. Rating arus dan termal

| Elemen | Target/klaim | Bukti | Status |
|---|---|---|---|
| Socket | 16 A class | MPN belum dipilih | `UNVERIFIED` |
| Plug | 16 A class | MPN belum dipilih | `UNVERIFIED` |
| Relay | 8 A / 250 VAC (RT2 IEC class) | Datasheet seri | `PENDING` |
| Fuse | 10 A time-lag | Datasheet seri | `PENDING` |
| Terminal | 10 A class | MPN/rating belum | `UNVERIFIED` |
| Kabel | 1.5 mm² H05VV-F | Perlu perhitungan/derating | `UNVERIFIED` |
| PCB | tidak membawa mains | low-voltage carrier | `GO` |
| Target kontinu | 10 A | Tidak tercapai oleh relay 8 A | `REDESIGN` |

**Rekomendasi:** turunkan rating kontinu final menjadi **8 A atau lebih rendah** (tergantung uji termal dan derating), atau gunakan contactor 2P 16 A dengan enclosure lebih besar. Jangan memberi label 10 A pada relay 8 A.

## 5. Power budget SELV

| Beban | Typical | Peak (estimasi) |
|---|---:|---:|
| ESP32-S3 DevKitC-1 + Wi-Fi | 180 mA | 350 mA |
| OLED | 15 mA | 20 mA |
| PZEM sisi terisolasi | 10 mA | 15 mA |
| Relay coil 5 V (RT2 class) | 80 mA | 80 mA |
| WS2812 + level shifter | 10 mA | 30 mA |
| TMP102 + RTC | 2 mA | 3 mA |
| **Total** | **~297 mA** | **~498 mA** |

Dengan IRM-05-5 1 A, peak ~50% (bukan 70%; angka ini revisi dari perkiraan awal). Margin baik, tetapi Wi-Fi burst dan inrush relay perlu diukur. Tambahkan 100 µF bulk dan 100 nF decoupling.

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
- Rencana provisional: `ADuM1201` + `B0505S-1WR3` barrier, dengan GND terpisah.
- Pinout aktual, baud, parity, register, dan CRC harus diverifikasi dari batch.
- Jika manual resmi tidak diperoleh, ganti ke ADE7953 atau metering lain setelah persetujuan.

**Status:** `BLOCKED`.

## 8. Relay, fuse, MOV, thermal cutoff

- Relay DPST-NO 8 A: dua kutub, tetapi rating di bawah target. Perlu uji lifecycle dan temperature rise.
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

- Harga belum dikumpulkan; BOM `UNPRICED`.
- Komponen safety yang mungkin mendorong biaya: PSU Mean Well, relay dua kutub, socket/plug ber-PE, fuse holder, enclosure flame-retardant, PE hardware, barrier isolasi.
- Target B (Rp500–750 ribu) belum dapat dikonfirmasi. Jika harga aktual melebihi, Q07 berubah ke C; jangan menurunkan safety.
- Beberapa komponen (PZEM, socket, enclosure) `DOCUMENTATION_DEFICIENT`; perlu sampel dan inspeksi.

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
