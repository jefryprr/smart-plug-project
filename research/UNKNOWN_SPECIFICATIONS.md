# Unknown Specifications — REV_D_CORE_ONLY

**Status:** `OPEN`
**Aturan:** Nilai di bawah tidak boleh diisi dengan tebakan. Setiap unknown harus ditutup dengan datasheet, pengukuran, atau keputusan engineer. Selama terbuka, artefak terkait tetap `PROVISIONAL`/`BLOCKED`.

| ID | Area | Unknown | Dampak | Cara menutup |
|---|---|---|---|---|
| U-001 | MCU board | Revisi fisik ESP32-S3-DevKitC-1 (v1.0/v1.1/clone), GPIO RGB, regulator; header **row spacing 22.86 mm and 1x22 layout verified from official v1.1 DXF** | GPIO map, footprint, boot-safe, LED | Foto depan-belakang, marking, pengukuran sample, cek dokumen Espressif |
| U-002 | MCU board | Konsumsi arus Wi-Fi peak dan inrush | Power budget, PSU, decoupling | Pengukuran dengan USB meter/scope |
| U-003 | PZEM | Batch/V4 asli, pinout, level UART, baud/parity, CRC, register, isolasi, CT ratio, dimensi | Metering, isolasi, firmware driver, space | Manual batch, pengukuran, inspeksi, uji isolated supply |
| U-004 | PZEM | Rating terminal tegangan dan current path | Rating chain, clearance | Datasheet batch dan inspeksi |
| U-005 | Relay | MPN/coil voltage/contact arrangement/rating UL-IEC/lifecycle RT444005 | Rating output, thermal, safety | Datasheet exact MPN, sample, lifecycle data |
| U-006 | Relay | Inrush/inductive capability untuk beban Q04=B | Switching endurance, contact welding | Datasheet category, uji lab |
| U-007 | Socket/plug | MPN, sertifikasi, material kontak, retensi, PE, dimensi | Q02, PE, mechanical, regulatory | Pilih produk terlacak; ukur dan uji retensi |
| U-008 | PSU | HLK-5M05 batch certificate, actual isolation/leakage, creepage, thermal derating, ripple/startup | Isolation, thermal, safety | Batch datasheet + hipot/thermal/load test |
| U-009 | Fuse | Breaking capacity, time-current, holder rating, coordination | Overcurrent protection | Datasheet dan perhitungan koordinasi |
| U-010 | MOV | Clamping voltage, energy, end-of-life, thermal fuse coordination | Surge protection | Surge study dan datasheet |
| U-011 | Thermal cutoff | Trip temperature, holding current, AC rating, batch approval | Thermal protection | Datasheet batch dan uji trip |
| U-012 | Clearance/creepage | Pollution degree, overvoltage category, material group, working voltage, altitude | Isolation, PCB/enclosure layout | IEC 60664-1 worksheet + engineer sign-off |
| U-013 | PE | MPN stud/terminal, torsi, kontinuitas, vibration | PE safety | Pilih part, uji kontinuitas dan getaran |
| U-014 | Enclosure | Material (ABS/PC/FR), UL94 rating, wall thickness, impact, thermal aging | Fire/mechanical safety | Pilih enclosure rated; review material |
| U-015 | Cable | Panjang final, derating, bend radius, strain relief | Thermal/mechanical | Perhitungan dan uji tarik |
| U-016 | PCB | Stackup, copper thickness, trace width, via current, clearance | Thermal, DRC | Perhitungan arus/termal dan DRC KiCad |
| U-017 | Display | Controller SSD1306 vs SH1106, address, dimensi, viewport | UI, firmware | Inspeksi modul dan datasheet |
| U-018 | RTC | Drift, backup runtime, battery/supercap selection | Offline schedule | Datasheet dan uji drift |
| U-019 | Cost | Harga/stock/ongkir semua komponen | BOM, budget | Snapshot 2026-11-15 ada di `bom/BOM_PROCUREMENT.csv`; ongkir/pajak aktual dan stok saat beli masih UNKNOWN |
| U-020 | Test lab | Tidak ada multimeter/lab (Q26=A) | Semua uji fisik | Sediakan alat dan personel kompeten |
| U-021 | Regulatory | Klasifikasi SNI/IEC, lab, label, sertifikasi | Klaim pasar | Konsultasi lembaga/regulatory specialist |
| U-022 | Firmware toolchain | ESP-IDF belum terpasang; versi target belum dipilih | Build/OTA/security | Pasang versi stabil, lock, build |
| U-023 | KiCad | KiCad CLI tidak terpasang | ERC/DRC/Gerber | Pasang KiCad versi terkunci; jalankan ERC/DRC |
| U-024 | Android | Android SDK tidak terpasang; APK belum dibuat | Build APK | Pasang SDK, build, uji emulator |
| U-025 | Push notification | FCM/Expo credentials belum ada | Android push | Akun/credential dan izin |
| U-026 | Deployment | VPS/domain/TLS belum ada | Production deploy | Infrastruktur dan izin pengguna |
| U-027 | MCU | Board N16R8 compatible vs official Espressif; regulator/RGB/strapping/RF belum diukur | GPIO, firmware, safety | Foto, pinout, RF, dan uji beban |
| U-028 | Enclosure | MG Duradus ABS IP65; flame rating/UL94 belum ada | Fire/mechanical safety | Sertifikat material + thermal/impact test |
| U-029 | Isolation | PZEM internal optocoupler creepage/hipot; no external ADuM/B0505S | Isolation safety | Hipot/leakage + creepage review |
| U-030 | Thermal | No temperature sensor in REV_D_CORE_ONLY; TCO/fuse only | Thermal safety | Thermal test + TCO batch data |
| U-031 | UART | PZEM 5V TX divider and 74HCT125 RX drive levels | UART reliability | Bench 9600-baud test |

## Aturan penutupan

1. Satu unknown = satu bukti (datasheet, foto, pengukuran, atau keputusan engineer).
2. Perubahan pada U-003/U-005/U-007/U-012/U-014 wajib memicu impact analysis pada BOM, schematic, PCB, CAD, wiring, dan firmware.
3. Unknown safety-critical tidak boleh ditutup dengan asumsi "kemungkinan aman".
