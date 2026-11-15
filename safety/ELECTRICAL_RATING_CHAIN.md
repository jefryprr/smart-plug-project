# Electrical Rating Chain — REV_A_PROVISIONAL

**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW`
**Rating final yang dipilih pengguna:** **8 A** (amendment 2026-11-15)
**Batas daya:** 8 A × 230 V ≈ **1.840 W**
**Rating kontinu provisional:** **8 A** (belum diuji termal)
**Prinsip:** rating akhir = nilai terendah yang dapat dibuktikan dari seluruh rantai, bukan angka target.

## 1. Rantai rating

| Elemen | Klaim/rencana | Sumber | Derating/ketidakpastian | Status |
|---|---|---|---|---|
| Plug input Type F | 16 A / 250 V class | MPN belum dipilih | Kontak/PE/clamp belum diukur | `UNVERIFIED` |
| Kabel input H05VV-F 3×1.5 mm² | 16 A class (tergantung instalasi) | Standar kabel; panjang belum final | Bend radius, strain relief, ambient | `UNVERIFIED` |
| Terminal L/N | 10 A class (rencana) | MPN belum final | Torsi, ferrule, creepage | `UNVERIFIED` |
| Fuse | 10 A time-lag, 250 V | Littelfuse 215 series | Breaking capacity, holder, koordinasi | `PENDING` |
| MOV | 275 VAC class | EPCOS S10K275 | Energy/clamping/end-of-life | `PENDING` |
| Thermal cutoff | 99 °C, 10 A / 250 V | Sefuse SF169E | Batch datasheet, holding current | `DOCUMENTATION_DEFICIENT` |
| Relay module K1 | 2-channel 5 V optocoupler module, 10 A class claim, two independent SPDT channels, off-board | Handsontec/DigiKey module data | Channel non-linkage, exact contact rating, lifecycle, inrush, active-low behavior | `DOCUMENTATION_DEFICIENT` |
| Terminal output | 10 A class | MPN belum final | Torsi/creepage | `UNVERIFIED` |
| Socket output Type F | 16 A / 250 V class | MPN belum dipilih | Retensi/PE/contact material | `UNVERIFIED` |
| PCB carrier | Tidak membawa mains | Desain off-board | Hanya SELV | `PROVISIONAL` |
| PE path | Kontinu, tidak diputus | Desain konsep | MPN/stud/torsi/uji | `BLOCKED` |

## 2. Perhitungan batas

- Module 2-channel mengklaim 10 A per channel (typical vendor datasheet), tetapi **bukan bukti** rating kontinu assembly.
- Fuse 10 A **tidak** menaikkan rating kontinu; fuse adalah backup.
- Rating final 8 A dipilih pengguna; thermal test wajib. Jika temperature rise melebihi batas engineer, rating turun.
- Derating awal: 10 A module × 0.8 = **8 A** pada ambient yang disetujui, sebelum koreksi enclosure. Ini asumsi, bukan hasil uji.
- Dua channel tidak mechanically linked; satu channel weld dapat meninggalkan konduktor lain. Ini residual risk, bukan klaim DPST.
- Jangan memberi label "10 A" atau "DPST safety" pada modul ini.

## 3. Beban dan inrush

Q04=B (campuran elektronik/SMPS) berarti:
- Batas eksplisit: **8 A kontinu, ~1.840 W, elektronik/SMPS rumah tangga**.
- Adaptor SMPS dapat memiliki inrush kapasitif tinggi.
- Module 10 A class belum otomatis cocok untuk inrush SMPS.
- Perlu datasheet contact category, inrush test, dan lifecycle.
- Beban motor/induktif/pemanas tidak dijanjikan.
- Kontak relay dapat weld; firmware tidak boleh mengklaim OFF fisik tanpa feedback.

## 4. Koordinasi (ringkas)

1. Fuse 10 A melindungi kabel/terminal dari short circuit, bukan module relay dari overload kecil.
2. Thermal cutoff independen memutus L jika hotspot melebihi trip; posisi dan rating harus diuji.
3. MOV membatasi transient; koordinasi dengan fuse dan thermal cutoff harus dihitung.
4. Software overcurrent (jika ada) hanya supplementary; tidak menggantikan fuse/thermal cutoff.
5. PE tidak boleh melalui fuse/relay/PCB trace sebagai satu-satunya jalur.

## 5. Bukti yang diperlukan sebelum rating dikunci

- [ ] Datasheet exact module relay, fuse, holder, terminal, socket, plug, PSU.
- [ ] Perhitungan time-current dan breaking capacity.
- [ ] Pengukuran temperature rise module/terminal/fuse pada 6.4 A, 8 A, dan overload terkendali di lab.
- [ ] Uji inrush SMPS.
- [ ] Uji lifecycle kontak tiap channel.
- [ ] Review engineer kompeten.
- [ ] Label final 8 A/1.840 W berdasarkan bukti.

**Kesimpulan:** `BLOCKED` untuk fabrikasi/penggunaan. Rating 8 A adalah keputusan pengguna, bukan hasil sertifikasi; thermal/lifecycle/PE/isolation tetap wajib diuji.
