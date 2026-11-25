# Re-analisis PCB & Dampak ke Enclosure 3D

**Tanggal:** 2026-11-25  
**Revisi:** `REV_D_CORE_ONLY`  
**Scope:** `hardware/kicad/psu_rev_d.kicad_pcb`, `hardware/kicad/smartplug.kicad_pcb`, `hardware/mechanical/`  
**Status:** `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_FABRICATION`

> Ini analisis teknik digital, bukan sertifikasi, bukan creepage IEC, dan bukan izin energisasi mains.
> Semua dimensi part yang belum diukur tetap `UNVERIFIED`.

---

## 1. Kesimpulan singkat

1. **PCB sudah lebih benar daripada rev sebelumnya**, tetapi belum bisa disebut “benar” untuk fabrikasi. DRC kedua board **0 violations / 0 unconnected**, namun DRC hanya menegakkan aturan 0.15/0.5 mm, bukan creepage mains.
2. **Perubahan PCB tidak mengubah outline, mounting hole, atau posisi boss enclosure.** PSU tetap 50 × 65 mm dengan H1/H3/H4; carrier tetap 100 × 70 mm dengan empat lubang M3. Bracket PSU dan boss carrier **tidak perlu digeser**.
3. **Ada satu penyesuaian enclosure yang kemungkinan besar diperlukan:** fuse holder **BLX-A** berada tepat di bawah relay shelf. Clearance vertikal tertutup hanya **~10.4 mm** (holder 18 mm di atas board, shelf bawah z=40). Swing tutup BLX-A tidak dimodelkan; akses servis fuse harus dianggap `REVIEW REQUIRED`. Solusinya: ukur sample, lalu tambah cutout servis di relay shelf, geser shelf, atau ganti holder.
4. **Perubahan carrier (C4, JP1, TP1/TP2/TP4/TP5, C3, U9)** semuanya low-profile dan tetap di dalam envelope carrier. Tidak perlu ubah body/lid/panel. JP1 cukup diakses dengan lid terbuka.
5. **Masih ada gap P0:** KF129 body/rating, pitch BLX-A, dimensi MOV/TCO, creepage IEC, PE path, schematic parity, HLK hipot, relay safety case, EMC, thermal 6 A, dan stackup 2 oz.

---

## 2. Data PCB terukur (2026-11-25)

| Metrik | PSU mains | Carrier SELV |
|---|---:|---:|
| Ukuran | 50.1 × 65.1 mm | 100.1 × 70.1 mm |
| Layer | 2 | 2 |
| Footprint total | 19 | 29 |
| Footprint assembled | 13 | 17 PCBA (TP/JP fitur PCB, tidak dibeli) |
| Track segment | 37 | 109 |
| Via | 6 | 15 |
| Width track | 1.0 mm (18), 1.5 mm (5), 2.5 mm (14) | 0.3 mm (59), 0.6 mm (50) |
| Layer track | F.Cu 34 / B.Cu 3 | F.Cu 97 / B.Cu 12 |
| Copper zone | 0 | 1 (GND, B.Cu) |
| DRC | 0/0 @ 0.5 mm | 0/0 @ 0.15 mm |
| Board min clearance | 0.0 mm | 0.15 mm |
| Schematic parity | tidak ada | tidak ada |

**Catatan:** `m_MinClearance = 0.0` di PSU. DRC 0/0 bukan bukti creepage/clearance. Audit geometri terpisah ada di `reports/psu_clearance_audit_20261124.json`.

---

## 3. Verifikasi konektivitas & footprint

### 3.1 PSU

