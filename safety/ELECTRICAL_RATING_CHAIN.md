# Electrical Rating Chain — REV_A_PROVISIONAL

**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW`
**Target pengguna:** 10 A (Q03=B)
**Rating kontinu provisional:** **8 A atau lebih rendah** (belum diuji)
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
| Relay K1 | DPST-NO 8 A / 250 VAC IEC class | TE RT2 series | Exact MPN, UL/IEC, lifecycle, inrush | `PENDING` |
| Terminal output | 10 A class | MPN belum final | Torsi/creepage | `UNVERIFIED` |
| Socket output Type F | 16 A / 250 V class | MPN belum dipilih | Retensi/PE/contact material | `UNVERIFIED` |
| PCB carrier | Tidak membawa mains | Desain off-board | Hanya SELV | `PROVISIONAL` |
| PE path | Kontinu, tidak diputus | Desain konsep | MPN/stud/torsi/uji | `BLOCKED` |

## 2. Perhitungan batas

- Relay 8 A IEC class adalah elemen terendah yang diketahui.
- Fuse 10 A **tidak** menaikkan rating kontinu; fuse adalah backup.
- Untuk beban kontinu, terapkan derating minimal 80% dari rating relay pada ambient yang disetujui:
  - 8 A × 0.8 = **6.4 A** pada ambient 40 °C, sebelum koreksi enclosure.
  - Jika suhu internal enclosure lebih tinggi, rating turun lagi.
- Target 10 A **tidak tercapai** dengan relay 8 A. Pilihan:
  1. Turunkan rating final ke 6.4–8 A dan uji termal.
  2. Ganti ke contactor 2P 16 A dan enclosure lebih besar.
  3. Ganti ke relay DPST 10 A yang punya datasheet resmi (belum ditemukan).
- Jangan memberi label "10 A" pada produk dengan relay 8 A.

## 3. Beban dan inrush

Q04=B (campuran elektronik/SMPS) berarti:
- Adaptor SMPS dapat memiliki inrush kapasitif tinggi.
- Relay 8 A resistif belum otomatis cocok untuk inrush SMPS.
- Perlu datasheet contact category, inrush test, dan lifecycle.
- Beban motor/induktif tidak dijanjikan.
- Kontak relay dapat weld; firmware tidak boleh mengklaim OFF fisik tanpa feedback.

## 4. Koordinasi (ringkas)

1. Fuse 10 A melindungi kabel/terminal dari short circuit, bukan relay dari overload kecil.
2. Thermal cutoff independen memutus L jika hotspot melebihi trip; posisi dan rating harus diuji.
3. MOV membatasi transient; koordinasi dengan fuse dan thermal cutoff harus dihitung.
4. Software overcurrent (jika ada) hanya supplementary; tidak menggantikan fuse/thermal cutoff.
5. PE tidak boleh melalui fuse/relay/PCB trace sebagai satu-satunya jalur.

## 5. Bukti yang diperlukan sebelum rating dikunci

- [ ] Datasheet exact MPN relay, fuse, holder, terminal, socket, plug, PSU.
- [ ] Perhitungan time-current dan breaking capacity.
- [ ] Pengukuran temperature rise relay/terminal/fuse pada 6.4 A, 8 A, dan overload terkendali di lab.
- [ ] Uji inrush SMPS.
- [ ] Uji lifecycle kontak.
- [ ] Review engineer kompeten.
- [ ] Label final berdasarkan rating terendah.

**Kesimpulan:** `BLOCKED`. Jangan fabrikasi atau memberi rating final sebelum bukti di atas.
