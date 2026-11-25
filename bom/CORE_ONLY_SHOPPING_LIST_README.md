# CORE-Only Shopping List — REV_D_CORE_ONLY

**File CSV (aktual):** `CORE_ONLY_SHOPEE_SHOPPING_LIST.csv`  
**File ini (estimasi lama):** `CORE_ONLY_SHOPPING_LIST.csv`  
**Board:** ESP32-S3-DevKitC-1 N16R8 **v1.0** (onboard RGB **GPIO48**)  
**Build:** CORE-only — tanpa OLED, RTC, atau RGB eksternal.

> **PENTING (2026-11-24):** Yang dipakai untuk belanja adalah **`CORE_ONLY_SHOPEE_SHOPPING_LIST.csv`**. File ini adalah daftar estimasi lama. Hardware aktual memakai fuse holder **BLX-A 6.3 A**, fuse **6.3 A**, TCO generik 96 °C, dan terminal **KF129-2P**; baris lama sudah diperbarui, tetapi CSV Shopee tetap sumber utama.

## Cara pakai

1. Buka CSV di Excel/LibreOffice/Google Sheets.
2. Isi kolom **link_pembelian** dengan URL toko pilihan Anda.
3. Isi **vendor_dipilih**, **status_beli**, **qty_diterima**, dan **tanggal_beli** saat berbelanja.
4. Jangan mengubah **qty_pakai** tanpa mengubah desain; itu jumlah yang terpasang.
5. **qty_beli** sudah termasuk pack/spare minimum. Untuk PCB, qty_beli 5 pcs karena batch fabrikasi; 1 dipakai, sisanya cadangan.
6. Harga adalah estimasi/listing, bukan quote. Perbarui harga aktual setelah checkout.

## Arti kolom

| Kolom | Arti |
|---|---|
| `no` | Nomor baris |
| `kategori` | Kelompok barang |
| `nama_barang` | Nama barang |
| `spesifikasi_singkat` | Spesifikasi penting |
| `qty_pakai` | Jumlah yang benar-benar dipasang |
| `qty_beli` | Jumlah yang perlu dibeli, termasuk spare/pack |
| `satuan` | pcs, pack, m, set, sesi |
| `referensi` | Designator/BOM line |
| `fungsi_singkat` | Fungsi dalam bahasa sederhana |
| `prioritas` | WAJIB / DISARANKAN / OPSIONAL / JASA_LAB |
| `safety_critical` | YA jika menyangkut mains/PE/isolasi/keselamatan |
| `status_harga` | VERIFIED_LISTING / ESTIMATED / UNKNOWN / JASA |
| `harga_satuan_estimasi_idr` | Harga satuan estimasi |
| `harga_total_estimasi_idr` | qty_beli x harga satuan |
| `link_pembelian` | **Isi sendiri** |
| `vendor_dipilih` | **Isi sendiri** |
| `status_beli` | BELUM / DIPESAN / DITERIMA |
| `qty_diterima` | **Isi saat barang datang** |
| `tanggal_beli` | **Isi sendiri** |
| `catatan` | Peringatan/verifikasi |

Kolom tambahan yang disarankan jika ingin lebih rapi: `nomor_invoice`, `batch_lot`, `tanggal_terima`, `kondisi_barang`, `catatan_inspeksi`.

## Ringkasan estimasi

| Kelompok | Estimasi |
|---|---:|
| WAJIB | Rp818,932 |
| DISARANKAN | Rp46,000 |
| OPSIONAL | Rp5,000 |
| JASA_LAB | Rp0 |
| **Total aktif** | **Rp869,932** |

Angka ini **bukan quote** dan belum termasuk pajak/ongkir. Dihitung dari `CORE_ONLY_SHOPPING_LIST.csv` (83 baris, 80 baris aktif) pada 2026-11-20.

Untuk daftar Shopee `CORE_ONLY_SHOPEE_SHOPPING_LIST.csv` (85 baris, 78 baris aktif): WAJIB **Rp635,060**, DISARANKAN **Rp5,500**, OPSIONAL **Rp0**, total aktif **Rp640,560** sebelum ongkir. Perbedaannya berasal dari baris PCB/tools dan tautan toko yang tidak ada di daftar Shopee.

Catatan penting:
- Total WAJIB di atas memakai **5 pcs PCB carrier + 5 pcs PCB PSU**, 1 m kabel mains, fuse cadangan, dan spare screw. BOM CORE Rp754.016 adalah **biaya per unit/share marketplace** (Rp794.016 all-in dengan ongkir), bukan total belanja 5 PCB.
- Tools dengan harga `UNKNOWN` dan seluruh `JASA_LAB` **belum dihitung** dalam total di atas.
- Jika hanya ingin 1 pcs PCB masing-masing, kurangi 4 pcs dari setiap baris PCB (harga per pcs 15.000).
- Untuk menghemat: beli CORE inti dulu, tunda tools yang sudah dimiliki, dan jangan membeli OLED/RTC/RGB eksternal.

## Yang tidak perlu dibeli di CORE-only

- OLED dan kabelnya
- DS3231/RTC dan kabelnya
- RGB eksternal/WS2812, resistor 330 Ω, kabel JST 3-pin
- Pullup I2C 4.7 kΩ
- ADuM1201 + B0505S (tidak dipakai di REV_D)
- TMP102 (sudah dihapus)

Onboard RGB DevKitC-1 v1.0 sudah tersedia di board; tidak perlu LED tambahan. M12 vent, nylon standoff M3x12, dan plate HLK tidak dipakai pada enclosure baru. Socket DV DSMS-2P-16A adalah surface socket; perlu 4 baut M4x16 (row 28a).

## Jangan dihapus/downgrade

Jangan menghapus atau menurunkan:
- fuse 10 A, MOV, TCO 99 °C
- PE stud/terminal
- terminal block mains
- rating relay
- isolasi PSU/PZEM
- enclosure barrier, gasket, strain relief (vent deferred; no vent hole)
- label prototipe

Barang-barang ini **safety-critical**. Menghapusnya bisa menambah biaya review/lab dan risiko keselamatan.

## Batas keselamatan

Ini masih prototipe digital. Jangan menyambungkan 230 VAC, jangan fabrikasi sebagai board fungsional, dan jangan mengklaim aman/siap pakai tanpa review engineer dan uji lab. Semua item mains/PSU tetap `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`.
