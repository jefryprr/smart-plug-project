# Riset Komponen — REV_A_PROVISIONAL

**Tanggal riset:** 15 November 2026
**Status:** `RESEARCH_ONLY` / `NOT_APPROVED`
**Keputusan pengguna:** Q09=D (bandingkan metering), Q10=C (studi 2–3 alternatif relay), Q11=D (pilih berdasar isolasi/dimensi).
**Aturan:** Skor bukan pengganti datasheet. Harga kosong sampai ada kutipan nyata. Rating yang tidak terverifikasi ditandai `UNKNOWN`/`UNVERIFIED`.

## Ringkasan rekomendasi bertingkat

| Fungsi | Rekomendasi utama | Alternatif | Status |
|---|---|---|---|
| MCU board | Espressif ESP32-S3-DevKitC-1 N16R8 resmi | N8R8 resmi; modul WROOM-1 bare | **PENDING_APPROVAL**; revisi board harus diverifikasi |
| Metering | PZEM-004T V4 100 A split CT **dengan barrier isolasi wajib** | ADE7953 + CT + isolasi; HLW8032 + shunt | **DOCUMENTATION_DEFICIENT**; V4 belum final |
| Relay/pemutus | **2-channel 5 V optocoupler module, off-board** (10 A class claim; final 8 A) | TE RT2 DPST-NO (earlier); Schneider Acti9 iCT 2P 16 A (besar) | **DOCUMENTATION_DEFICIENT**; dua SPDT tidak linked |
| PSU | **Hi-Link HLK-5M05** (user-selected) | Mean Well IRM-05-5 (better docs, larger); Recom RAC01-05SC (too low current) | **PENDING_APPROVAL**; efficiency ~70%, isolation/cert batch unverified |
| Fuse | Littelfuse 215 series 10 A time-lag | Schurter 0001.2510; Bel 5TT 10 | **PENDING_APPROVAL**; koordinasi belum |
| MOV | EPCOS S10K275 | Littelfuse V275LA10P; Bourns MOV-10D271K | **PENDING_APPROVAL**; studi surge belum |
| Thermal cutoff | Sefuse SF169E 99 °C 10 A | Therm-O-Disc one-shot; KSD301 (ditolak) | **DOCUMENTATION_DEFICIENT** |
| Sensor suhu | TI TMP102AIDRLR | MCP9808; DS18B20 | **PENDING_APPROVAL** |
| OLED | SSD1306 0.96" I2C | SH1106 1.3"; bare panel | **DOCUMENTATION_DEFICIENT** |
| Socket/plug | Type F 16 A 2P+E (Q02 lean) | Type E/F combo; standar lokal | **DOCUMENTATION_DEFICIENT/BLOCKED** |
| Enclosure | ABS/PC **220x120x70 confirmed (Q06=C)**, flame-retardant (150x100 and 180x120 fail clearance) | Hammond/Bud rated enclosure; 3D print prototype | **BLOCKED**; material belum dipilih |
| Isolasi UART | ADuM1201 + B0505S-1WR3 | Si8622 + R1SE-0505; optocoupler + isolated DC/DC | **PENDING_APPROVAL** |
| RTC | DS3231MZ+ | PCF8523T; SNTP holdover | **PENDING_APPROVAL** |

## 1. MCU board

| Kandidat | Kelebihan | Kekurangan/risiko | Skor bukti |
|---|---|---|---|
| Espressif ESP32-S3-DevKitC-1 N16R8 resmi | Dokumen resmi, USB, 16 MB flash/8 MB PSRAM, onboard RGB, regulator 3.3 V | Revisi v1.0 vs v1.1 berbeda untuk GPIO RGB; board besar; harga lebih tinggi | 4/5 |
| Espressif DevKitC-1 N8R8 | Sama, flash/PSRAM lebih kecil | PSRAM 8 MB tetap; flash 8 MB mungkin cukup, tetapi N16R8 diminta | 3/5 |
| Clone pihak ketiga | Murah, tersedia lokal | Pin/RGB/strapping/regulator tidak dapat disimpulkan dari DevKitC-1 resmi | 1/5 |
| ESP32-S3-WROOM-1 bare | Paling ringkas untuk produksi | Perlu RF, antenna, USB, regulator, flash/PSRAM, dan desain baru | 3/5 |

