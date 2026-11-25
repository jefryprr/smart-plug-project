# Riset Desain PCB & Review PCB Saat Ini

**Tanggal:** 2026-11-24  
**Revisi:** `REV_D_CORE_ONLY`  
**Scope:** `smartplug.kicad_pcb` (SELV carrier 100 × 70 mm) dan `psu_rev_d.kicad_pcb` (mains-entry PSU 50 × 65 mm)  
**Status:** `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_FABRICATION`

> **Re-analisis 2026-11-25:** lihat `reports/PCB_REANALYSIS_AND_ENCLOSURE_IMPACT_2026-11-25.md` untuk audit ulang PCB dan dampak ke enclosure 3D (BLX-A service access, U9/DevKit, C3/U9, KF129, dll.).

> Dokumen ini adalah review teknik, bukan sertifikasi dan bukan prosedur energisasi mains.
> Tidak ada klaim bahwa PCB ini aman, siap fabrikasi, atau memenuhi IEC/SNI/UL.
> PCB mains hanya boleh di-review dan diuji oleh personel kompeten di lab yang sesuai.

---

## 1. Ringkasan Eksekutif

Topologi keseluruhan sudah masuk akal untuk prototipe: PSU mains dipisah dari carrier SELV, fuse berada sebelum MOV, TCO berada di jalur L setelah MOV, dan relay/PZEM mendapat 5 V langsung dari PSU (bukan dari carrier). Namun ada beberapa hal yang **memblokir fabrikasi**:

1. **Footprint PSU sudah disesuaikan ke part Shopee, tetapi belum semuanya terbukti.** F1 sekarang memakai footprint BLX-A 2-pad (21.5 mm, provisional), MOV memakai D12/7.5 mm untuk 10D271K, TB1/TB2 tetap memakai pad Phoenix 5.08 mm untuk KF129-2P, dan TCO memakai footprint custom 5.1 mm. Body/courtyard/rating KF129, pitch BLX-A, dan dimensi TCO masih `UNVERIFIED`; ukur sample sebelum fabrikasi.
2. **Rating fuse holder 6.3 A membatasi sistem ke 6 A.** BLX-A yang dibeli adalah 6.3 A / 250 V, bukan 10 A. Fuse 10 A di holder 6.3 A tidak boleh dipakai. Fuse diganti ke Littelfuse 215-series 6.3 A, dan target sistem diturunkan ke 6 A (`PROVISIONAL`), bukan 8 A.
3. **Barrier/creepage belum dihitung.** Slot 2 mm berhenti di y=45; lebar slot bukan clearance konduktor. Audit geometri memberikan copper mains-to-SELV minimum ~9.05 mm dan L-N minimum ~1.3 mm (L_LOAD vs cabang AC N), tetapi IEC 60664-1, coating, dan kontinuitas barrier masih `BLOCKED`.
4. **DRC sekarang 0 violations / 0 unconnected**, tetapi `m_MinClearance` board masih 0.0 dan netclass hanya 0.5 mm. DRC 0/0 bukan bukti creepage/keselamatan.
5. **Footprint HLK-5M05 sudah sesuai geometri KiCad resmi.** Pin 33.6/6/18 mm; angka datasheet 35.8/20.5 mm adalah referensi body, bukan center-to-center semua pin. Sample tetap perlu diukur.
6. **Tidak ada schematic level-komponen yang terhubung ke PCB.** Schematic masih block-level; `schematic_parity` kosong. PCB dibuat oleh script, bukan dari netlist schematic. Untuk board mains, ini gap traceability P0.
7. **PE tidak ada di PCB PSU.** PE adalah chassis stud terpisah; harus dipastikan kontinu dari plug → stud → socket, tidak diswitch/dis fuse, dan diuji.
8. **Relay module bukan disconnect yang safety-rated.** Dua channel SPDT independen, bukan DPST mekanis; satu kontak weld bisa meninggalkan konduktor lain. Ini residual risk yang harus ditutup di safety case.
9. **Belum ada filter EMC mains** (X2/Y2/CM choke) dan belum ada pre-scan. HLK adalah switching converter; conducted emission berisiko.
10. **2 oz copper hanya target di dokumen, tidak tercantum di stackup PCB.** Fab harus diminta 2 oz dan stackup harus di-review.

Yang sudah baik:
- Pemisahan fisik PSU mains dan carrier SELV.
- Urutan proteksi L: F1 → MOV → TCO → load/HLK.
- Trace mains 2.5 mm dan target 2 oz; konservatif untuk beban 6 A.
- DRC PSU 0/0 setelah perbaikan layout MOV/F1/TCO; tidak ada unconnected.
- F1, MOV, TCO, dan HLK tidak lagi saling menabrak secara courtyard; HLK digeser 1.5 mm agar clear dari body TB2.
- TCO diletakkan di atas HLK, F1 di kanan atas, MOV di kiri; tidak ada crossing track F.Cu yang tidak disengaja.
- Audit clearance geometric tersedia di `reports/psu_clearance_audit_20261124.json`.
- Carrier: C3 dipindah dekat U9, C4 100 nF gate-source ditambahkan, JP1 memisahkan 5 V PSU/USB, dan TP1/TP2/TP4/TP5 ditambahkan; DRC carrier tetap 0/0.
- Carrier punya GND zone B.Cu, fiducial, mounting hole, dan label blok.
- Relay/PZEM 5 V dari PSU J6/J7; carrier J2/J3 pin 1 NC; tidak ada duplikasi 5 V.
- Dokumen status `NOT_FOR_FABRICATION` dan daftar “not proven” sudah jujur.

