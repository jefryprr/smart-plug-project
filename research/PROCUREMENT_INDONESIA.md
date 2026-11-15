# Procurement Indonesia — Prototype Smart Plug 8 A

**Tanggal riset:** 15 November 2026  
**Mata uang:** IDR  
**Status:** `PROCUREMENT_RESEARCH` / `NOT_APPROVED` / `NOT_FOR_FABRICATION`  
**Daftar belanja terstruktur:** `bom/BOM_PROCUREMENT.csv` dan `bom/BOM_PROCUREMENT.md`

---

## 1. Ringkasan eksekutif

Riset ini menjawab satu pertanyaan: **komponen apa yang benar-benar bisa dibeli di Indonesia sekarang, di mana, berapa harganya, dan apakah muat di budget Rp500.000–750.000?**

Hasilnya:

| Konfigurasi | Subtotal | + ongkir estimasi Rp40.000 | Status budget |
|---|---:|---:|---|
| **Elektronik inti** (tanpa enclosure, konektor, kabel, mekanik) | **Rp526.923** | — | di dalam budget |
| **CORE** (safety/function minimum, 39 baris) | **Rp756.987** | **Rp796.987** | sedikit di atas cap |
| **CORE dengan harga restock EasyWare** | **Rp705.519** | **Rp745.519** | **masuk budget** |
| **FULL** (CORE + OLED + RTC + RGB + konektor) | **Rp895.976** | **Rp935.976** | jelas di atas budget |

**Kesimpulan:** budget Rp750.000 **tidak cukup** untuk prototype lengkap dengan OLED, RTC, RGB, dan semua konektor pada harga marketplace saat ini. Budget **cukup untuk elektronik inti** dan **hampir cukup untuk CORE fisik**. CORE hanya bisa masuk Rp750.000 all-in jika ESP32-S3 dan PZEM dibeli pada harga restock EasyWare (Rp103.500 dan Rp135.000), atau ongkir ditekan mendekati nol.

Jangan menurunkan fuse, MOV, thermal cutoff, terminal, PE, enclosure, atau barrier isolasi untuk mengejar budget. Itu bukan cost optimization; itu safety downgrade.

---

## 2. Metode dan tingkat keyakinan harga

Harga diambil pada **15 November 2026** dari halaman produk atau listing marketplace. Tidak ada harga rekaan. Setiap baris punya status:

| Status | Arti |
|---|---|
| `VERIFIED_STORE_PAGE` | Harga dan produk dibaca langsung dari halaman toko (EasyWare, Blibli). |
| `VERIFIED_AGGREGATOR` | Harga dan judul produk diambil dari listing Shopee/Tokopedia via BigGo; halaman seller tidak dibuka satu per satu. |
| `ESTIMATED` | Tidak ada listing exact; harga diestimasi dari komponen sejenis. Wajib dikonfirmasi sebelum beli. |
| `UNKNOWN` | Tidak ada harga yang bisa dipertanggungjawabkan. Tidak dipakai di total. |

Yang **tidak** termasuk:
- ongkir aktual, pajak, bea impor, biaya platform;
- alat (multimeter, solder, crimp tool, hipot tester);
- biaya 3D print/jasa bengkel;
- biaya uji lab;
- biaya PCB fungsional (PCB sekarang masih placement-only).

Harga marketplace berubah cepat. Anggap angka ini sebagai **snapshot**, bukan quote.

---

## 3. Keputusan komponen inti

### 3.1 MCU — ESP32-S3 N16R8

| Kandidat | Harga | Sumber | Stok | Catatan |
|---|---:|---|---|---|
| EasyWare ESP32-S3 N16R8 DevKitC-1 | Rp103.500 | `store.easyware.id` | **habis** | Harga terbaik, tapi tidak bisa dibeli sekarang. |
| Shopee N16R8 compatible (ALFA Electronics) | Rp139.968 | `shopee.co.id/product/18800073/40152181733` | listed | Board compatible, **bukan** board Espressif resmi. |
| Shopee N16R8 lain | Rp117.600–Rp174.000 | BigGo | listed | Kualitas/varian tidak seragam. |
| Official Espressif | belum ada stok lokal terverifikasi | Mouser/DigiKey | luar negeri | Biaya kirim/impor tinggi. |