**Temuan:** dokumen Espressif membedakan LED RGB v1.0 (GPIO48) dan v1.1 (GPIO38). Board pihak ketiga tidak boleh dianggap sama. GPIO33–37 tidak dipakai karena N16R8 memakai octal PSRAM. GPIO0/3/45/46 adalah strapping; hindari untuk relay/aktuator.

**Sumber:**
- https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html
- https://documentation.espressif.com/api/resource/path/docs/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html
- https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf

**Status:** `PENDING_APPROVAL`; foto depan-belakang dan pengukuran header wajib sebelum GPIO final.

## 2. Metering

| Kandidat | Isolasi | Dokumentasi | Ukuran | Interface | Risiko | Skor |
|---|---|---|---|---|---|---|
| PZEM-004T V4 100 A split CT | **UNVERIFIED** untuk batch V4; barrier eksternal direncanakan | Manual resmi batch belum diperoleh; arsip historis tidak otomatis berlaku | Modul besar (~89×53×24 mm, approximate) | UART TTL/Modbus | Pinout/level/isolasi/CT ratio belum pasti; terminal voltage mains | 2/5 |
| PZEM-004T V3 100 A | Sama, versi lebih lama | Lebih banyak arsip, tetapi bukan V4 | Mirip | UART | Membeli V3 bukan solusi dokumentasi V4 | 2/5 |
| ADE7953 + CT + isolasi | Dapat dirancang dengan barrier yang jelas | Datasheet ADI tersedia | IC kecil, tapi butuh CT, burden, supply | SPI/I2C | Desain baru, kalibrasi, biaya, waktu | 4/5 |
| HLW8032 + shunt | Sederhana | Datasheet tersedia | Kecil | UART | Shunt membawa arus beban; isolasi UART tetap perlu; tidak cocok untuk 8 A kontinu tanpa desain termal | 2/5 |
| Shelly EM (modul jadi) | Produk jadi | Dokumen terbatas | Modul | Wi-Fi/API | Bukan desain terbuka; integrasi dan sertifikasi tidak dapat diklaim | 1/5 |

**Temuan:** CT 100 A hanya rating sensor, bukan izin arus output. PZEM V4 dengan CT berarti jalur arus utama tidak melalui modul, tetapi terminal tegangan tetap mains-referenced. Barrier UART `ADuM1201` + isolated DC/DC `B0505S` direncanakan sebagai solusi provisional; ini belum menggantikan review isolasi assembly.

**Sumber:**
- https://github.com/im-0/pzem-004t-original-docs (arsip historis)
- https://www.easyware.co.id/product/peacefair-pzem-004t-v4-ac-power-energy-meter-uart-modbus-original/ (ketersediaan, bukan datasheet)
- https://www.analog.com/en/products/ade7953.html
- https://www.analog.com/media/en/technical-documentation/data-sheets/ADuM1200_1201.pdf
- https://www.mornsun-power.com/html/pdf/B0505S-1WR3.html

**Status:** `DOCUMENTATION_DEFICIENT`. Jangan finalkan PZEM sebelum manual batch, pinout, level UART, isolasi, dan dimensi diukur.

## 3. Relay/pemutus

| Kandidat | Konfigurasi | Rating kelas | Kelebihan | Kekurangan | Skor |
|---|---|---|---|---|---|
| TE RT2 `RT444005` | DPST-NO (2 form A) | 8 A / 250 VAC (IEC), UL 10 A untuk varian tertentu | Dua kutub dalam satu relay, PCB mount, coil 5 V | Target lama 10 A tidak tercapai; final 8 A; rating UL/IEC harus dicek per MPN | 4/5 (earlier) |
| Omron G2R-2A | DPST-NO | 5 A / 250 VAC | Dokumen baik, dua kutub | Terlalu rendah untuk 8 A kontinu; derating jadi ~4 A | 3/5 |
| Schneider Acti9 iCT 2P 16 A | 2P contactor | 16 A / 250 VAC | Rating jelas, dua kutub, DIN rail | Besar, tidak muat 220×120×70; butuh enclosure lain | 3/5 |
| Dua Omron G5LE-1A | 2× SPST-NO | 10 A / 250 VAC masing-masing | Rating 10 A, murah | Tidak mechanically linked; kegagalan satu kontak tidak menjamin pemutusan dua kutub | 2/5 |
| Hongfa HF115F-L | DPST latching | 10 A class (klaim seri) | Dua kutub, coil rendah | Latching dapat tetap ON setelah power loss; bukan fail-safe | 1/5 |