---

## 2. Apa Itu PCB yang “Baik, Benar, Efektif, Efisien”?

### 2.1 Benar (correctness)
- Schematic, netlist, PCB, BOM, dan footprint adalah satu sumber kebenaran.
- ERC/DRC berjalan pada aturan yang relevan; bukan hanya “0 violations” dengan aturan yang dilonggarkan.
- Setiap part punya MPN, footprint, pinout, dan rating yang terverifikasi.
- Tidak ada pin NC yang tidak sengaja terhubung; tidak ada net yang salah.

### 2.2 Aman (safety)
- Creepage/clearance dihitung dari tegangan, kategori overvoltage, pollution degree, material group (CTI), dan tingkat isolasi (basic/reinforced).
- Isolasi slot/barrier kontinu; tidak ada jalur creepage yang “memutar” ujung slot.
- PE kontinu, tidak diswitch/dis fuse; titik bonding punya lock washer dan test point.
- Fuse, MOV, TCO, terminal, relay, dan konektor punya rating serta breaking capacity yang sesuai.
- Tidak mengandalkan solder mask, coating, atau 3D print sebagai isolasi tanpa data.
- Jarak komponen ke enclosure/barrier dan jalur kabel diverifikasi, bukan hanya AABB.

### 2.3 Elektrik
- Trace width dihitung dari arus, kenaikan suhu, copper weight, dan panjang.
- Drop tegangan dan loop area power/return dijaga.
- Decoupling ditempatkan dekat pin power IC.
- Impedansi/terminasi hanya relevan untuk sinyal cepat; untuk desain ini, return path dan loop area lebih penting.
- Konektor dan kabel punya rating arus/tegangan serta strain relief.

### 2.4 EMC
- Loop area switching diperkecil; input/output filter ditempatkan dekat konektor.
- Ground plane/return path tidak terpotong; split plane tidak dilintasi sinyal tanpa alasan.
- Filter EMI (X2, Y2, CM choke, ferrite) dipilih dari hasil pre-scan, bukan asal tambah.
- Antenna keepout modul RF dijaga; enclosure dan ground plane tidak merusak antenna.
- ESD protection pada antarmuka yang dapat disentuh.

### 2.5 Termal
- Copper weight, trace width, via, dan airflow cukup untuk losses.
- Komponen panas (HLK, relay, terminal, fuse) tidak menaikkan hotspot di atas rating/TCO holding.
- Thermal test dilakukan di enclosure tertutup, ambient yang disepakati.
- Tidak ada komponen yang bekerja di dekat batas tanpa margin.

### 2.6 DFM (design for manufacturing)
- Min trace/space, annular ring, drill, via aspect ratio, solder mask, dan silkscreen sesuai kemampuan fab.
- Panelization, fiducial, tooling hole, dan breakaway dipilih sesuai jumlah pcs.
- Surface finish dan copper weight cocok dengan pitch/komponen.
- Tidak ada courtyard/ref des yang hilang; tidak ada fitur yang memicu biaya khusus tanpa alasan.

### 2.7 Testability
- Test point untuk rail, ground, UART, relay, dan PE.
- Fiducial untuk assembly; silkscreen ref des untuk debug.
- Programming/service access aman dan diberi label.
- Ada test procedure dan log; tidak mengandalkan “tampak hidup”.

### 2.8 Efisien (cost/efort)
- Layer count dan board size sesuai kebutuhan, bukan berlebihan.
- Part umum, mudah disolder, dan tersedia; tidak memaksa rework.
- Satu kali desain benar lebih murah daripada dua kali fabrikasi + rework.
- Untuk prototipe 5 pcs, 2-layer + THT/SMD campuran masih wajar; 4-layer hanya jika ada alasan EMC/thermal.

---

## 3. Riset: Standar dan Praktik yang Relevan

### 3.1 Standar utama
| Standar | Relevansi untuk proyek ini |
|---|---|
| **IPC-2221 / IPC-2222** | Prinsip umum desain PCB, spacing konduktor, annular ring, solder mask, dan persyaratan fabrikasi. |
| **IPC-2152** | Perhitungan current-carrying capacity trace/via berdasarkan kenaikan suhu dan copper weight. |
| **IPC-9592** | Persyaratan untuk power conversion devices; relevan untuk PSU/HLK, thermal, dan reliability. |
| **IPC-A-600 / IPC-6012** | Kriteria acceptability dan kualifikasi PCB rigid; dipakai saat inspeksi fab. |
| **IEC 60664-1** | Insulation coordination: creepage, clearance, pollution degree, overvoltage category, material group. **Wajib untuk mains.** |
| **IEC 62368-1** | Keselamatan peralatan audio/video/IT; pendekatan hazard-based untuk isolasi dan konstruksi. |
| **CISPR 32 / EN 55032** | Emisi EMC multimedia equipment; relevan untuk pre-scan conducted/radiated. |
| **IEC 61000-4** | Immunity: ESD, EFT, surge, dip, dll. |