**Keputusan:** gunakan board N16R8 **compatible** Rp139.968 untuk prototype, dengan deviasi Q08=B dicatat eksplisit. Jangan menyebutnya board resmi. Verifikasi marking N16R8, GPIO RGB (v1.0=48, v1.1=38), regulator, USB, dan pinout sebelum firmware dikunci.

### 3.2 Metering — PZEM-004T V4 100 A

| Varian | Harga | Sumber | Stok | Catatan |
|---|---:|---|---|---|
| EasyWare 10 A | Rp112.500 | `store.easyware.id` | habis | **Tidak dipakai** untuk 8 A kontinu; tidak ada margin. |
| EasyWare 100 A close CT | Rp135.000 | `store.easyware.id` | habis | Harga bagus jika restock. |
| EasyWare 100 A open CT | Rp180.000 | `store.easyware.id` | habis | Split CT, lebih mudah dipasang. |
| Shopee 100 A closed CT (ALFA) | Rp150.000 | `shopee.co.id/product/18800073/41719667847` | listed | Dipakai di CORE. |
| Shopee 100 A split CT | Rp250.000–Rp321.000 | BigGo | listed | Lebih mahal; tidak perlu untuk prototype. |

**Keputusan:** PZEM-004T V4 **100 A CT**. Varian closed CT cukup; bedanya hanya cara memasang kabel, bukan akurasi. Jangan memakai varian 10 A untuk beban 8 A kontinu. CT 100 A adalah rating sensor, bukan izin arus output.

### 3.3 PSU — Hi-Link HLK-5M05

| Sumber | Harga | Stok | Catatan |
|---|---:|---|---|
| Shopee Marnov Electronic | Rp49.000 | listed | Dipakai di CORE. |
| Shopee lain | Rp49.900–Rp64.000 | listed | Banyak varian/klaim “original”. |
| CNC Store Bandung | Rp63.300 | **habis** | Harga retailer lokal, stok kosong. |

**Keputusan:** HLK-5M05 Rp49.000–Rp64.000. Status tetap `PENDING_APPROVAL`. Efisiensi hanya ~70% pada 220 V full load, jadi panas ~2.1 W. Batch certificate, isolasi, creepage, dan counterfeit belum terbukti. Jangan membeli modul tanpa marking.

### 3.4 Relay — modul 2 channel 5 V optocoupler

| Sumber | Harga | Catatan |
|---|---:|---|
| Shopee AIFRobotic | Rp16.650 | Dipakai di CORE. |
| Shopee lain | Rp12.000–Rp34.848 | Kualitas relay/modul bervariasi. |

**Keputusan:** modul 2 channel 5 V optocoupler, **dua SPDT independen**, bukan DPST mechanically linked. Klaim 10 A adalah klaim vendor. Rating final 8 A hanya setelah uji thermal/lifecycle. Verifikasi active-LOW, JD-VCC, dan pinout.

### 3.5 Sensor suhu — TMP102

| Sumber | Harga | Catatan |
|---|---:|---|
| Shopee GY-TMP102 breakout | Rp50.000 | Dipakai di CORE. |
| Shopee TMP102 breakout lain | Rp68.040 | Alternatif. |
| MCP9808 module | Rp66.500–Rp69.000 | Alternatif jika TMP102 sulit. |
| DS18B20 waterproof | Rp10.000–Rp17.640 | Alternatif murah, tetapi 1-Wire dan firmware belum ada. |

**Keputusan:** GY-TMP102 breakout Rp50.000 untuk prototype. IC asli TMP102AIDRLR SOT-563 tetap desain carrier. Verifikasi marking/address; tempatkan di hotspot relay/terminal.

### 3.6 Isolasi UART — ADuM1201 + B0505S

