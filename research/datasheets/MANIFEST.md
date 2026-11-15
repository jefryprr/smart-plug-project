# Datasheet Manifest — REV_A_PROVISIONAL

**Diperiksa:** 15 November 2026
**Aturan:** PDF resmi yang tersedia disimpan lokal dan di-hash. Jika unduhan gagal atau tidak resmi, hanya tautan yang dicatat dan statusnya `LINK_ONLY`/`DOCUMENTATION_DEFICIENT`. Halaman distributor bukan pengganti datasheet.

## Tersimpan lokal

| File | Sumber | Ukuran (byte) | SHA-256 | Revisi | Catatan |
|---|---|---:|---|---|---|
| `esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf` | https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf | 1.280.501 | `27D71971DA07C280C6068D08C74720D1A25B8F20CF8494DC1765BDD28D40D435` | UNKNOWN | Modul WROOM-1; bukan bukti revisi board DevKitC-1 |
| `meanwell_irm-05.pdf` | https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.PDF | 146.389 | `8E13F9373A39D8E0D92D540082CB97A9F3172111EA749B807AF96DB9E27D878A` | UNKNOWN | PSU 5 V 1 A |
| `ti_tmp102.pdf` | https://www.ti.com/lit/ds/symlink/tmp102.pdf | 1.151.760 | `C9DA6620EF95F75CE94372F670A84D168E05922DD32CEBFAA6517083F15EBFAF` | UNKNOWN | Sensor suhu |
| `microchip_mcp9808.pdf` | https://ww1.microchip.com/downloads/en/DeviceDoc/MCP9808-0.5C-Maximum-Accuracy-Digital-Temperature-Sensor-Data-Sheet-DS20005095B.pdf | 1.831.079 | `E7B6502F744C3E605A424D7B784A23BAA471A41F8BC6D51F6321027B0C43972F` | UNKNOWN | Alternatif sensor |
| `mornsun_b0505s-1wr3.pdf` | https://www.mornsun-power.com/html/pdf/B0505S-1WR3.html | 38.277 | `A6833229AE0DF1C68CBF9812AFF477B5214254C0513B5DA53241D44E5C9EE2AE` | UNKNOWN | Isolated DC/DC |
| `te_rt2.pdf` | https://www.mouser.com/datasheet/2/418/9/ENG_DS_RT2_3-576697.pdf | 13.897 | `1E61EB9D070BF58B3BD65A04CBBDA078C68D37AA36611FDF814D788358191290` | UNKNOWN | Relay RT2; bukan bukti exact MPN/coil |
| `omron_b3f.pdf` | https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3f.pdf | 711.882 | `BE9CF69E5F43FB7689448A2097C19858E5643C0E2E49CD77D018881543E27A1F` | UNKNOWN | Tombol |
| `ti_sn74ahct1g125.pdf` | https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf | 1.253.856 | `564B239F73FF629F960832FA7E1C64F6A651EEA28F64115ECEFCDB7AF22CA416` | UNKNOWN | Level shifter |
| `vishay_1n4007.pdf` | https://www.vishay.com/docs/88503/1n4001.pdf | 74.632 | `56A77C6615C90C11993D37D94E67F335CF3A2D1FE00F25D2A1A4833834356D07` | UNKNOWN | Flyback diode |

## Link-only / belum tersimpan

| Dokumen | URL | Status | Alasan |
|---|---|---|---|
| ESP32-S3-DevKitC-1 v1.1 user guide | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html | `LINK_ONLY` | HTML resmi; revisi board harus diverifikasi fisik |
| ESP32-S3-DevKitC-1 v1.0 user guide | https://documentation.espressif.com/api/resource/path/docs/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html | `LINK_ONLY` | Perbedaan RGB GPIO48 vs GPIO38 |
| ADuM1201 | https://www.analog.com/media/en/technical-documentation/data-sheets/ADuM1200_1201.pdf | `LINK_ONLY` | Unduhan timeout; tautan resmi |
| DS3231M | https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231M.pdf | `LINK_ONLY` | Unduhan timeout |
| TDK SIOV varistor | https://www.tdk-electronics.tdk.com/inf/70/db/varistors/leaded_sio_v_series.pdf | `LINK_ONLY` | URL 404 saat diakses; cari halaman produk resmi |
| PZEM-004T V4 | https://github.com/im-0/pzem-004t-original-docs | `DOCUMENTATION_DEFICIENT` | Arsip historis, bukan manual batch V4 yang dibeli |
| PZEM retailer 1 | https://www.easyware.co.id/product/peacefair-pzem-004t-v4-ac-power-energy-meter-uart-modbus-original/ | `AVAILABILITY_ONLY` | Bukan datasheet |
| PZEM retailer 2 | https://store.easyware.id/produk/peacefair-pzem-004t-v40-modul-energy-meter-ac-80-260v-10a-100a-ct-split-ct-ttl-modbus-arduino-esp32/ | `AVAILABILITY_ONLY` | Bukan datasheet |
| IEC 60884-1:2022 | https://webstore.iec.ch/en/publication/34175 | `LICENSED` | Dokumen berbayar; jangan reproduksi tanpa lisensi |
| IEC 60664-1:2020 | https://webstore.iec.ch/en/publication/59671 | `LICENSED` | Dokumen berbayar |
| IEC 60664-1:2025 amendment | https://webstore.iec.ch/en/publication/80714 | `LICENSED` | Dokumen berbayar |
| IEC 61058-1:2026 | https://webstore.iec.ch/en/publication/85002 | `LICENSED` | Dokumen berbayar |

## Catatan

- Hash di atas dihitung dari file yang benar-benar diunduh pada tanggal tersebut.
- PDF dapat direvisi pabrikan tanpa mengubah nama file; selalu catat tanggal akses dan revisi.
- Untuk PZEM, socket, enclosure, dan thermal cutoff, **tidak ada dokumen pabrikan batch** yang cukup. Statusnya tetap `DOCUMENTATION_DEFICIENT`.
- Jangan mengunduh/mereproduksi standar IEC berbayar tanpa lisensi.