### 3.2 Sumber praktik industri
- **Altium — “The Best High Voltage PCB Design Software Package”**: menekankan IPC-2221/IPC-2152, spacing konduktor, trace width, heat removal, dan aturan DRC untuk high voltage. <https://resources.altium.com/p/high-voltage-pcb-design>
- **JLCPCB — Rigid PCB Manufacturing Capabilities**: 2-layer FR4 mendukung 1 oz / 2 oz / 2.5 oz / 3.5 oz / 4.5 oz; controlled impedance untuk 4+ layer; panelization disarankan untuk board kecil. <https://jlcpcb.com/capabilities/pcb-capabilities>
- **PCBWay — PCB Manufacturing Tolerances**: min trace/space 0.1 mm (disarankan ≥0.15 mm), annular ring min 0.15 mm, drill 0.2–6.3 mm, 2 oz tersedia, panelization V-score/tab-route. <https://www.pcbway.com/pcb_prototype/pcb_manufacturing_tolerances.html>
- **TI — “PCB Design Guidelines For Reduced EMI” (SZZA009)**: loop area, ground plane, decoupling, I/O filtering, dan placement. <https://www.ti.com/lit/an/szza009/szza009.pdf>

### 3.3 Angka yang tidak boleh ditebak
- Creepage/clearance untuk 230 VAC **tidak boleh** hanya “6–12 mm provisional”. Harus dihitung dari:
  - tegangan kerja dan kategori overvoltage (rumah: OVC II),
  - pollution degree (biasanya 2 untuk enclosure tertutup, 3 jika kondensasi/kotor),
  - material group/CTI FR4,
  - tingkat isolasi (basic/reinforced),
  - coating/conformal coating atau tidak.
- Untuk 250 VAC, OVC II, pollution degree 2, nilai tipikal basic insulation berada di sekitar **2.5 mm clearance / 3.0 mm creepage** (material group I), dan reinforced kira-kira dua kali lipat. **Angka final harus dihitung engineer dari IEC 60664-1, bukan dari tabel ringkas ini.**
- Slot 2 mm saat ini **di bawah** angka tipikal basic clearance; ini alasan P0, bukan klaim “pasti gagal”.

---

## 4. Data PCB Saat Ini (diukur dari file KiCad)

| Metrik | Carrier SELV | PSU Mains |
|---|---:|---:|
| File | `hardware/kicad/smartplug.kicad_pcb` | `hardware/kicad/psu_rev_d.kicad_pcb` |
| Ukuran | 100.1 × 70.1 mm | 50.1 × 65.1 mm |
| Layer | 2 | 2 |
| Copper | 1 oz (desain) | 2 oz target (tidak tercantum di stackup) |
| Footprint | 29 (22 assembled + 3 fiducial + 4 mounting) | 19 (13 assembled + 3 mounting + 3 fiducial) |
| Track segment | 109 | 37 |
| Via | 15 | 6 |
| Width track | 0.3 mm (59), 0.6 mm (50) | 1.0 mm (18), 1.5 mm (5), 2.5 mm (14) |
| Layer track | F.Cu 97 / B.Cu 12 | F.Cu 34 / B.Cu 3 |
| Copper zone | 1 (GND, B.Cu) | 0 |
| DRC | 0 violations / 0 unconnected @ 0.15 mm | 0 violations / 0 unconnected @ 0.5 mm |
| Board min clearance | 0.0 mm | 0.0 mm |
| Track min width | 0.2 mm | 0.2 mm |
| Copper-edge clearance | 0.5 mm | 0.5 mm |
| Schematic parity | block-level schematic; no component netlist parity | `schematic_parity: []` |

**Penting:** `m_MinClearance = 0.0` di kedua board. DRC hanya memakai netclass; carrier 0.15 mm, PSU 0.5 mm. Tidak ada netclass “Mains” dengan clearance 3/6 mm. DRC 0/0 **bukan** bukti creepage/clearance.

---

## 5. Temuan Mendalam

### 5.1 P0 — Safety / correctness / blocking

#### F-01. Footprint terminal block: Phoenix-specific, belum terbukti untuk KF129
- **PCB:** TB1/TB2 memakai `TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` (Phoenix MKDS 1.5/2-5.08, 17.5 A / 250 V).
- **BOM/kartu belanja:** KF129-2P, 5.08 mm, 300 V / 25 A.
- **Dampak:** Pad Phoenix 5.08 mm / drill 1.3 mm / pad 2.6 mm **mungkin** kompatibel dengan KF129, tetapi body, courtyard, retensi, dan rating 25 A belum terbukti. Phoenix MKDS sendiri hanya 250 V, di bawah target ≥300 V.
- **Aksi:** Verifikasi KF129 fisik terhadap footprint; jika body/courtyard tidak cocok, buat footprint KF129 khusus. Jangan mengklaim rating 300 V sampai part/footprint direview.
- **Status:** `UNVERIFIED`; `BLOCKED` untuk klaim rating 300 V.

#### F-02. Footprint MOV sudah diganti ke D12/7.5 mm, tetapi sample belum diukur
- **PCB:** `RV_Disc_D12mm_W5mm_P7.5mm` (disc 12 mm, pitch 7.5 mm), pad 1.8 mm, drill 0.8 mm.
- **Part:** 10D271K, disc 10 mm; pitch perlu dicek (sering 7.5 mm).
- **Dampak:** Footprint D12 lebih besar dari disc 10 mm; secara mekanis longgar, tetapi lead pitch/body harus cocok. Lead stress atau solder bridge mungkin terjadi.
- **Aksi:** Ukur MOV fisik (diameter, pitch, lead diameter); ganti ke footprint D10 jika tersedia/terukur. Jangan menganggap D12 sebagai bukti fit.
- **Status:** `UNVERIFIED`.