| Ref | Footprint | Part aktual | Hasil |
|---|---|---|---|
| TB1/TB2 | Phoenix MKDS 5.08 mm, pad 2.6/drill 1.3 | KF129-2P, 300 V/25 A claim | **Pad-compatible only**; body/rating/retensi `UNVERIFIED` |
| F1 | BLX-A 2-pad, pitch 21.5 mm, pad 2.6/drill 1.6 | BLX-A 6.3 A/250 V | **Provisional**; pitch 21.5 mm dari seller, belum diukur |
| MOV1 | RV disc D12, pitch 7.5 mm | 10D271K, disc 10 mm | **Provisional**; diameter/pitch sample belum diukur |
| TF1 | Custom 2-pad, pitch 5.1 mm, body 10 × 5 mm | Generic 96 °C, 10 A | **UNVERIFIED**; marking/dimensi sample belum diukur |
| PS1 | Custom HLK, 33.6/6/18 mm | HLK-5M05 | **VERIFIED geometry** (sama dengan KiCad official); sample belum diukur |
| F2 | 1206 | PTC 1.0 A | **Provisional**; hold/trip belum diukur |
| D1 | SMB | SMBJ5.0A 600 W | **Provisional**; marking belum diukur |
| J5/J6/J7 | JST-XH 2-pin | JST-XH 2-pin | **OK** keying/rating perlu verifikasi |

- Net PSU: `L_IN`, `N_MAINS`, `L_FUSED`, `L_LOAD`, `+5V_PRE`, `+5V`, `GND`; tidak ada PE net.
- Urutan proteksi: TB1 L → F1 → L_FUSED → MOV1/TF1 → L_LOAD → TB2/HLK. Sesuai desain.
- F1 pad2 (L_FUSED) → TF1 pad1 (L_FUSED) berjarak **2.5 mm** center; pad radii 1.3 + 0.65 → **gap 0.55 mm**. Same net, tidak lagi 0.05 mm.
- TF1 body sekarang di x=38.5..48.5, y=34..39; right edge **1.5 mm** dari board edge 50; F1 body bottom 40.25 → gap 1.25 mm; HLK body top 33 → gap 1 mm.

### 3.2 Carrier

| Ref | Perubahan | Status |
|---|---|---|
| U9 | DIP-14 footprint untuk adapter SOP-14; dipindah ke x=72 agar clear dari body DevKit | **PROVISIONAL**; adapter height/width belum diukur |
| C3 | 100 nF di (80,31), ~3.2 mm dari U9 pin 14 | **PROVISIONAL**; body C3 ke U9 body hanya ~0.44 mm, perlu review |
| C4 | 100 nF RELAY_GATE–GND di (88,30) | **PROVISIONAL**; verifikasi edge relay |
| JP1 | Solder jumper `+5V_IN`–`+5V` di (63,63), rot 180 | **PROVISIONAL**; harus disolder untuk operasi PSU, dibuka untuk service USB |
| TP1/TP2/TP4/TP5 | +5V, GND, RELAY_GATE, BUTTON | **OK**; +3V3/PZEM/PE belum ada |
| J2/J3 | 4-pin, pin 1 NC | **RISK**; kabel 4-pin bisa salah pasang |

- Net carrier: `+5V`, `+5V_IN`, `+3V3`, `GND`, `BUTTON`, `RELAY_CTRL`, `RELAY_GATE`, `RELAY_IN`, `PZEM_TX_3V3`, `PZEM_RX_5V`, `PZEM_TX_5V`, `PZEM_RX_3V3`.
- `+5V_IN` sekarang 0.6 mm (sebelumnya 0.3 mm), cukup untuk arus carrier ~0.58 A.
- Tidak ada net mains di carrier.

---

## 4. Clearance / creepage

| Pasangan | Geometri | Status |
|---|---:|---|
| Mains–SELV (PSU) | **9.05 mm** (N bus ke pad GND HLK) | **UNVERIFIED**; bukan creepage IEC |
| L–N (PSU) | **1.3 mm** (L_LOAD vs cabang AC N) | **UNVERIFIED**; functional gap, bukan isolasi |
| L_FUSED–N di MOV | ~1.65 mm | **UNVERIFIED**; MOV memang melintasi L–N |
| Terminal pad gap | 5.08 mm pitch, pad 2.6 → **2.48 mm** | **UNVERIFIED**; body KF129 harus diukur |
| F1 pad–TF1 pad | **0.55 mm** (same net) | **PROVISIONAL**; manufacturing review |
| TF1 body–board edge | **1.5 mm** | **PROVISIONAL** |
| F1 body–board edge | **1.75 mm**; pad edge 0.7 mm | **PROVISIONAL**; copper-edge 0.5 lolos |
| Slot isolasi | 2 mm, x=19..21, y=0..45 | **BLOCKED**; belum kontinu sampai tepi atas, belum dihitung IEC |

