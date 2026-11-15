# Procurement Indonesia — Prototype Smart Plug 8 A (REV_B)

**Tanggal riset:** 15–16 November 2026  
**Mata uang:** IDR  
**Status:** `PROCUREMENT_RESEARCH` / `NOT_APPROVED` / `NOT_FOR_FABRICATION`  
**Daftar belanja:** `bom/BOM_PROCUREMENT.csv` dan `bom/BOM_PROCUREMENT.md`

---

## 1. Ringkasan eksekutif

REV_B menghapus **GY-TMP102** dan **ADuM1201 + B0505S**. Isolasi galvanik PZEM-004T V4 sekarang menjadi satu-satunya barrier komunikasi; carrier hanya melakukan level shifting 5 V ↔ 3,3 V.

| Konfigurasi | Subtotal | + ongkir estimasi Rp40.000 | Status |
|---|---:|---:|---|
| Elektronik inti (tanpa enclosure/konektor/kabel) | **Rp433.633** | — | di dalam budget |
| **CORE** (safety/function minimum, 47 baris) | **Rp698.297** | **Rp738.297** | **di bawah Rp750.000** |
| **CORE dengan restock EasyWare** | **Rp646.829** | **Rp686.829** | margin lebih besar |
| **FULL** (+ OLED/RTC/RGB/konektor) | **Rp815.897** | **Rp855.897** | di atas budget |

**Kesimpulan:** CORE sekarang **masuk budget** bahkan pada harga marketplace, selama ongkir tetap sekitar Rp40.000. FULL masih di atas Rp750.000; tunda OLED/RTC/RGB atau naikkan budget. Jangan menurunkan fuse, MOV, TCO, PE, terminal, enclosure, atau rating relay untuk mengejar FULL.

---

## 2. Metode

Harga diambil 15–16 November 2026 dari halaman toko atau listing marketplace. Tidak ada harga rekaan.

| Status | Arti |
|---|---|
| `VERIFIED_STORE_PAGE` | Harga/produk dibaca langsung dari halaman toko. |
| `VERIFIED_AGGREGATOR` | Harga/judul dari listing Shopee/Tokopedia via BigGo. |
| `ESTIMATED` | Tidak ada listing exact; estimasi dari komponen sejenis. |

Tidak termasuk: ongkir aktual, pajak, bea impor, alat ukur/solder/crimp, jasa 3D print, biaya lab, dan biaya fabrikasi PCB aktual.

---

## 3. Keputusan komponen inti

### 3.1 MCU — ESP32-S3 N16R8

| Kandidat | Harga | Stok | Catatan |
|---|---:|---|---|
| EasyWare N16R8 DevKitC-1 | Rp103.500 | habis | Harga terbaik jika restock. |
| Shopee N16R8 compatible (ALFA) | Rp139.968 | listed | Dipakai di CORE; **bukan** board resmi. |
| Official Espressif | belum ada stok lokal | — | Biaya impor tinggi. |

**Keputusan:** board compatible Rp139.968 dengan deviasi Q08=B tercatat. Verifikasi marking N16R8, GPIO RGB (v1.0=48, v1.1=38), regulator, USB, dan pinout two 1x22 headers.

### 3.2 Metering — PZEM-004T V4 100 A CT

| Varian | Harga | Stok | Catatan |
|---|---:|---|---|
| EasyWare 100 A close CT | Rp135.000 | habis | Restock price. |
| Shopee 100 A closed CT (ALFA) | Rp150.000 | listed | Dipakai di CORE. |
| Shopee 100 A split CT | Rp250.000+ | listed | Lebih mahal; tidak perlu. |
| PZEM 10 A | Rp112.500 | habis | **Ditolak** untuk 8 A kontinu. |

**Keputusan:** PZEM V4 100 A CT. **Tidak ada ADuM1201/B0505S eksternal.** Sisi TTL PZEM sudah SELV melalui optocoupler internal; tetap wajib review creepage dan hipot assembly. Jangan hubungkan USB saat mains aktif.

### 3.3 PSU — Hi-Link HLK-5M05

| Sumber | Harga | Stok | Catatan |
|---|---:|---|---|
| Shopee Marnov | Rp49.000 | listed | Dipakai di CORE. |
| CNC Store Bandung | Rp63.300 | habis | Referensi lokal. |