#### F-03. Fuse holder BLX-A: rating 6.3 A, footprint 21.5 mm provisional
- **PCB:** custom `Fuseholder_BLX-A_5x20mm` (2 pad, pitch 21.5 mm, pad 2.6 mm, drill 1.6 mm, body 22 × 9.5 mm).
- **Part:** BLX-A PCB fuse holder, 5 × 20 mm, **6.3 A / 250 V**, 1 holder per fuse.
- **Temuan:** Holder yang dibeli **bukan** 10 A. Rating 6.3 A membatasi arus kontinu sistem; fuse 10 A di holder ini tidak acceptable. Fuse sudah diganti ke Littelfuse 215-series 6.3 A dan target sistem diturunkan ke 6 A.
- **Footprint:** Seller menyebut jarak kaki 21.5 mm; datasheet Tayda hanya memberi body 22 × 9.5 × 10.5 mm dan pin 1.4 × 0.35 mm. Pitch 21.5 mm **belum** diverifikasi pada sample.
- **Aksi:** Ukur sample; jika pitch berbeda, buat footprint baru. Verifikasi retensi fuse, rating, dan akses servis.
- **Status:** `PROVISIONAL` untuk rating 6.3 A; `UNVERIFIED` untuk pitch/body.

#### F-04. TCO generic: footprint 5.1 mm provisional, marking belum diverifikasi
- **PCB:** custom TF1, pad 1.3 mm, drill 0.7 mm, pitch 5.1 mm, body outline 10 × 5 mm.
- **Part:** generic 96 °C 10 A (bukan SF96E).
- **Dampak:** Body/lead spacing bisa berbeda; TCO safety-critical dan harus diklem ke hotspot. Footprint custom belum diukur.
- **Aksi:** Ukur TCO fisik; verifikasi marking 96 °C/RFT 99 °C, holding 84 °C, dimensi, dan clamping termal. Jangan mengklaim SF96E.
- **Status:** `UNVERIFIED`; `BLOCKED` untuk klaim TCO generik.

#### F-05. Footprint HLK-5M05: cocok dengan footprint resmi KiCad
- **Datasheet:** 35.8 mm dan 20.5 mm adalah dimensi referensi body/pin row, bukan jarak center-to-center semua pin.
- **Footprint:** pin (45.8,17), (45.8,23), (12.2,11), (12.2,29) → x span 33.6 mm; y span 6 mm dan 18 mm.
- **Verifikasi:** footprint resmi KiCad `Converter_ACDC_Hi-Link_HLK-5Mxx` memakai pad (0,0), (0,6), (33.6,-6), (33.6,12) — geometri yang sama. Custom footprint tidak salah.
- **Aksi:** Ukur sample HLK untuk memastikan batch; tidak perlu ubah footprint.
- **Status:** `VERIFIED` untuk geometri; sample tetap `UNVERIFIED`.

#### F-06. Barrier/creepage path belum dihitung (bukan sekadar lebar slot)
- **Layout:** slot x=19..21, y=0..45 (2 mm), terbuka di tepi bawah, berhenti di y=45; HLK body 38 × 23 mm membentang di atas slot.
- **Koreksi:** lebar slot bukan sama dengan clearance konduktor. Audit geometri `scripts/psu_clearance_audit.py` memberi copper mains-to-SELV minimum **9.05 mm** (N bus ke pad GND HLK) dan L-N minimum **1.3 mm** (L_LOAD vs cabang AC N); branch MOV ~1.65 mm. Angka ini bukan creepage IEC.
- **Dampak:** barrier tidak kontinu sampai tepi atas; creepage bisa memutar ujung slot; pad terminal 5.08 mm (pad 2.6 mm) menyisakan gap ~2.48 mm.
- **Aksi:** Hitung IEC 60664-1; putuskan basic/reinforced; perlebar slot hanya jika hasil perhitungan menuntut; buat keepout/barrier kontinu; tentukan coating; review 3D clearance ke enclosure.
- **Status:** `BLOCKED`; hasil audit geometri hanya `UNVERIFIED`.

#### F-07. DRC 0/0 tercapai, tetapi tidak menegakkan creepage mains
- **Bukti:** DRC terakhir **0 violations / 0 unconnected**; namun `m_MinClearance = 0.0`, PSU netclass 0.5 mm, dan tidak ada netclass/keepout mains. Audit clearance geometric terpisah memberi 9.05 mm mains-to-SELV dan 1.3 mm L-N.
- **Dampak:** Kesalahan spacing 1–2 mm masih bisa lolos DRC; 0/0 bukan bukti keselamatan.
- **Aksi:** Buat netclass `MAINS` (L_IN/N_MAINS/L_FUSED/L_LOAD) dengan clearance/creepage sesuai perhitungan IEC; netclass `SELV` 0.2–0.5 mm; tambah keepout/rule area; jalankan DRC dengan aturan tersebut.
- **Status:** `BLOCKED` untuk klaim keselamatan; DRC 0/0 hanya `DIGITAL_COMPLETE` untuk aturan 0.5 mm.