**Kesimpulan:** angka 9.05 mm terlihat besar, tetapi jalur creepage bisa memutar ujung slot, melewati body HLK, atau melalui pad terminal. Tidak ada klaim IEC sampai engineer menghitung dengan OVC/pollution degree/material group/coating.

---

## 5. Arus, termal, EMC

- Rating sistem **6 A provisional** karena holder BLX-A 6.3 A. Target 8 A tidak dapat diklaim.
- 2.5 mm / 2 oz untuk 6 A masih konservatif menurut IPC-2152, tetapi **bukan hasil uji termal**.
- HLK disipasi ~2.1 W pada 5 W; TCO holding 84 °C; thermal test 6 A di enclosure tertutup belum dilakukan.
- PTC 1.0 A vs HLK 1 A: margin tipis; peak Wi-Fi/relay belum diukur.
- Tidak ada filter EMC mains (X2/Y2/CM choke); HLK switching. Pre-scan CISPR 32/EN 55032 belum ada.
- Carrier: C4 membantu edge gate, tetapi trace GPIO→R1 masih panjang (~68 mm). Belum ada test waveform.

---

## 6. Dampak ke enclosure 3D

### 6.1 Yang **tidak** perlu diubah

| Item | Alasan |
|---|---|
| Body 220 × 120 × 70 | Outline PCB dan tinggi komponen masih di dalam envelope 30 mm; tidak ada perubahan luar. |
| Lid + gasket | Tidak ada komponen baru yang menembus lid; button/RGB/USB cover tidak berubah. |
| Socket cutout 45.6 / flange 50 × 50 | Posisi socket tidak berubah; PSU board tidak bergeser. |
| M16 gland | Posisi tidak berubah. |
| Barrier x=-4 | Tidak berubah oleh PCB; catatan: barrier menyentuh tepi carrier x=-5 (0 mm), perlu review tersendiri. |
| PSU bracket 50 × 65, holes H1/H3/H4 | Board outline dan lubang tidak berubah. |
| Carrier boss 4× M3 | Carrier outline dan lubang tidak berubah. |

### 6.2 Yang **perlu review/perubahan**

| Item | Temuan | Rekomendasi |
|---|---|---|
| Relay shelf vs F1 | F1 BLX-A di bawah shelf (x 93.75..104.25, y -14.75..8.25). Holder tertutup ~18 mm → top z~29.6; shelf bawah z=40 → **10.4 mm**. Swing tutup tidak dimodelkan. | Ukur BLX-A. Jika tutup tidak bisa dibuka: tambah cutout servis di shelf, geser shelf, atau ganti holder. Jangan cetak final sebelum check. |
| TB1 wire entry | Body KF129 TB1 berakhir di y~11.6, shelf edge y=11 → wire entry tepat di tepi shelf. | Cek bend radius kabel 1.5 mm² dan strain relief; mungkin perlu notch di shelf. |
| KF129 body | Body/tinggi/wire entry belum diukur; PCB hanya pad-compatible. | Ukur sample; jika body lebih besar, bracket/enclosure cable route bisa berubah. |
| U9 adapter vs DevKit | U9 body x 70.92..80.69; DevKit body berakhir ~x 68.17 → **2.75 mm** gap. Adapter bisa lebih lebar. | Ukur adapter + DevKit; jika <1 mm, geser U9 lagi atau pakai adapter low-profile. |
| C3 vs U9 body | C3 body bottom 32.01; U9 body top 32.45 → **0.44 mm**. | Review visual/3D; jika terlalu mepet, geser C3 ke (80,30) atau ganti 0603. |
| Barirer–carrier | Barrier x=-5..-3, carrier edge x=-5 → **0 mm**. | Beri clearance 1–2 mm atau slot; pastikan tidak menjepit tepi PCB. |