**Temuan:** Target 10 A tidak dapat diklaim dengan relay 8 A. Rating final harus 8 A atau lebih rendah setelah uji termal, atau ganti ke contactor 16 A dengan enclosure lebih besar. Relay latching ditolak untuk kebijakan fail-safe. Relay optocoupler modul pasar tidak otomatis aman: contact arrangement, isolation, dan rating harus diverifikasi.

### 3A. Amendment pengguna: modul optocoupler 2 channel

Pengguna memilih **modul relay optocoupler 2 channel umum, 5 V, off-board** (bukan relay PCB DPST). Modul ini biasanya berisi **dua relay SPDT independen**, bukan DPST yang mechanically linked.

| Aspek | Temuan | Status |
|---|---|---|
| Konfigurasi | 2 channel SPDT (COM/NO/NC), biasanya aktif-LOW | `TYPICAL_MODULE` |
| Rating klaim | AC 250 V / 10 A per channel (vendor) | `UNVERIFIED` untuk batch |
| Input | 5 V, 15–20 mA per channel; optocoupler | `TYPICAL` |
| Isolasi | Optocoupler coil/input; bukan bukti creepage mains di PCB modul | `REVIEW_REQUIRED` |
| Kelebihan | Mudah diganti, mounting off-board, dua channel untuk L/N | — |
| Risiko | Tidak mechanically linked; satu channel weld/stuck; modul pasar tanpa datasheet batch | High |
| Keputusan | Gunakan **8 A final** dengan dua channel L/N, bracket di enclosure, driver MOSFET active-low | `PROVISIONAL` |

**Sumber:**
- Handsontec 2-channel 5 V optical isolated relay module datasheet: https://www.handsontec.com/dataspecs/module/2Ch-relay.pdf
- DigiKey TS0010D 2-channel relay module datasheet: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/5773/TS0010D%20DATASHEET.pdf
- Envistia product/user guide (active-LOW, JD-VCC, 10 A SPDT): https://envistiamall.com/products/2-channel-10a-optoisolated-power-relay-module-5v-control
- Catatan: halaman penjual bukan pengganti datasheet batch. Verifikasi pinout, level input, dan rating kontak saat barang tiba.

**Sumber:**
- https://www.mouser.com/datasheet/2/418/9/ENG_DS_RT2_3-576697.pdf
- https://omronfs.omron.com/en_US/ecb/products/pdf/en-g2r.pdf
- https://www.se.com/ww/en/product-range/642-acti9-ict/
- https://easby.com/shop/hf115f-l-double-pole-latching-relay (deskripsi seri, bukan datasheet resmi)

**Status:** `PENDING_APPROVAL`; pilihan `RT444005` adalah arah riset, bukan MPN final. Perlu exact coil voltage, UL/IEC rating, dan lifecycle.

## 4. PSU

| Kandidat | Output | Isolasi | Ukuran | Kelebihan | Kekurangan | Skor |
|---|---|---|---|---|---|---|
| Hi-Link HLK-5M05 | 5 V / 1 A, 5 W | Modul AC/DC, 2500 VAC claim | 38×23×18 mm | Kecil, murah, 4-pin, user-selected | Efficiency ~70% → ~2.1 W heat; batch certification/isolation/creepage unverified | 3/5 |
| Mean Well IRM-05-5 | 5 V / 1 A, 5 W | Modul AC/DC | ~53.5×28.5×19 mm | Dokumen resmi, efisiensi ~78%, thermal lebih baik | Lebih besar/mahal | 4/5 (fallback) |
| Recom RAC01-05SC | 5 V / 0.2 A | Modul AC/DC | Kecil | Dokumen baik | Arus 0.2 A terlalu kecil untuk Wi-Fi + relay | 2/5 |
| Hi-Link HLK-PM01 | 5 V / 0.6 A | Modul | Kecil/murah | Populer di Indonesia | Dokumentasi/kualitas batch bervariasi; isolation/creepage perlu verifikasi | 2/5 |
| Mean Well IRM-10-5 | 5 V / 2 A | Modul | Lebih besar | Margin arus besar | Ukuran/termal lebih besar | 3/5 |

**Power budget provisional:** ESP32-S3 + Wi-Fi peak ~0.35 A; OLED ~0.02 A; PZEM ~0.01 A; relay module 2 channel ~0.14 A typical / 0.16 A peak; RGB ~0.03 A; sensor/RTC ~0.003 A; total ~0.36 A typical, ~0.58 A peak. HLK-5M05 1 A gives ~42% margin at the estimate, but efficiency is only ~70% and heat is ~2.1 W at full load. This is not measured.