#### F-08. Tidak ada schematic level-komponen / netlist parity
- **Bukti:** `smartplug.kicad_sch` adalah block schematic; PSU DRC `schematic_parity: []`; PCB dibuat oleh `generate_*_pcb.py`, bukan dari netlist schematic.
- **Dampak:** Tidak ada ERC yang memverifikasi pin/net; kesalahan net bisa lolos ke PCB. Untuk board mains, traceability tidak cukup.
- **Aksi:** Buat schematic symbol-level (carrier + PSU), hubungkan ke PCB, jalankan ERC + DRC + netlist parity; review sebelum fab.
- **Status:** `ENGINEERING_REVIEW_REQUIRED`.

#### F-09. PE tidak ada di PCB PSU
- **Bukti:** TB1/TB2 hanya N/L; PE adalah chassis stud; tidak ada PE net di PSU.
- **Dampak:** PE path harus kontinu dan tidak boleh diswitch/dis fuse; jika wiring salah, enclosure/socket PE bisa tidak terhubung.
- **Aksi:** Buat wiring diagram PE plug → stud → socket; stud dengan lock washer/nut; test point PE; continuity/fault-current test.
- **Status:** `BLOCKED` sampai wiring/PE review.

#### F-10. Relay module bukan disconnect safety-rated
- **Bukti:** Modul 2-channel optocoupler, dua SPDT independen; J3 IN1/IN2 di-tie; BOM mencatat “bukan DPST mekanis”.
- **Dampak:** Satu kontak weld dapat meninggalkan konduktor lain; tidak bisa diklaim sebagai double-pole disconnect.
- **Aksi:** Safety case harus menganggap relay sebagai functional switch, bukan isolasi; pertimbangkan contactor 2-pole mekanis atau relay safety-rated; tambah physical disconnect/fuse coordination.
- **Status:** `ENGINEERING_REVIEW_REQUIRED`.

#### F-11. HLK isolation/certificate/hipot belum terbukti
- **Bukti:** HLK batch certificate, isolation, ripple, thermal belum diukur; datasheet claim 2500 VAC.
- **Dampak:** Barrier utama mains–SELV adalah HLK; tanpa hipot/leakage, klaim isolasi tidak sah.
- **Aksi:** Hipot/leakage test pada sample/batch; verifikasi certificate; jangan mengandalkan slot PCB sebagai barrier utama.
- **Status:** `HARDWARE_VALIDATION_REQUIRED`.

#### F-12. 2 oz copper tidak tercantum di stackup
- **Bukti:** File PCB hanya `(thickness 1.6)`; tidak ada stackup/copper weight; README menyebut “2 oz target”.
- **Dampak:** Fab bisa memakai 1 oz; rating arus/thermal berubah.
- **Aksi:** Tulis stackup 2 oz di fab notes dan file PCB; verifikasi kemampuan fab; ukur copper thickness/test coupon.
- **Status:** `UNVERIFIED`.

### 5.2 P1 — Functional / EMC / thermal / testability

| ID | Temuan | Bukti | Aksi |
|---|---|---|---|
| F-13 | Decoupling U9 jauh | C3 100 nF dipindah dari (58,48) ke (80,31), ~3.2 mm dari U9 pin 14 | Selesai secara layout; verifikasi jarak/loop saat review. |
| F-14 | Trace gate relay panjang | GPIO4 → R1 ≈ 68 mm, 0.3 mm; C4 100 nF ditambahkan di RELAY_GATE–GND | Filter terpasang; trace panjang masih ada. Pertimbangkan pindahkan driver di rev berikutnya. |
| F-15 | Backfeed USB → 5 V PSU | JP1 solder jumper memisahkan J8 +5V_IN dari +5V; buka saat service USB | Selesai secara layout; beri label “OPEN FOR USB SERVICE”. |
| F-16 | J2/J3 4-pin dengan pin 1 NC | Pin 1 NC; kabel 4-pin standar bisa salah pasang | Gunakan kabel 3-pin/lepaskan wire pin 1; rev berikutnya ganti ke 3-pin keyed. |
| F-17 | Test point kurang | TP1 +5V, TP2 GND, TP4 RELAY_GATE, TP5 BUTTON ditambahkan | +3V3, PZEM TX/RX, PE masih belum ada; tambah di rev berikutnya. |
| F-18 | Tidak ada reverse-polarity protection J8 | J8 2-pin +5 V/GND | Tambah P-MOSFET ideal diode atau keyed connector; label polaritas. |
| F-19 | PSU 5 V bus panjang/loop besar | 5 V x=2, GND x=9.2, panjang ~43 mm; tidak ada local decoupling di J5/J6/J7 | Tambah 100 nF/10 µF di tiap output; pertimbangkan ferrite/pi filter. |
| F-20 | PTC 1.0 A vs HLK 1 A dan peak load | Total 5 V estimate ≤1 A; peak belum diukur; PTC aktual 1.0 A | Ukur peak Wi-Fi+relay; derating PTC/HLK; pertimbangkan HLK 2 A. |
| F-21 | Tidak ada filter EMC mains | Tidak ada X2/Y2/CM choke; HLK switching | Pre-scan CISPR 32/EN 55032; tambah filter sesuai hasil. |
| F-22 | Thermal HLK 2.1 W di enclosure tertutup | Efficiency ~70%; 5 W; 2.1 W heat | Thermal test 6 A/ambient; copper/thermal pad/vent; cek TCO <84 °C. |
| F-23 | Tidak ada copper zone PSU | 0 zones; return path hanya track | Pertimbangkan GND pour SELV dengan keepout mains; jangan kurangi creepage. |
| F-24 | Antenna keepout/RF belum diverifikasi | DevKit antenna dekat dinding/ground plane | Jaga keepout antenna; uji Wi-Fi range di enclosure. |
| F-25 | Reference designator disembunyikan | `Reference().SetVisible(False)` di generator | Tambah ref des atau assembly map; untuk prototipe manual. |
| F-26 | Tidak ada ESD protection button/connector | Button/tombol exposed; JST internal | Tambah RC/TVS pada button; ESD pada service interface. |
| F-27 | Tidak ada bleeder 5 V | C1/C2 bisa menyimpan muatan | Tambah 1–2.2 kΩ bleeder jika diperlukan; cek discharge time. |
| F-28 | Terminal block pad gap ~2.48 mm | Pitch 5.08 mm, pad 2.6 mm; KF129 body unverified | Review creepage pad; terminal body; target ≥300 V. |
| F-29 | L/N/PE label kurang | N/L dan rating fuse sudah ditambahkan; PE masih off-board | Tambah label PE stud/wiring; warning; J2/J3 pin 1 NC. |
| F-30 | PSU mounting holes/standoff | H1/H3/H4; bracket 3D print | Pastikan standoff isolatif/nylon; cek clearance ke mains. |
| F-39 | BLX-A holder 6.3 A vs target 8 A | Holder rating 6.3 A; fuse 10 A tidak boleh dipakai | Turunkan rating sistem ke 6 A; ganti fuse ke 6.3 A; dokumentasikan di label/PRD. |
| F-40 | HLK body vs TB2 clearance | Body 10.0 vs TB2 body 8.6 → 1.4 mm; courtyard 9.75 vs 9.1 → 0.65 mm | Verifikasi 3D; jangan menggeser HLK tanpa cek F1/TCO. |
| F-41 | TCO/F1 pad gap | F1 pad2 41.5, TCO pad1 39.0; pad radii 1.3 + 0.65 = 1.95, gap 0.55 mm | Diperbaiki: TCO digeser ke (43.5, 36.5); gap 0.55 mm. Masih same-net, tetapi tidak lagi rawan bridge. |