| Parts | Harga | Sumber | Catatan |
|---|---:|---|---|
| CJMCU ADUM1201 module | Rp25.900 | Shopee | Modul, bukan barrier tersertifikasi. |
| Mornsun B0505S-1WR3 | Rp38.500 | Shopee | Genuine Mornsun; clone Rp22.000 ditolak. |

**Keputusan:** pakai keduanya sebagai barrier eksternal provisional. B0505S memberi supply terisolasi ke sisi PZEM; tanpa itu, ADuM tidak menambah isolasi karena ground kedua sisi menjadi common. Modul ADuM murah tetap harus diuji creepage/hipot. Alternatif: percaya optocoupler internal PZEM **hanya** jika engineer menyetujui setelah uji — itu bukan default.

### 3.7 Proteksi mains

| Parts | Harga | Sumber | Catatan |
|---|---:|---|---|
| Littelfuse 5x20 10 A 250 VAC slow-blow | Rp18.300 | Shopee | Verifikasi MPN/marking/breaking capacity. |
| Fuse holder panel 5x20 | Rp5.500 | Shopee | Tool-access, mount di dalam enclosure. |
| MOV 10D271K 275 VAC | Rp7.500 | Shopee | Generic; EPCOS S10K275 lebih baik. |
| Thermal fuse 99 °C 10 A | Rp4.995 | Shopee | Generic; Sefuse SF169E batch datasheet belum ada. |

**Keputusan:** semua tetap `PENDING_APPROVAL`/`DOCUMENTATION_DEFICIENT`. Ini bukan pengganti koordinasi proteksi dan uji lab.

### 3.8 Terminal, socket, plug, enclosure

| Parts | Harga | Sumber | Catatan |
|---|---:|---|---|
| Terminal block 5.08 2-pin | Rp2.450 | Shopee | Generic 5EDR; bukan Phoenix. |
| Terminal block 5.08 5-pin | Rp11.760 | Shopee | Untuk PZEM. |
| PE terminal 6 mm² | Rp10.250 | Shopee | PE harus kontinu, tidak diswitch/fuse. |
| Simon Schuko socket 16 A | Rp25.026 | Shopee | Model/sertifikasi/PE belum diverifikasi. |
| BOSS BP16 Schuko plug 16 A | Rp14.044 | Shopee | Cable clamp/PE belum diverifikasi. |
| M16 cable gland IP68 | Rp2.400 | Shopee | Strain relief ke enclosure. |
| MG Duradus 220×120×70 ABS IP65 | Rp99.684 | Shopee | Ukuran exact; flame rating ABS **belum** terverifikasi. |

**Keputusan:** enclosure exact-size Rp99.684 dipakai untuk fit-check, tetapi tetap `BLOCKED` sampai material flame-retardant, fit, thermal, impact, dan PE review selesai. ABS belum otomatis UL94 V-0.

### 3.9 Kabel dan wiring

| Parts | Harga | Sumber | Catatan |
|---|---:|---|---|
| NYYHY 3×1.5 mm² flexible | Rp29.000/m | Blibli/Supreme | 0.5 m = Rp14.500; bukan H05VV-F. |
| Hookup wire 0.25 mm² | Rp5.000 | estimasi | SELV only. |
| Heatshrink 5 mm | Rp2.400–Rp5.000 | Shopee | Flame rating belum diverifikasi. |
| Ferrules/crimp | belum dihitung | — | Wajib untuk terminal mains; alat terpisah. |

---

## 4. Rincian budget CORE

| Kelompok | Subtotal |
|---|---:|
| Metering (PZEM) | Rp150.000 |
| MCU (ESP32) | Rp139.968 |
| Mechanical (enclosure, bracket, PE, fastener) | Rp131.884 |
| Connectors (terminal, socket, plug, gland, header) | Rp71.680 |
| Isolation (ADuM + B0505S) | Rp64.400 |
| Sensing (TMP102) | Rp50.000 |
| Power (HLK-5M05) | Rp49.000 |
| Protection (fuse, holder, MOV, TCO) | Rp36.295 |
| Cable (mains + hookup) | Rp19.500 |
| Switching (relay + MOSFET) | Rp18.150 |
| UI (button) | Rp7.000 |
| Passives | Rp6.610 |
| PCB/protoboard | Rp5.500 |
| Consumables (heatshrink) | Rp5.000 |
| Labels | Rp2.000 |
| **CORE total** | **Rp756.987** |