**Keputusan:** HLK-5M05 Rp49.000. Tetap `PENDING_APPROVAL`: efisiensi ~70%, panas ~2.1 W, batch/isolasi/creepage belum terbukti.

### 3.4 Relay — modul 2 channel 5 V optocoupler

| Sumber | Harga | Catatan |
|---|---:|---|
| Shopee AIFRobotic | Rp16.650 | Dipakai di CORE. |
| Shopee lain | Rp12.000–Rp34.848 | Kualitas bervariasi. |

**Keputusan:** modul 2 channel, dua SPDT independen, **bukan DPST**. Klaim 10 A adalah klaim vendor; final 8 A setelah uji thermal/lifecycle. IN1/IN2 diikat dan dikendalikan satu AO3400.

### 3.5 Level shifting PZEM + RGB — 74HCT125

| Part | Harga | Catatan |
|---|---:|---|
| SN74HCT125N DIP-14 | Rp8.750 | Dipakai di CORE. |

- PZEM TX (5 V) → **R4 10k / R5 20k divider** → ESP32 GPIO18 (3,3 V).
- ESP32 GPIO17 (3,3 V) → **74HCT125** (5 V) → PZEM RX.
- ESP32 GPIO10 (3,3 V) → **74HCT125** → 330R → WS2812 data.
- 74HCT125 VCC = 5 V, 100 nF decoupling. Tidak ada isolasi eksternal.

### 3.6 Proteksi mains

| Part | Harga | Catatan |
|---|---:|---|
| Littelfuse 5x20 10 A 250 VAC slow-blow | Rp18.300 | Verifikasi MPN/marking. |
| Fuse holder panel 5x20 | Rp5.500 | Tool-access, di dalam enclosure. |
| MOV 10D271K 275 VAC | Rp7.500 | Generic; EPCOS S10K275 lebih baik. |
| Thermal fuse 99 °C 10 A | Rp4.995 | Generic; Sefuse SF169E batch datasheet belum ada. |

**Tidak ada sensor suhu firmware.** Proteksi termal sekarang **hanya** fuse + TCO one-shot + desain termal enclosure. Ini peningkatan residual risk yang harus diuji.

### 3.7 Konektor, socket, enclosure

| Part | Harga | Catatan |
|---|---:|---|
| 2x22 female header strip (split into two 1x22 rows) | Rp3.250 | DevKitC-1 memakai dua header 1x22 dengan jarak baris 22,86 mm. |
| JST-XH 4-pin (PZEM/relay/OLED) | Rp12.300 | Empat kabel. |
| JST-XH 6-pin (RTC) | Rp8.000 est. | 32K boleh NC. |
| JST-XH 2-pin (button/5V) | Rp5.000 est. | Bisa solder langsung. |
| 5.08 mm terminal 2-pin/5-pin | Rp2.450 / Rp11.760 | Generic 5EDR. |
| PE terminal 6 mm² | Rp10.250 | PE kontinu, tidak diswitch. |
| Simon Schuko 16 A | Rp25.026 | Sertifikasi/PE belum. |
| BOSS BP16 plug | Rp14.044 | Cable clamp/PE belum. |
| M16 gland IP68 | Rp2.400 | Strain relief. |
| MG Duradus 220×120×70 ABS IP65 | Rp99.684 | Flame rating belum. |

---

## 4. Rincian budget CORE

| Kelompok | Subtotal |
|---|---:|
| Metering (PZEM) | Rp150.000 |
| MCU (ESP32) | Rp139.968 |
| Mechanical (enclosure, bracket, PE, fastener) | Rp131.884 |
| Connectors (terminal, socket, plug, gland, header, JST) | Rp106.280 |
| Power (HLK-5M05) | Rp49.000 |
| Protection (fuse, holder, MOV, TCO) | Rp36.295 |
| Cable (mains + hookup) | Rp19.500 |
| Switching (relay + MOSFET) | Rp18.150 |
| PCB carrier 100×70 (5 pcs share) | Rp15.000 |
| Passives (R/C) | Rp9.470 |
| UI/level shift (74HCT125) | Rp8.750 |
| UI (button) | Rp7.000 |
| Consumables (heatshrink) | Rp5.000 |
| Labels | Rp2.000 |
| **CORE total** | **Rp698.297** |

Top CORE cost drivers:

1. PZEM 100 A — Rp150.000
2. ESP32-S3 N16R8 — Rp139.968
3. Enclosure 220×120×70 — Rp99.684
4. HLK-5M05 — Rp49.000
5. Simon socket — Rp25.026
6. Littelfuse fuse — Rp18.300
7. Relay module — Rp16.650
8. PCB carrier — Rp15.000
9. NYYHY cable — Rp14.500
10. BOSS plug — Rp14.044

---

## 5. Rincian FULL add-ons

| Line | Part | Harga |
|---|---|---:|
| E-005 | DS3231SN RTC module | Rp49.500 |
| E-021 | OLED 0.96 SSD1306 I2C | Rp33.300 |
| E-027 | JST-XH 4-pin cable for OLED | Rp12.300 |
| E-022 | WS2812B module | Rp8.500 |
| E-028 | JST-XH 6-pin cable for RTC | Rp8.000 |
| E-048 | JST-XH 3-pin cable for RGB | Rp5.000 |
| E-018 | 330 Ω resistor | Rp1.000 |
| **FULL add-ons** | | **Rp117.600** |

FULL = CORE + add-ons = **Rp815.897** sebelum ongkir. Ini fitur display/time/RGB, bukan safety tambahan.

---

## 6. Skenario budget

### Skenario A — CORE beli sekarang

- ESP32 compatible Rp139.968
- PZEM 100 A closed CT Rp150.000
- CORE lain Rp408.329
- **Subtotal Rp698.297**
- Ongkir Rp40.000
- **All-in Rp738.297 → di bawah Rp750.000**

### Skenario B — CORE dengan restock EasyWare

- ESP32 Rp103.500
- PZEM Rp135.000
- CORE lain Rp408.329
- **Subtotal Rp646.829**
- Ongkir Rp40.000
- **All-in Rp686.829 → margin ~Rp63.000**

### Skenario C — FULL

- CORE Rp698.297
- Add-ons Rp117.600
- **Subtotal Rp815.897**
- Ongkir Rp40.000
- **All-in Rp855.897 → +Rp105.897 (14,1%) di atas cap**

FULL tidak realistis di Rp750.000 tanpa menunda fitur. Jangan menurunkan safety.

---

## 7. Strategi pemasok

- **EasyWare (Bandung):** harga bagus, stok cepat habis. Cocok untuk OLED, RTC, passives, header. Cek restock.
- **Shopee/Tokopedia via BigGo:** stok luas, harga kompetitif, tapi clone/counterfeit dan ongkir bervariasi. Buka halaman seller sebelum beli.
- **CNC Store Bandung:** referensi HLK-5M05 Rp63.300, stok habis.
- **Blibli:** kabel NYYHY Supreme 3×1.5 Rp29.000/m terverifikasi.
- **Lokal/Jaya Plaza:** terminal, fuse holder, kabel, gland, screw, heatshrink.

---

## 8. Risiko stok dan kualitas

| Risiko | Dampak | Mitigasi |
|---|---|---|
| EasyWare ESP32/PZEM habis | CORE +Rp51.468 | Beli marketplace; CORE masih Rp738.297 all-in. |
| ESP32 compatible bukan resmi | GPIO/RGB/regulator berbeda | Foto, ukur pinout, catat deviasi Q08=B. |
| PZEM internal isolation saja | Single barrier; creepage batch belum | Hipot/leakage review; jangan USB saat mains. |
| Tidak ada sensor suhu | Firmware tidak bisa deteksi overheat | Fuse + TCO + thermal test; label dan prosedur. |
| HLK-5M05 counterfeit | Isolasi/efisiensi buruk | Seller bereputasi, marking, hipot/thermal. |
| Relay 10 A klaim | Kontak panas/weld | Uji 8 A thermal/lifecycle; fuse/TCO. |
| Enclosure ABS | Flame rating belum | Review material/UL94; jangan klaim aman. |
| Fuse/MOV/TCO generic | Rating tidak pasti | Verifikasi MPN/marking; uji lab. |
| Socket/plug tanpa cert | PE/kontak buruk | Brand Simon/BOSS, uji PE/tarik. |
| Kabel NYYHY bukan H05VV-F | Kurang fleksibel | 3×1.5, strain relief, ferrule. |

---

## 9. Urutan pembelian

### Tahap 1 — CORE