### 5.3 P2 — DFM / cost / documentation

| ID | Temuan | Aksi |
|---|---|---|
| F-31 | Docstring PSU 50×70 vs actual 50×65 | Perbaiki dokumen/generator. |
| F-32 | DRC mengabaikan courtyard/via-center/footprint filters | Perbaiki footprint; jangan abaikan untuk build produksi. |
| F-33 | Panelization belum didefinisikan | Panel 5 pcs dengan tab-route/V-score, fiducial per panel. |
| F-34 | Surface finish belum dipilih | HASL lead-free cukup untuk THT/0805; ENIG jika fine pitch/aging. |
| F-35 | Via tenting/annular ring belum dispesifikkan | Tentukan tented/non-tented; annular ring ≥0.15 mm. |
| F-36 | Copper balance PSU | 2 oz + 2.5 mm traces; pertimbangkan copper balance/hatch pour. |
| F-37 | 2-layer vs 4-layer | 2-layer cukup untuk carrier low-speed; 4-layer hanya jika EMC/return path menuntut. |
| F-38 | Test coupon/stackup | Sertakan coupon untuk 2 oz/annular ring/thermal. |

---

## 6. Matriks Cross-Check Footprint ↔ Part

| Ref | Footprint PCB | Part di BOM/kartu belanja | Status |
|---|---|---|---|
| TB1/TB2 | Phoenix MKDS 1.5/2-5.08 pad (5.08 mm, 1.3 mm drill, 2.6 mm pad) | KF129-2P (300 V/25 A claim) | **Pad-compatible only** — body/rating/retention `UNVERIFIED` |
| F1 | Custom BLX-A 2-pad, 21.5 mm, pad 2.6, drill 1.6 | BLX-A 5×20, 6.3 A/250 V | **Provisional** — pitch/body sample `UNVERIFIED`; rating limits system to 6 A |
| MOV1 | RV disc D12, pitch 7.5 mm | 10D271K 10 mm | **Provisional** — disc/pitch sample `UNVERIFIED` |
| TF1 | Custom TCO, 5.1 mm pitch, body 10×5 | Generic 96 °C, not SF96E | **UNVERIFIED/BLOCKED** for generic marking |
| PS1 | Custom HLK, 33.6/6/18 mm | HLK-5M05 | OK (sesuai KiCad official); sample verify |
| J5/J6/J7 | JST-XH B2B 2-pin | JST-XH 2-pin cable | OK (verifikasi) |
| C1 | CP radial 6.3×5.4 | 100 µF 10 V | OK (verifikasi) |
| C2 | 0805 | 100 nF 0805 | OK |
| F2 | 1206 | PTC 1.0 A 1206 | OK (rating; verify hold/trip) |
| D1 | SMB | SMBJ5.0A 600 W | OK (verify marking) |
| Carrier J2/J3 | JST-XH B4B 4-pin | JST-XH 4-pin cable | OK; pin 1 NC |
| Carrier J6/J8 | JST-XH B2B 2-pin | JST-XH 2-pin cable | OK |
| U9 | DIP-14 7.62 mm | 74HCT125D SOP-14 + adapter | OK via adapter; cek tinggi |
| Q1 | SOT-23 | AO3400A | OK |
| R/C | 0805 | 0805 | OK |
| ESP32 | 2× 1×22 socket, 22.86 mm | ESP32-S3-DevKit C N16R8 | **Cek** pinout/row/antena |

---