### 6.3 Angka tinggi komponen (perkiraan)

| Komponen | Tinggi perkiraan | Top z (board top 11.6) | Catatan |
|---|---:|---:|---|
| HLK-5M05 | 18 mm | 29.6 | datasheet |
| BLX-A holder | 18 mm (worst case) | 29.6 | cover swing belum dihitung |
| KF129-2P | ~10 mm | 21.6 | sample |
| MOV 10D271K | ~12 mm | 23.6 | disc 10 mm |
| TCO generic | ~5 mm | 16.6 | sample |
| Relay shelf bottom | — | 40.0 | 3 mm plate |
| Relay module top | 18 mm di shelf | 61.0 | shelf 43..61 |
| Lid inner | — | 67.5 | clearance 6.5 mm ke relay |

---

## 7. Temuan berprioritas

### P0 — blocking

1. **BLX-A pitch/body** belum diukur; footprint 21.5 mm berasal dari deskripsi seller, bukan drawing.
2. **KF129-2P** body/rating/retensi belum terbukti; PCB hanya cocok di pad Phoenix.
3. **MOV 10D271K** dan **TCO generic** belum diukur; footprint D12/5.1 mm provisional.
4. **Creepage/clearance IEC 60664-1** belum dihitung; slot 2 mm belum kontinu.
5. **PE path** tidak ada di PCB; chassis stud harus diuji kontinuitas/fault current.
6. **Schematic level-komponen / netlist parity** tidak ada.
7. **HLK isolation/hipot/certificate** belum diuji.
8. **Relay module bukan safety-rated disconnect**; dua SPDT independen.
9. **Rating 6 A** harus dikunci di PRD/label; 8 A tidak boleh diklaim.

### P1 — sebelum prototipe dinyalakan

10. **F1 service access** di bawah relay shelf; cutout/relokasi belum diputuskan.
11. **TB1 wire bend** di tepi shelf.
12. **U9 adapter vs DevKit** clearance 2.75 mm (adapter width unverified).
13. **C3–U9 body** 0.44 mm.
14. **Barrier–carrier** 0 mm.
15. **EMC filter/pre-scan** dan thermal 6 A belum ada.
16. **PTC 1.0 A vs HLK 1 A** margin tipis; peak load belum diukur.
17. **Test point +3V3/PZEM/PE** belum ada.
18. **J2/J3 pin 1 NC** misplug risk.
19. **2 oz stackup** belum masuk file/fab notes.

### P2 — DFM

20. Panelization, surface finish, annular ring, via tenting, copper balance.
21. Test coupon 2 oz/annular ring/thermal.
22. Refdes disembunyikan; perlu assembly map.

---

## 8. Rekomendasi tindakan

1. **Ukur sample** BLX-A (pitch, body, cover swing), KF129 (body, height, wire entry), MOV 10D271K, TCO generic, adapter SOP14, dan DevKit.
2. **Putuskan F1 service access**: cutout relay shelf vs geser shelf vs ganti holder. Jangan cetak final sebelum ini.
3. **Hitung creepage IEC 60664-1** dan review slot/barrier; update netclass/keepout.
4. **Buat schematic level-komponen** + ERC + netlist parity.
5. **Uji PE continuity/fault current**, HLK hipot/leakage, EMC pre-scan, thermal 6 A.
6. **Kunci rating 6 A** di PRD/label; update semua dokumen yang masih menyebut 8 A/16 A.
7. **Verifikasi 2 oz stackup** dan DFM dengan fab.

---

## 9. Status akhir

- PCB digital: `DIGITAL_COMPLETE` untuk DRC 0/0 dan crosscheck BOM/konektivitas.
- PCB fisik: `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`.
- Enclosure: body/lid/bracket **tidak berubah**; relay-shelf/fuse service **REVIEW REQUIRED**.
- Fabrikasi/penggunaan: **`NOT_FOR_FABRICATION` / `NOT_FOR_USE`**.

Tidak ada klaim aman, sertifikasi, atau kesiapan produksi.