1. ESP32-S3 N16R8 Rp139.968 (atau restock Rp103.500)
2. PZEM-004T V4 100 A CT Rp150.000 (atau restock Rp135.000)
3. HLK-5M05 Rp49.000
4. Relay 2 channel Rp16.650
5. Fuse Littelfuse 10 A + holder Rp23.800
6. MOV 10D271K Rp7.500
7. Thermal fuse 99 °C Rp4.995
8. Terminal blocks + PE terminal Rp29.360
9. Simon socket + BOSS plug + gland Rp41.470
10. Enclosure 220×120×70 Rp99.684
11. 74HCT125 + divider/pullups/passives Rp18.220
12. JST/header/kabel Rp43.350
13. PCB carrier Rp15.000
14. Labels, heatshrink, fastener, bracket Rp35.300

### Tahap 2 — FULL

- OLED Rp33.300
- DS3231 Rp49.500
- WS2812 + JST Rp13.500
- JST OLED/RTC Rp20.300

Tahap 2 menambah **Rp117.600**. Jangan beli sebelum CORE lulus uji SELV dan thermal awal.

---

## 10. Red flags

- PZEM 10 A untuk 8 A kontinu.
- Relay tanpa optocoupler/marking.
- HLK/PSU tanpa marking atau harga jauh di bawah pasar.
- Fuse kaca sembarangan; gunakan ceramic 250 VAC + holder rated.
- MOV/TCO tanpa rating jelas; KSD301 auto-reset bukan TCO one-shot.
- Socket/plug tanpa PE/cable clamp.
- Enclosure ABS diklaim “fireproof” tanpa UL94.
- ESP32 “N16R8” yang ternyata N8R2/N8R8.
- PZEM “V4” yang ternyata V3.

---

## 11. Status safety

Semua komponen mains tetap:

`PENDING_APPROVAL` / `DOCUMENTATION_DEFICIENT` / `BLOCKED`

Belum ada yang `READY_FOR_FABRICATION` atau `READY_FOR_USE`. Sebelum energisasi:

- review creepage/clearance, PE, fuse/MOV/TCO coordination;
- hipot/leakage test (termasuk PZEM internal barrier);
- thermal test enclosure 220×120×70 pada ambient 40 °C;
- load/inrush 8 A, relay lifecycle, enclosure material/fit/impact;
- uji firmware tanpa sensor suhu (kebijakan ON dan warning).

---

## 12. Sumber utama (15–16 November 2026)

- EasyWare ESP32-S3 N16R8: https://store.easyware.id/produk/esp32-s3-n16r8-devkitc-1-dual-usb-c/
- EasyWare PZEM V4: https://store.easyware.id/produk/peacefair-pzem-004t-v40-modul-energy-meter-ac-80-260v-10a-100a-ct-split-ct-ttl-modbus-arduino-esp32/
- EasyWare OLED: https://store.easyware.id/produk/oled-0-96-inch-128x64-ssd1306/
- EasyWare DS3231: https://store.easyware.id/produk/modul-rtc-ds3231-real-time-clock-i2c-eeprom-at24c32-jam-presisi-arduino-esp32-baterai-cadangan/
- CNC Store HLK-5M05: https://cncstorebandung.com/product/hi-link-hlk-5m05-module-ac-to-dc-5v-1a-5-watt/
- Shopee ESP32 N16R8: https://shopee.co.id/product/18800073/40152181733
- Shopee PZEM 100 A CT: https://shopee.co.id/product/18800073/41719667847
- Shopee HLK-5M05: https://shopee.co.id/product/29614947/7316405255
- Shopee relay 2 channel: https://shopee.co.id/product/214108565/5414791883
- Shopee enclosure Duradus: https://shopee.co.id/product/115758056/5491049261
- Shopee Simon socket: https://shopee.co.id/product/1393930173/24138502361
- Shopee BOSS plug: https://shopee.co.id/product/37155877/41075654392

**Harga/listing lengkap:** `bom/BOM_PROCUREMENT.csv` (54 baris, tanggal, seller, URL, status verifikasi).

---

**Catatan akhir:** dokumen ini riset pengadaan, bukan persetujuan komponen. Harga listing bukan quote. Jangan mengenergisasi mains atau memfabrikasi PCB berdasarkan dokumen ini tanpa review engineer dan uji lab.