## 7. Creepage/Clearance: Angka yang Harus Dihitung

Yang perlu dihitung engineer:
1. Tegangan kerja: 230 VAC nominal; surge/OVC II.
2. Pollution degree: 2 (enclosure tertutup) atau 3 (condensation/contamination).
3. Material group FR4/CTI: material group I/II/III.
4. Isolasi: basic vs reinforced; functional vs safety.
5. Coating: solder mask vs conformal coating; coating tidak otomatis menaikkan isolasi.
6. Slot/barrier: 2 mm sekarang; target awal minimal **3 mm basic / 6 mm reinforced** (angka final dari standar).
7. Terminal block: pad gap ~2.48 mm; body terminal memberi creepage tambahan; verifikasi.
8. HLK: AC–DC pin/body; module internal isolation; board slot.
9. PE: creepage ke PE stud/komponen SELV; PE tidak boleh dekat mains tanpa jarak.
10. Enclosure: jarak PCB ke dinding/barrier; 3D print tolerance; kabel.

**Jangan** menulis “creepage 6–12 mm” sebagai klaim tanpa perhitungan. Saat ini statusnya `UNVERIFIED`.

---

## 8. EMC & Thermal: Prioritas

### EMC
- HLK-5M05 adalah switching converter; input/output loop harus kecil.
- Tidak ada X2/Y2/CM choke; conducted emission belum diketahui.
- PSU 5 V bus panjang; tambah local decoupling/ferrite.
- Carrier low-speed; trace gate relay panjang; tambah filter/ESD.
- Antenna ESP32: jaga keepout; uji range di enclosure.
- Lakukan pre-scan CISPR 32/EN 55032 sebelum klaim EMC.

### Thermal
- HLK ~2.1 W; terminal/fuse/TCO/relay juga panas.
- 2.5 mm/2 oz trace pada 6 A masih konservatif menurut IPC-2152.
- TCO holding 84 °C; hotspot harus <84 °C dengan margin.
- Thermal test di enclosure tertutup, ambient 40 °C (atau disepakati), load 6 A.
- Jika hotspot >84 °C, relokasi TCO/derate/vent.

---

## 9. Rencana Aksi Berprioritas

### P0 — sebelum fabrikasi
1. **Footprint audit**: TB1/TB2 (KF129 body), F1 (BLX-A 21.5 mm sample), MOV1 (10D271K), TF1 (generic TCO); PS1 sample verify; regenerate; DRC.
2. **Putuskan terminal block**: KF129 + verifikasi body, atau Phoenix MKDS + rating 250 V.
3. **Hitung creepage/clearance IEC 60664-1**; perlebar/continuous slot; tentukan coating; update netclass/keepout.
4. **Buat schematic level-komponen** + netlist parity + ERC; review.
5. **PE path**: wiring diagram, stud, lock washer, test point; continuity/fault-current plan.
6. **Relay safety case**: anggap functional switch; contactor/2-pole atau physical disconnect; weld risk.
7. **HLK hipot/leakage/certificate**; MOV/fuse/TCO coordination/surge study.
8. **2 oz stackup** di file/fab notes; verifikasi fab.
9. **Tetapkan rating 6 A** di PRD/label; update semua dokumen yang masih menyebut 8 A/16 A.

### P1 — sebelum prototipe dinyalakan
10. Decoupling U9/J2/J3; gate filter; test points; backfeed protection; reverse polarity.
11. EMC filter/pre-scan; thermal test 6 A; PTC/HLK peak measurement.
12. Label L/N/PE, fuse 6.3 A, 5 V outputs, J2/J3 pin1 NC; ref des/assembly map.
13. Antenna keepout/RF test; ESD button/interface.

### P2 — sebelum produksi
13. Panelization, surface finish, annular ring, via tenting, copper balance.
14. 2-layer vs 4-layer evaluation; test coupon; DFM review dengan fab.
15. Dokumentasi: docstring 50×65, stackup, test procedure, incoming inspection.

---

## 10. Checklist Review/Fabrikasi

- [ ] Schematic level-komponen ↔ PCB netlist parity; ERC 0; DRC 0 dengan aturan mains.
- [ ] Footprint audit semua part safety-critical (TB, fuse, MOV, TCO, HLK, relay, socket).
- [ ] Creepage/clearance calculation signed; slot/barrier continuous; coating decision.
- [ ] PE continuity/fault-current plan; stud torque/lock washer/test point.
- [ ] Fuse/MOV/TCO coordination and breaking capacity; surge study.
- [ ] HLK hipot/leakage/certificate; PZEM internal isolation; relay module isolation.
- [ ] 2 oz stackup; annular ring; min trace/space; panelization; fiducials.
- [ ] Thermal test 6 A/40 °C; TCO <84 °C; HLK/terminal/relay hotspots.
- [ ] EMC pre-scan CISPR 32/EN 55032; filter if needed.
- [ ] Test points: +5 V, +3V3, GND, PZEM TX/RX, relay gate, button, PE.
- [ ] Labels: L/N/PE, fuse rating, warnings, J2/J3 pin1 NC, 5 V source.
- [ ] Incoming inspection: measure samples; update BOM/footprints; log.

---

## 11. Referensi

