# Protection Coordination — REV_B_NO_TEMP

**Status:** `BLOCKED_PENDING_CALCULATION_AND_LAB`
**Prinsip:** fuse/thermal cutoff/MOV harus terkoordinasi; software bukan proteksi utama.

## 1. Rantai proteksi

```
L → fuse 10 A → MOV (L-N) → thermal cutoff → relay pole 1 → socket L
N → relay pole 2 → socket N
PE → socket PE (tidak diputus)
```

## 2. Tabel koordinasi (nilai belum final)

| Perangkat | Fungsi | Rating | Karakteristik | Koordinasi |
|---|---|---|---|---|
| Fuse F1 | Short-circuit backup | 10 A, 250 V, time-lag | Time-current TBD | Harus melindungi kabel/terminal; jangan menganggap proteksi overload presisi |
| Holder FH1 | Mounting | 10 A class TBD | TBD | Rating, sentuhan, akses servis |
| MOV1 | Transient clamping | 275 VAC class | Energy/clamping TBD | Perlu thermal fuse/koordinasi end-of-life |
| Thermal cutoff TF1 | Independent overtemp | 99 °C, 10 A class TBD | One-shot | Dipasang di hotspot; trip mengunci OFF |
| Relay module K1 | Disconnect (2 channels) | 10 A class claim, final 8 A | Two independent SPDT channels, active-low; not mechanically linked | Rating kontak/inrush/lifecycle; channel weld |
| Terminal TB1/TB2 | Connection | 10 A class TBD | Torsi/ferrule | Tidak boleh longgar/panas |
| Socket X1 | Output | 16 A class TBD | Retensi/PE | Tidak boleh berputar/tercabut |
| Software | Supplemental | Threshold TBD | Sampling | Tidak boleh menjadi satu-satunya proteksi |

## 3. Skenario

| Skenario | Respons yang diharapkan | Bukti diperlukan |
|---|---|---|
| Short circuit L-N di output | Fuse putus, relay terbuka, tidak ada api | Uji lab dengan sumber arus terbatas |
| Overload 12 A kontinu | Fuse/thermal cutoff/relay coordination | Uji time-current dan temperature rise |
| Relay contact weld (one channel) | Tidak ada klaim OFF; channel lain/thermal cutoff/fuse backup | Uji kontak per channel dan FMEA |
| MOV end-of-life short | Fuse/thermal coordination, tidak ada api | Uji surge/end-of-life |
| Terminal loose | Temperature rise, thermal cutoff trip | Uji tarik/torsi/termal |
| PSU failure | SELV mati, relay drop (coil de-energized) | Fault injection |
| Firmware hang | Watchdog reset, relay commanded OFF; independent protection tetap | Unit/HIL low-voltage |
| Overvoltage transient | MOV clamping; warning hanya indikasi | Surge test |

## 4. Breaking capacity / fault current

- Fault current rumah tangga Indonesia dapat tinggi; breaking capacity fuse/holder harus sesuai.
- Nilai prospective short-circuit current di lokasi instalasi **belum diukur**.
- Jangan memakai fuse kaca murah tanpa breaking capacity yang terdokumentasi.
- Koordinasi harus dihitung oleh engineer, bukan dipilih dari nama "10 A".

## 5. Status

- [ ] Perhitungan time-current.
- [ ] Breaking capacity dan holder rating.
- [ ] MOV energy/clamping/thermal coordination.
- [ ] Thermal cutoff trip dan holding current.
- [ ] Uji short-circuit/overload di lab kompeten.
- [ ] Uji kedua channel module relay secara terpisah (weld/stuck).
- [ ] Sign-off.

**Kesimpulan:** `BLOCKED`. Jangan mengklaim proteksi lengkap.