Top 10 cost drivers:

1. PZEM 100 A — Rp150.000
2. ESP32-S3 N16R8 — Rp139.968
3. Enclosure 220×120×70 — Rp99.684
4. TMP102 breakout — Rp50.000
5. HLK-5M05 — Rp49.000
6. B0505S — Rp38.500
7. ADuM1201 module — Rp25.900
8. Simon socket — Rp25.026
9. Littelfuse fuse — Rp18.300
10. Relay module — Rp16.650

Elektronik inti (MCU + metering + PSU + sensor + isolasi + relay + proteksi + passives + protoboard) = **Rp526.923**. Sisanya enclosure, konektor, kabel, dan mekanik.

---

## 5. Rincian FULL add-ons

| Line | Part | Harga |
|---|---|---:|
| E-005 | DS3231SN RTC module | Rp49.500 |
| E-021 | OLED 0.96 SSD1306 I2C | Rp33.300 |
| E-009 | SN74AHCT1G125 buffer | Rp16.389 |
| E-025 | JST-XH 4-pin cable | Rp12.300 |
| E-022 | WS2812B module | Rp8.500 |
| E-028 | JST-XH 6-pin cable (est.) | Rp8.000 |
| E-026 | JST-XH 2-pin cable (est.) | Rp5.000 |
| E-027 | JST-XH 3-pin cable (est.) | Rp5.000 |
| E-018 | 330 Ω resistor | Rp1.000 |
| **FULL add-ons** | | **Rp138.989** |

FULL = CORE + add-ons = **Rp895.976** sebelum ongkir. Ini fitur lengkap (display, RTC, RGB, konektor), bukan safety tambahan.

---

## 6. Skenario budget

### Skenario A — CORE dengan restock EasyWare (rekomendasi)

- ESP32-S3 Rp103.500 (restock)
- PZEM 100 A close CT Rp135.000 (restock)
- CORE lain Rp518.019
- **Subtotal Rp705.519**
- Ongkir Rp40.000
- **All-in Rp745.519** → **di bawah Rp750.000**

Syarat: kedua barang restock pada harga lama. Jika tidak, skenario ini gagal.

### Skenario B — CORE beli sekarang

- ESP32 compatible Rp139.968
- PZEM 100 A closed CT Rp150.000
- **Subtotal Rp756.987**
- Ongkir Rp40.000
- **All-in Rp796.987** → **+Rp46.987 (6,3%) di atas cap**

Ini bukan kegagalan safety; ini selisih harga pasar. Bisa ditutup dengan menunggu restock, mengurangi ongkir, atau menaikkan budget sedikit.

### Skenario C — FULL

- CORE Rp756.987
- Add-ons Rp138.989
- **Subtotal Rp895.976**
- Ongkir Rp40.000
- **All-in Rp935.976** → **+Rp185.976 (24,8%) di atas cap**

FULL tidak realistis di Rp750.000 tanpa mengubah fitur atau menurunkan komponen safety. Jangan pura-pura bisa.

---

## 7. Strategi pemasok

### EasyWare (Bandung)

Kelebihan: harga sering lebih murah dari marketplace, produk jelas, halaman bisa diverifikasi. Kekurangan: stok cepat habis, terutama ESP32 dan PZEM. Cocok untuk OLED, RTC, passives, header, heatshrink. Cek restock sebelum memulai build.

### Shopee / Tokopedia via BigGo

Kelebihan: stok luas, harga kompetitif, banyak seller. Kekurangan: harga berubah, judul kadang menyesatkan, clone/counterfeit, ongkir bervariasi. Gunakan BigGo untuk membandingkan, lalu buka halaman seller dan cek rating/ulasan. Jangan membeli relay/PSU/PZEM dari seller tanpa riwayat.

