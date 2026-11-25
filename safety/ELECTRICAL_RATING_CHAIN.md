# Electrical Rating Chain — REV_D_CORE_ONLY

**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW`
**Target pengguna:** **8 A** (amendment 2026-11-15) — **TIDAK DAPAT DIPENUHI** oleh rantai part aktual.
**Rating kontinu provisional:** **6 A** (dibatasi BLX-A fuse holder 6.3 A; belum diuji termal)
**Batas daya provisional:** 6 A × 230 V ≈ **1.380 W**
**Prinsip:** rating akhir = nilai terendah yang dapat dibuktikan dari seluruh rantai, bukan angka target.

## 1. Rantai rating

**REV_D_CORE_ONLY PSU board:** 50 x 65 mm, 2 oz target, 2.5 mm mains traces, TB1/F1/MOV/TCO/TB2, HLK-5M05, 3x JST 5 V. The 6 A provisional path rating and thermal rise are `UNVERIFIED`; see `hardware/psu/README.md`.


| Elemen | Klaim/rencana | Sumber | Derating/ketidakpastian | Status |
|---|---|---|---|---|
| Plug input Type F | DV DIP-2P-16A, 16 A / 250 V, IP44 | Shopee listing + DV datasheet | Kontak/PE/clamp belum diukur | `DOCUMENTATION_DEFICIENT` |
| Kabel input NYYHY 3×1.5 mm² | 16 A class (tergantung instalasi) | Supreme NYYHY; 0.5 m provisional | Bend radius, strain relief, ambient | `PROVISIONAL` |
| Terminal L/N | KF129-2P, 5.08 mm, 300 V / 25 A claim (0 reviews/0 sold) | Shopee listing | Body/retention/rating unverified; Phoenix pad-compatible only | `UNVERIFIED` |
| Fuse | **6.3 A** time-lag, 250 V, Littelfuse 215 series claim | Shopee listing | Breaking capacity/MPN unverified | `PROVISIONAL` |
| Fuse holder | **BLX-A, 6.3 A / 250 V**, 5×20 mm | Shopee/Tayda A-2584 data | Rating limits system to 6 A; pin pitch 21.5 mm unverified | `PROVISIONAL` |
| MOV | 275 VAC class, 10D271K (generic) | Shopee listing | Energy/clamping/end-of-life; 10 mm disc/pitch unmeasured | `UNVERIFIED` |
| Thermal cutoff | Generic 96 °C marking / 99 °C RFT, 10 A / 250 VAC (NOT SF96E) | Shopee listing | Holding 84 °C; marking/dimensions/trip test unverified | `UNVERIFIED` |
| Relay module K1 | 2-channel 5 V optocoupler module, 10 A class claim, two independent SPDT channels, off-board | Handsontec module data | Channel non-linkage, exact contact rating, lifecycle, inrush, active-low behavior | `DOCUMENTATION_DEFICIENT` |
| Terminal output | KF129-2P, 5.08 mm, 300 V / 25 A claim (0 reviews/0 sold) | Shopee listing | Body/retention/rating unverified | `UNVERIFIED` |
| Socket output Type F | DV DSMS-2P-16A, 16 A / 250 V, flange 50×50, fixing 38×38, IP44 | Shopee listing + DV datasheet | Retensi/PE/contact material; depth belum | `DOCUMENTATION_DEFICIENT` |
| PCB carrier | 100×70 SELV carrier; no mains; routed DRC 0 | `hardware/kicad/smartplug.kicad_pcb` | Hanya SELV; belum diuji fisik | `ENGINEERING_REVIEW_REQUIRED` |
| PE path | Kontinu, tidak diputus | Desain konsep | MPN/stud/torsi/uji | `BLOCKED` |

## 2. Perhitungan batas

- Module 2-channel mengklaim 10 A per channel (typical vendor datasheet), tetapi **bukan bukti** rating kontinu assembly.
- **Rating kontinu dibatasi fuse holder BLX-A 6.3 A.** Fuse 6.3 A dan holder 6.3 A; target 8 A tidak dapat diklaim.
- Rating provisional 6 A; thermal test wajib. Jika temperature rise melebihi batas engineer, rating turun lagi.
- Derating awal: holder 6.3 A × ~0.95 = **6 A**; ini batas komponen, bukan hasil uji. Module 10 A claim tidak menaikkan batas.
- Dua channel tidak mechanically linked; satu channel weld dapat meninggalkan konduktor lain. Ini residual risk, bukan klaim DPST.
- Jangan memberi label "10 A", "16 A", atau "DPST safety" pada modul ini.

## 3. Beban dan inrush

Q04=B (campuran elektronik/SMPS) berarti:
- Batas eksplisit provisional: **6 A kontinu, ~1.380 W, elektronik/SMPS rumah tangga** (dibatasi holder 6.3 A).
- Adaptor SMPS dapat memiliki inrush kapasitif tinggi.
- Module 10 A class belum otomatis cocok untuk inrush SMPS.
- Perlu datasheet contact category, inrush test, dan lifecycle.
- Beban motor/induktif/pemanas tidak dijanjikan.
- Kontak relay dapat weld; firmware tidak boleh mengklaim OFF fisik tanpa feedback.

## 4. Koordinasi (ringkas)

1. Fuse 6.3 A melindungi kabel/terminal dari short circuit, bukan module relay dari overload kecil; holder 6.3 A dan fuse 6.3 A harus koheren.
2. Thermal cutoff independen memutus L jika hotspot melebihi trip; posisi dan rating harus diuji.
3. MOV membatasi transient; koordinasi dengan fuse dan thermal cutoff harus dihitung.
4. Software overcurrent (jika ada) hanya supplementary; tidak menggantikan fuse/thermal cutoff.
5. PE tidak boleh melalui fuse/relay/PCB trace sebagai satu-satunya jalur.

## 5. Bukti yang diperlukan sebelum rating dikunci

- [ ] Datasheet exact module relay, fuse, holder, terminal, socket, plug, PSU.
- [ ] Perhitungan time-current dan breaking capacity.
- [ ] Pengukuran temperature rise module/terminal/fuse pada 4 A, 6 A, dan overload terkendali di lab.
- [ ] Uji inrush SMPS.
- [ ] Uji lifecycle kontak tiap channel.
- [ ] Review engineer kompeten.
- [ ] Label final 6 A/1.380 W berdasarkan bukti.

**Kesimpulan:** `BLOCKED` untuk fabrikasi/penggunaan. Target 8 A tidak dapat dipenuhi oleh holder 6.3 A; rating provisional 6 A adalah batas komponen, bukan sertifikasi. Thermal/lifecycle/PE/isolation tetap wajib diuji.
