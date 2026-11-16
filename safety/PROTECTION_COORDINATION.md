# Protection Coordination — REV_C_PSU_BOARD

**Status:** `BLOCKED_PENDING_CALCULATION_AND_LAB`
**Prinsip:** fuse/thermal cutoff/MOV harus terkoordinasi; software bukan proteksi utama.

## 1. Rantai proteksi

```
TB1 L → F1 10 A → MOV (L-N) → TF1 TCO → TB2 L → relay pole 1 → socket L
TB1 N → TB2 N → relay pole 2 → socket N
HLK AC branch from TB2/TCO output → HLK-5M05 → F2 PTC + D1 TVS → J5/J6/J7 5 V
PE → dedicated chassis stud → socket PE (tidak diputus)
```

## 2. Tabel koordinasi (nilai belum final)

| Perangkat | Fungsi | Rating | Karakteristik | Koordinasi |
|---|---|---|---|---|
| REV_C PSU board | Mains entry + SELV output | 50x65 mm, 2 oz target | 2 mm isolation notch; HLK bridges | Creepage/hipot/thermal UNVERIFIED |
| Fuse F1 | Short-circuit backup | 10 A, 250 V, time-lag | Time-current TBD | On PSU board, after TB1; protect wiring/terminal |
| PTC F2 (5 V) | SELV 5 V wiring backup | 1.1 A hold, 1206 | Trip/time TBD | Bukan proteksi mains; melindungi wiring/rail 5 V |
| TVS D1 (5 V, PSU board) | SELV transient clamp | SMBJ5.0A, 5 V standoff | Clamping TBD | Melindungi total output 5 V J5/J6/J7; bukan pengganti isolasi |
| Holder F1 clips | Mounting | 10 A class TBD | TBD | Tool-access via lid; rating/retention TBD |
| MOV1 | Transient clamping | 275 VAC class | Energy/clamping TBD | Perlu thermal fuse/koordinasi end-of-life |
| Thermal cutoff TF1 | Independent overtemp | 99 °C, 10 A class TBD | One-shot | On PSU board after MOV; senses HLK/terminal/PCB hotspot; trip removes load + HLK |
| Relay module K1 | Disconnect (2 channels) | 10 A class claim, final 8 A | Two independent SPDT channels, active-low; not mechanically linked | Rating kontak/inrush/lifecycle; channel weld |
| TB1/TB2 | Connection | 10 A class TBD | Torsi/ferrule | On PSU board; input/output L/N; no PE |
| J5/J6/J7 | 3x 5 V output | 3 A class TBD | Keyed JST-XH 2.5 mm | J5 carrier, J6 relay, J7 PZEM conditional |
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