### CNC Store Bandung

Harga HLK-5M05 Rp63.300 terverifikasi di halaman produk, tetapi stok habis. Berguna sebagai pembanding harga dan untuk komponen mekanik/3D print.

### Blibli

Kabel NYYHY Supreme 3×1.5 Rp29.000/m terverifikasi. Cocok untuk kabel dan barang brand, tetapi ongkir bisa lebih tinggi.

### Toko lokal / Jaya Plaza

Untuk terminal, fuse holder, kabel, gland, screw, heatshrink. Harga bisa lebih murah dan tanpa ongkir, tetapi stok/varian tidak online. Rekomendasi: beli komponen pasif/mekanik lokal, komponen aktif online.

---

## 8. Risiko stok dan kualitas

| Risiko | Dampak | Mitigasi |
|---|---|---|
| EasyWare ESP32/PZEM habis | CORE +Rp51.468 | Tunggu restock atau beli marketplace; jangan ganti ke 10 A. |
| ESP32 compatible bukan resmi | GPIO/RGB/regulator berbeda | Foto board, ukur pinout, verifikasi N16R8; catat deviasi Q08=B. |
| PZEM V4 batch berbeda | Pinout/UART/CT ratio berbeda | Ukur sebelum wiring; dokumentasi batch; jangan percaya warna kabel. |
| HLK-5M05 counterfeit | Isolasi/efisiensi/creepage buruk | Beli seller bereputasi; cek marking; hipot/thermal test. |
| Relay module 10 A klaim | Kontak panas/weld | Uji 8 A thermal/lifecycle; gunakan fuse/TCO; jangan klaim DPST. |
| Enclosure ABS | Tidak flame-retardant | Review material/UL94; jangan klaim aman; pertimbangkan PC/ABS FR atau metal. |
| Fuse/MOV/TCO generic | Rating/breaking capacity tidak pasti | Verifikasi MPN/marking; fuse Littelfuse; TCO batch datasheet; uji lab. |
| Socket/plug tanpa cert | PE/kontak/retensi buruk | Beli brand (Simon/BOSS), cek marking, uji PE kontinuitas dan tarik. |
| Kabel NYYHY bukan H05VV-F | Kurang fleksibel untuk cord | Gunakan 3×1.5, strain relief, ferrule; atau beli H05VV-F jadi. |
| ADuM/B0505S module murah | Creepage/isolasi tidak memadai | Hipot/leakage review; jangan anggap modul = barrier tersertifikasi. |

---

## 9. Urutan pembelian yang disarankan

### Tahap 1 — CORE safety/function (beli sekarang atau tunggu restock)

1. ESP32-S3 N16R8 (EasyWare restock Rp103.500, fallback Rp139.968)
2. PZEM-004T V4 100 A CT (EasyWare restock Rp135.000, fallback Rp150.000)
3. HLK-5M05 Rp49.000
4. Relay 2 channel Rp16.650
5. Fuse Littelfuse 10 A + holder Rp23.800
6. MOV 10D271K Rp7.500
7. Thermal fuse 99 °C Rp4.995
8. Terminal blocks + PE terminal Rp29.360
9. Simon socket + BOSS plug + gland Rp41.470
10. Enclosure 220×120×70 Rp99.684
11. ADuM1201 + B0505S Rp64.400
12. TMP102 breakout Rp50.000
13. Kabel, protoboard, labels, heatshrink, fastener, bracket Rp52.300
14. AO3400, resistors, caps, diode Rp6.610

### Tahap 2 — UI/time (setelah CORE hidup dan aman di SELV)

- OLED Rp33.300
- DS3231 RTC Rp49.500
- WS2812 + buffer Rp24.889
- JST connectors Rp30.300

Tahap 2 menambah **Rp138.989**. Jangan membeli ini sebelum CORE lulus uji SELV dan thermal awal.

---