**Sumber:** https://www.hlktech.net/index.php?id=1243 (official page); `research/datasheets/hlk-5m05_distributor.pdf` (3-page distributor copy, drawing 38×23×18, 4 pins); `research/PSU_HLK_5M05.md`.

**Status:** `PENDING_APPROVAL`; batch certificate, isolation/leakage, ripple/startup, and thermal test required.

## 5. Proteksi arus, surge, dan termal

| Fungsi | Kandidat | Catatan | Status |
|---|---|---|---|
| Fuse | Littelfuse 215 10 A time-lag | Breaking capacity, holder, coordination belum | PENDING |
| Fuse holder | Schurter 0031.8201 | Touch-proof/tool-access belum | PENDING |
| MOV | EPCOS S10K275 | Surge study dan thermal coordination belum | PENDING |
| Thermal cutoff | Sefuse SF169E 99 °C 10 A | Datasheet batch belum; 10 A AC rating perlu bukti | DOCUMENTATION_DEFICIENT |
| Thermal cutoff alternatif | Therm-O-Disc one-shot | Perlu MPN dan rating | PENDING |
| Thermostat | KSD301 90 °C 10 A | Auto-reset, bukan one-shot; tidak dipilih sebagai satu-satunya proteksi | REJECTED |

**Catatan:** Fuse 10 A bukan izin arus kontinu 10 A. Beban kontinu provisional 8 A atau lebih rendah; fuse 10 A adalah backup. Thermal cutoff harus independen dari MCU dan dipasang di hotspot terminal/relay. MOV bukan fitur surge lengkap tanpa koordinasi dan uji.

## 6. Sensor, UI, dan RTC

| Fungsi | Kandidat | Kelebihan | Kekurangan | Skor |
|---|---|---|---|---|
| Suhu | TMP102AIDRLR | I2C, kecil, 3.3 V, datasheet TI | Perlu kalibrasi/posisi | 4/5 |
| Suhu | MCP9808 | Akurasi baik | Lebih mahal | 4/5 |
| Suhu | DS18B20 | Probe remote | 1-wire, response lambat | 3/5 |
| OLED | SSD1306 0.96" I2C | Umum, 3.3 V | Modul pasar tanpa datasheet pabrikan | 3/5 |
| OLED | SH1106 1.3" | Lebih besar | Controller berbeda; jangan assume kompatibel | 3/5 |
| RTC | DS3231MZ+ | TCXO, I2C, akurasi baik | Perlu battery/supercap | 4/5 |
| RTC | PCF8523T | Murah, I2C | Perlu crystal, drift | 3/5 |

## 7. Socket, plug, enclosure, dan PE

| Fungsi | Kandidat | Status | Alasan |
|---|---|---|---|
| Socket | Type F 16 A 2P+E | DOCUMENTATION_DEFICIENT | Model, sertifikasi, material kontak, retensi, dan PE belum |
| Socket | Type E/F combo | DOCUMENTATION_DEFICIENT | Kompatibilitas lebih luas, tetapi produk "universal" berisiko |
| Plug | Type F 16 A 3-core | DOCUMENTATION_DEFICIENT | Mating/clamp/PE belum |
| Enclosure | ABS/PC 220x120x70 confirmed (Q06=C), UL94 V-0 | BLOCKED | Material, impact, thermal aging, wall thickness belum; 150x100/180x120 gagal clearance |
| Enclosure | Hammond/Bud rated | PENDING | Perlu ukuran dan rating yang cocok |
| PE hardware | Stud/screw/lock washer | BLOCKED | Safety-critical; belum ada MPN |
| 3D print | PLA/PETG prototype | PROTOTYPE_ONLY | Bukan enclosure listrik tersertifikasi |

## 8. Kesimpulan

1. **Tidak ada BOM final.** Semua baris `PENDING_APPROVAL`, `PROVISIONAL`, `DOCUMENTATION_DEFICIENT`, atau `BLOCKED`.
2. **Target 10 A belum tercapai** oleh relay 8 A. Turunkan rating final atau ubah enclosure/contactor.
3. **PZEM V4 belum dapat diisolasi hanya dari nama modul.** Barrier UART dan pengukuran batch wajib.
4. **Socket/plug/PE/enclosure adalah blocker keselamatan**, bukan item kosmetik.
5. **Harga belum dikumpulkan.** Jangan membeli berdasarkan dokumen ini.
