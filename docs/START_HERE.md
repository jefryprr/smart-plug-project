# Mulai di Sini — Panduan untuk Semua Orang

**Proyek:** SMART PLUG PROJECT  
**Revisi desain:** `REV_C_PSU_BOARD`  
**Status:** prototipe digital, `ENGINEERING_REVIEW_REQUIRED`, `NOT_FOR_FABRICATION`

Dokumen ini dibuat untuk orang yang **bukan engineer** tetapi ingin memahami proyek ini tanpa tersesat di ratusan file.

---

## 1. Dalam satu paragraf

SMART PLUG PROJECT adalah rancangan colokan listrik pintar berbasis ESP32-S3. Alat ini dirancang untuk mengukur pemakaian listrik, menyalakan atau mematikan beban dari jarak jauh, membuat jadwal, dan menampilkan data di web atau Android. Repo ini berisi seluruh proses desainnya: riset komponen, daftar belanja, gambar rangkaian, PCB, kabel, casing 3D, firmware, server, aplikasi, simulator, dan analisis keselamatan.

**Yang penting:** ini masih **prototipe digital**. Belum ada alat fisik yang dirakit atau dinyalakan dengan 230 VAC. Jangan menganggapnya produk jadi atau aman digunakan.

---

## 2. Tiga hal yang harus dipahami lebih dulu

### a. Listrik 230 VAC itu berbahaya

Bagian yang tersambung ke colokan listrik disebut **mains**. Bagian ini bisa mematikan. Bagian ESP32, layar, dan tombol disebut **SELV** (tegangan rendah yang dirancang terpisah dari mains). Mencampur keduanya tanpa isolasi yang benar bisa membuat bagian yang seharusnya aman menjadi bertegangan tinggi.

Karena itu repo ini punya banyak dokumen keselamatan. Bukan karena bertele-tele, tetapi karena kesalahan kecil di mains bisa berakibat fatal.

### b. “Ada file” bukan berarti “sudah terbukti”

Repo ini punya PCB, Gerber, casing 3D, dan firmware. Itu semua adalah **artefak digital**. Belum berarti:

- PCB sudah dicetak dan diuji;
- casing sudah dicetak dan dipasang;
- firmware sudah di-flash ke board asli;
- alat sudah diuji beban 8 A;
- isolasi sudah diuji hipot;
- PE sudah diuji kesinambungannya.

Status yang dipakai proyek ini membedakan hal-hal tersebut. Lihat [`PROJECT_STATUS.md`](PROJECT_STATUS.md).

### c. Ada dua dunia: hardware dan software

- **Software** (API, web, Android, simulator, firmware core) bisa diuji di komputer. Banyak yang sudah PASS.
- **Hardware** (mains, thermal, PE, isolasi, beban) hanya bisa dibuktikan dengan alat fisik dan lab. Semua masih BLOCKED.

Jangan mencampur “test software PASS” dengan “alat aman dipakai”.

---

## 3. Pilih jalur bacaan Anda

### Saya ingin tahu cara kerjanya

1. [`../README.id.md`](../README.id.md) — ringkasan proyek.
2. [`ARCHITECTURE.md`](ARCHITECTURE.md) — diagram dan alur data.
3. [`HARDWARE_GUIDE.md`](HARDWARE_GUIDE.md) — komponen dan PCB.
4. [`SOFTWARE_GUIDE.md`](SOFTWARE_GUIDE.md) — API, web, Android, MQTT.
5. [`GLOSSARY.md`](GLOSSARY.md) — istilah teknis.

### Saya ingin menjalankan demonya

1. [`SOFTWARE_GUIDE.md`](SOFTWARE_GUIDE.md) — cara menjalankan API dan web.
2. [`TESTING.md`](TESTING.md) — cara menjalankan tes.
3. [`../docs/tutorials/16_LOCAL_MOCK_TEST.md`](tutorials/16_LOCAL_MOCK_TEST.md) — simulasi tanpa hardware.

### Saya ingin melihat hardware

1. [`HARDWARE_GUIDE.md`](HARDWARE_GUIDE.md) — gambaran board dan konektor.
2. [`../hardware/psu/README.md`](../hardware/psu/README.md) — PCB PSU 230 VAC → 5 V.
3. [`../hardware/kicad/README.md`](../hardware/kicad/README.md) — carrier SELV.
4. [`../hardware/wiring/README.md`](../hardware/wiring/README.md) — harness kabel.
5. [`../bom/BOM_MASTER.md`](../bom/BOM_MASTER.md) — daftar komponen.