## 10. Red flags — jangan dibeli

- PZEM 10 A untuk beban 8 A kontinu.
- Relay module tanpa optocoupler atau tanpa marking rating.
- HLK/PSU tanpa marking, atau harga jauh di bawah pasar.
- Fuse kaca sembarangan untuk mains; gunakan ceramic 250 VAC dan holder rated.
- MOV tanpa rating/tegangan jelas.
- Thermal fuse yang diklaim “auto-reset” (KSD301) sebagai pengganti one-shot TCO.
- Socket/plug tanpa PE atau tanpa cable clamp.
- Enclosure ABS yang diklaim “fireproof” tanpa bukti UL94.
- ADuM/B0505S clone tanpa datalog/hipot.
- ESP32 “N16R8” yang ternyata N8R2/N8R8; cek marking.
- PZEM “V4” yang ternyata V3; jangan asumsikan protokol/pinout sama.

---

## 11. Status safety

Semua komponen mains tetap:

`PENDING_APPROVAL` / `DOCUMENTATION_DEFICIENT` / `BLOCKED`

Belum ada yang `READY_FOR_FABRICATION` atau `READY_FOR_USE`. Harga dan stok tidak mengubah status safety. Sebelum energisasi mains:

- review engineer untuk creepage/clearance, PE, fuse/MOV/TCO coordination;
- hipot/leakage test;
- thermal test di enclosure 220×120×70 pada ambient 40 °C;
- load/inrush test 8 A;
- relay lifecycle test;
- enclosure material/fit/impact review.

---

## 12. Sumber utama (dicek 2026-11-15)

**Toko langsung:**
- EasyWare ESP32-S3 N16R8: https://store.easyware.id/produk/esp32-s3-n16r8-devkitc-1-dual-usb-c/
- EasyWare PZEM V4: https://store.easyware.id/produk/peacefair-pzem-004t-v40-modul-energy-meter-ac-80-260v-10a-100a-ct-split-ct-ttl-modbus-arduino-esp32/
- EasyWare OLED: https://store.easyware.id/produk/oled-0-96-inch-128x64-ssd1306/
- EasyWare DS3231: https://store.easyware.id/produk/modul-rtc-ds3231-real-time-clock-i2c-eeprom-at24c32-jam-presisi-arduino-esp32-baterai-cadangan/
- CNC Store HLK-5M05: https://cncstorebandung.com/product/hi-link-hlk-5m05-module-ac-to-dc-5v-1a-5-watt/
- Blibli NYYHY 3×1.5: https://www.blibli.com/p/kabel-listrik-serabut-nyyhy-3x1-5-supreme-meteran/is--GUL-70047-00870-00001

**Marketplace (link produk):**
- ESP32 N16R8 compatible: https://shopee.co.id/product/18800073/40152181733
- PZEM 100 A closed CT: https://shopee.co.id/product/18800073/41719667847
- HLK-5M05: https://shopee.co.id/product/29614947/7316405255
- Relay 2 channel: https://shopee.co.id/product/214108565/5414791883
- TMP102 breakout: https://shopee.co.id/product/12793026/7334661838
- ADUM1201 module: https://shopee.co.id/product/18800073/56958705695
- B0505S-1WR3: https://shopee.co.id/product/119918417/20095650678
- Littelfuse fuse: https://shopee.co.id/product/88911101/12944617615
- Enclosure Duradus: https://shopee.co.id/product/115758056/5491049261
- Simon socket: https://shopee.co.id/product/1393930173/24138502361
- BOSS plug: https://shopee.co.id/product/37155877/41075654392

**Harga/listing lengkap:** lihat `bom/BOM_PROCUREMENT.csv` (48 baris, tanggal, seller, URL, status verifikasi).

---

**Catatan akhir:** dokumen ini adalah riset pengadaan, bukan persetujuan komponen. Harga listing bukan quote. Stok marketplace bisa berubah sebelum pembelian. Jangan mengenergisasi mains atau memfabrikasi PCB berdasarkan dokumen ini.
