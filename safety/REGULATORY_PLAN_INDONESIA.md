# Regulatory Plan — Indonesia (Provisional)

**Status:** `RESEARCH_REQUIRED`
**Penting:** Dokumen ini bukan nasihat hukum/regulasi dan bukan klaim sertifikasi. Klasifikasi produk, SNI, dan persyaratan lab harus dikonfirmasi kepada lembaga/regulatory specialist yang berwenang.

## 1. Klasifikasi yang belum pasti

Produk saat ini adalah **prototipe akademik** (Q12=A), bukan produk konsumen. Jika kelak dipasarkan:
- Apakah termasuk aksesori listrik rumah tangga (plug/socket-outlet), perangkat elektronik rumah tangga, atau produk IoT dengan catu daya eksternal?
- Apakah perlu SNI wajib, sertifikasi keselamatan, EMC, dan label?
- Apakah plug/socket Type F yang dijual di Indonesia harus memenuhi IEC 60884-1 dan/atau SNI tertentu?
- Apakah produk dengan relay 230 VAC dan PZEM memerlukan pengujian lab tertentu?

Jawaban belum tersedia. Jangan mengklaim "SNI ready", "siap dijual", atau "tersertifikasi".

## 2. Standar yang perlu ditinjau

| Standar | Relevansi | Status |
|---|---|---|
| IEC 60884-1:2022 | Plugs and socket-outlets rumah tangga/serupa | `APPLICABILITY_UNKNOWN` |
| IEC 60664-1:2020 + Amd 1:2025 | Koordinasi isolasi (clearance/creepage) | `REQUIRED_FOR_DESIGN` |
| IEC 61058-1:2026 | Switches for appliances | `APPLICABILITY_UNKNOWN` |
| IEC 60335-1 | Household appliances safety (mungkin relevan) | `APPLICABILITY_UNKNOWN` |
| IEC 61000-6-x / CISPR | EMC/emisi/imunitas | `APPLICABILITY_UNKNOWN` |
| IEC 61010-1 | Measurement/control/laboratory equipment (mungkin) | `APPLICABILITY_UNKNOWN` |
| Standar relay/fuse/PSU/enclosure | Komponen dan koordinasi | `COMPONENT_SPECIFIC` |
| SNI terkait | Wajib/tidak, edisi, lab | `RESEARCH_REQUIRED` |

## 3. Persyaratan yang mungkin

### 3.1 Keselamatan listrik
- Clearance/creepage, solid insulation, dielectric strength.
- PE continuity, touch protection, strain relief.
- Temperature rise, abnormal operation, short circuit.
- Material flammability (enclosure/PCB).
- Rating label dan warning.

### 3.2 EMC
- Emisi konduktif/radiasi (PSU, relay, ESP32).
- Imunitas (ESD, surge, burst).
- Pengujian di lab EMC terakreditasi.

### 3.3 Lingkungan
- RoHS, WEEE (jika berlaku).
- Kemasan/label.

### 3.4 Radio
- ESP32-S3 Wi-Fi/BLE: modul dengan sertifikasi radio; produk akhir mungkin perlu notifikasi/sertifikasi.
- Jangan mengklaim sertifikasi radio hanya karena modul memiliki sertifikat.

## 4. Rencana tindakan

1. Tentukan klasifikasi produk dan skenario penggunaan (rumah tangga, laboratorium, komersial).
2. Konsultasi regulator/lab Indonesia untuk SNI dan sertifikasi yang berlaku.
3. Susun test plan berdasarkan standar yang benar, bukan daftar nomor tebakan.
4. Lakukan pre-compliance/internal test dengan lab kompeten.
5. Perbaiki desain, ulangi uji.
6. Siapkan dokumen teknis, label, manual, dan declaration.
7. Jangan menjual/mengklaim sebelum sertifikat/izin yang relevan diperoleh.

## 5. Label (provisional)

Label harus memuat:
- Nama/model, nomor seri.
- Rating tegangan/arus/frekuensi (dari rating chain, bukan target).
- Jenis beban yang diizinkan.
- Peringatan: bukan pengganti MCB/RCD; jangan buka; jangan gunakan di luar rating; PE harus terhubung.
- Simbol PE dan peringatan listrik.
- QR pairing tidak boleh berisi secret yang dapat dipakai ulang.
- Tanggal/revisi.

**Status:** `BLOCKED`. Konten final menunggu rating dan review regulatory.