### Saya ingin memahami keselamatan

1. [`SAFETY.md`](SAFETY.md) — ringkasan bahaya dan aturan.
2. [`../safety/ISOLATION_PLAN.md`](../safety/ISOLATION_PLAN.md) — batas isolasi.
3. [`../safety/RESIDUAL_RISK_REGISTER.csv`](../safety/RESIDUAL_RISK_REGISTER.csv) — risiko yang masih tersisa.
4. [`../safety/REVIEW_SIGNOFF_TEMPLATE.md`](../safety/REVIEW_SIGNOFF_TEMPLATE.md) — apa yang harus ditandatangani engineer.

### Saya ingin berkontribusi

1. [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — aturan kontribusi.
2. [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) — perilaku komunitas.
3. [`../SECURITY.md`](../SECURITY.md) — melaporkan masalah keamanan.

---

## 4. Istilah yang sering muncul

| Istilah | Arti sederhana |
|---|---|
| **Mains** | Listrik 230 VAC dari colokan. Berbahaya. |
| **SELV** | Bagian tegangan rendah yang dirancang terpisah dari mains. |
| **Isolasi galvanik** | Tidak ada jalur listrik langsung antara dua sisi; data/daya menyeberang lewat medan magnet atau cahaya. |
| **Creepage / clearance** | Jarak minimum di permukaan PCB/udara agar listrik tidak melompat. |
| **Hipot** | Uji tegangan tinggi untuk memeriksa isolasi. |
| **PE** | Protective Earth, kabel ground pengaman. Tidak boleh diputus. |
| **TCO** | Thermal cutoff, sekring suhu sekali pakai. |
| **MOV** | Varistor untuk menahan lonjakan tegangan. |
| **PTC** | Sekring arus yang naik resistansinya saat panas. |
| **TVS** | Dioda penahan lonjakan tegangan. |
| **PZEM** | Modul pengukur energi listrik. |
| **CT** | Current transformer, penjepit arus. |
| **UART** | Jalur komunikasi serial TX/RX. |
| **MQTT** | Protokol pesan ringan untuk IoT. |
| **API** | Pintu masuk data/aplikasi lewat HTTP. |
| **HIL** | Hardware-in-the-loop, uji dengan hardware asli. |
| **BOM** | Bill of Materials, daftar komponen. |
| **ADR** | Architecture Decision Record, catatan keputusan desain. |

Daftar lengkap: [`GLOSSARY.md`](GLOSSARY.md).

---

## 5. Status proyek secara jujur

**Sudah lolos secara digital:**

- 34 tes domain, 11 tes MQTT, 38 tes API, 4 tes simulator.
- 75 pemeriksaan firmware core; build ESP-IDF v6.1.
- Build web + 5 tes Playwright + axe.
- KiCad ERC 0; carrier DRC 0/0; PSU DRC 0/0; Gerber provisional.
- WireViz 3 harness; CadQuery STEP/STL; static wiring/GPIO/BOM crosscheck.

**Belum dan tidak boleh diklaim:**

- Alat fisik sudah dirakit.
- Sudah dinyalakan dengan 230 VAC.
- Isolasi/hipot/leakage lulus.
- PE continuity lulus.
- Thermal 8 A lulus.
- Firmware sudah di-flash dan terintegrasi.
- Android sudah diuji di HP.
- PostgreSQL/Docker/TLS produksi sudah jalan.
- SNI/CE/UL atau siap jual.

Angka dan log lengkap: [`PROJECT_STATUS.md`](PROJECT_STATUS.md), [`../reports/VALIDATION_SUMMARY.json`](../reports/VALIDATION_SUMMARY.json), [`../reports/FAILURES.md`](../reports/FAILURES.md).

---

## 6. Aturan emas

1. **Jangan menyambungkan 230 VAC** ke prototipe ini.
2. **Jangan bekerja sendirian** dengan mains.
3. **Jangan memutus PE.**
4. **Jangan menganggap mock/simulator sebagai uji fisik.**
5. **Jangan mencetak label rating atau logo sertifikasi.**
6. **Jangan mengirim Gerber provisional ke pabrik** sebagai board fungsional.
7. **Jangan menyimpan secret** di repo, log, atau screenshot.

Kalau Anda hanya ingin belajar software, tidak perlu menyentuh hardware sama sekali. Mulai dari [`SOFTWARE_GUIDE.md`](SOFTWARE_GUIDE.md).