1. IPC-2221B, *Generic Standard on Printed Board Design*; IPC-2222A, *Sectional Design Standard for Rigid Organic Printed Boards*.
2. IPC-2152, *Standard for Determining Current-Carrying Capacity in Printed Board Design*.
3. IPC-9592B, *Requirements for Power Conversion Devices for the Computer and Telecommunications Industries*.
4. IPC-A-600J, *Acceptability of Printed Boards*; IPC-6012E, *Qualification and Performance Specification for Rigid Printed Boards*.
5. IEC 60664-1:2020, *Insulation coordination for equipment within low-voltage supply systems — Part 1: Principles, requirements and tests*.
6. IEC 62368-1:2018, *Audio/video, information and communication technology equipment — Part 1: Safety requirements*.
7. CISPR 32:2015+AMD1:2019, *Electromagnetic compatibility of multimedia equipment — Emission requirements*.
8. IEC 61000-4 series, *Electromagnetic compatibility (EMC) — Testing and measurement techniques*.
9. Altium, “The Best High Voltage PCB Design Software Package”, <https://resources.altium.com/p/high-voltage-pcb-design>.
10. JLCPCB, “Rigid PCB Manufacturing Capabilities”, <https://jlcpcb.com/capabilities/pcb-capabilities>.
11. PCBWay, “PCB Manufacturing Tolerances”, <https://www.pcbway.com/pcb_prototype/pcb_manufacturing_tolerances.html>.
12. Texas Instruments, “PCB Design Guidelines For Reduced EMI” (SZZA009), <https://www.ti.com/lit/an/szza009/szza009.pdf>.

---

## 12. Perbaikan yang sudah diimplementasikan (2026-11-24)

### PSU

- F1 diganti ke footprint **BLX-A 2-pad, 21.5 mm** (provisional), pad 2.6 mm, drill 1.6 mm, body 22 × 9.5 mm.
- Fuse diganti ke **Littelfuse 215-series 6.3 A / 250 V**; holder BLX-A 6.3 A; target sistem diturunkan ke **6 A provisional**.
- TB1/TB2 memakai **KF129-2P** (pad Phoenix 5.08 mm; body/rating `UNVERIFIED`).
- MOV1 memakai **10D271K** dengan footprint **D12/7.5 mm** (provisional).
- TF1 memakai **generic 96 °C** dengan footprint custom **5.1 mm / body 10 × 5 mm** (provisional).
- Layout diubah: N bus x=23.5, MOV x=27, F1 x=43.5, TCO x=43.5, HLK digeser 1.5 mm ke atas; tidak ada crossing F.Cu yang tidak disengaja. TCO/F1 pad gap sekarang 0.55 mm.
- Ditambahkan courtyard untuk HLK dan TCO; DRC **0 violations / 0 unconnected**.
- Label N/L, rating fuse 6.3 A, dan “6 A MAX” ditambahkan.
- Audit clearance geometric: mains-to-SELV **9.05 mm**, L-N **1.3 mm** (bukan klaim IEC).
- Gerber/drill/POS provisional diekspor ulang.

### Carrier

- C3 dipindah ke (78,24), dekat U9 pin 14.
- C4 100 nF ditambahkan antara RELAY_GATE dan GND.
- JP1 solder jumper memisahkan J8 `+5V_IN` dari `+5V` (buka saat service USB).
- TP1 +5V, TP2 GND, TP4 RELAY_GATE, TP5 BUTTON ditambahkan.
- DRC carrier **0 violations / 0 unconnected**; PCBA BOM 17 baris (TP/JP dikecualikan sebagai fitur PCB).

### BOM / dokumentasi

- `bom/CORE_ONLY_SHOPEE_SHOPPING_LIST.csv`: fuse 6.3 A, holder BLX-A, catatan rating 6 A.
- `bom/BOM_MASTER.yaml` / `BOM_PROCUREMENT.csv` / `COMPONENT_APPROVALS.yaml`: diselaraskan ke part Shopee (ESP32, HLK, relay, 74HCT125D + adapter, fuse, holder, MOV, TCO, PTC, TVS, TB, JST, socket, plug).
- `safety/ELECTRICAL_RATING_CHAIN.md`, `PROTECTION_COORDINATION.md`, `THERMAL_CALCULATION.md`, `THERMAL_RISK_AND_DERATING.md`, `FMEA`, `RESIDUAL_RISK_REGISTER.csv`: rating 8 A → **6 A provisional**, fuse/holder 6.3 A.
- `hardware/psu/README.md` dan schematic PSU: rating/part diperbarui.
- `PRD.md`, `README.md`, `README.id.md`, `ROADMAP.md`, `CHANGELOG.md`: catatan 6 A provisional.

### Verifikasi digital yang lulus

- PSU DRC **0/0** (`reports/kicad/psu_drc.json`, exit 0).
- Carrier DRC **0/0** (`reports/kicad/drc.json`, exit 0).
- `validate_psu.py` **PASS**.
- `validate_connectivity.py` **PASS**.
- `generate_bom.py` **PASS** (59 master rows, 49 procurement lines).

### Masih terbuka (tidak boleh diklaim selesai)

- IEC 60664-1 creepage/clearance, barrier continuity, coating.
- KF129 body/rating, BLX-A pitch, 10D271K disc/pitch, TCO marking/dimensions.
- PE path, relay safety case, HLK hipot/isolation, EMC pre-scan, thermal 6 A.
- Schematic level-komponen + netlist parity/ERC.
- 2 oz stackup, fab DFM review.
- Semua uji fisik mains.

---

**Status akhir:** `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_FABRICATION`.  
Tidak ada klaim keselamatan, sertifikasi, atau kesiapan produksi.
