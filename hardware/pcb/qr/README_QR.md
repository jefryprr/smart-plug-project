# PCB QR Label — Schematic Documentation

**Status:** `PROTOTYPE_LABEL` / **NOT_FOR_USE**  
**Placement:** SELV carrier only, `F.SilkS` outline + printed label  
**Label:** 22 × 22 mm, white polyester/polyimide, black print  
**QR target:** `https://github.com/jefryprr/smart-plug-project/blob/main/hardware/schematic/SYSTEM_SCHEMATIC.pdf`

## Files

| File | Isi |
|---|---|
| `pcb_label_22mm.pdf` | Label siap cetak, ukuran **22,00 × 22,00 mm** (100% scale) |
| `pcb_label_22mm.png` | Preview 1200 dpi |
| `pcb_label_22mm.svg` | Vector |
| `schematic_qr.png` | QR saja (referensi) |
| `SCHEMATIC_QR_22MM.kicad_mod` | Footprint silkscreen-only, tanpa pad/copper |
| `SCHEMATIC_QR.pretty/` | Library footprint untuk KiCad |
| `QR_PLACEMENT.md` | Hasil cek clearance |
| `QR_TEST_REPORT.md` | Hasil scan test |
| `carrier_top_with_qr.png` | Visual placement di render PCB |

## Apakah aman?

**Bisa dan aman dengan metode label + silkscreen outline**, karena:

- Tidak ada perubahan **copper, pad, via, solder mask, atau netlist**.
- Label ditempel di area **SELV carrier**, bukan di PSU mains.
- Area label `x=14..36 mm`, `y=36..58 mm` sudah dicek:
  - tidak ada pad dalam 1,5 mm,
  - tidak ada via,
  - tidak ada test point/fiducial/mounting hole,
  - jarak ke baris socket DevKit 3,14 mm,
  - margin tepi PCB 12 mm.
- Label menutupi beberapa **trace SELV** dan teks silkscreen `BUTTON`; ini tidak memutus/mengubah copper. Jika teks `BUTTON` harus tetap terlihat, pindahkan teks silk itu ±5 mm (perubahan silkscreen saja).

**Jangan** menaruh QR di PSU mains. **Jangan** scan dengan mains ON atau tangan masuk ke enclosure terbuka. Scan hanya saat mains OFF/enclosure aman, atau gunakan duplikat label di luar enclosure.

## Pemasangan

1. Cetak `pcb_label_22mm.pdf` **100% scale** di label putih polyester/polyimide, tinta hitam, laminasi matte.
2. Bersihkan area label dengan IPA; keringkan.
3. Tempel setelah reflow/cleaning, bukan sebelum.
4. Area: `x=14..36 mm`, `y=36..58 mm`; center `(25,47) mm`.
5. Jangan menutup TP5, via, atau pad. TP5 berada 4 mm di atas area label.
6. Tambahkan footprint `SCHEMATIC_QR_22MM` di `(25,47) mm`, layer `F.SilkS`; **tanpa pad/copper**.
7. Jalankan DRC setelah menambahkan footprint; periksa silk-over-pad.
8. Uji scan dengan phone sebelum enclosure ditutup.

## Aktivasi URL

QR mengarah ke PDF di repo publik `jefryprr/smart-plug-project`. URL akan **404 sampai** file berikut di-commit dan di-push ke branch `main`:

- `hardware/schematic/SYSTEM_SCHEMATIC.pdf`

Repo sudah publik, jadi setelah push URL langsung bisa diakses. QR belum diuji lewat internet karena PDF belum di-push.

## Catatan penting

- QR ini bukan pengganti dokumentasi cetak/lab. Isinya hanya link.
- Jangan mengklaim QR sebagai rating/CE/SNI/UL.
- Label bukan barrier isolasi; jangan menaruhnya di jalur creepage/clearance mains.
- Jika label rusak, ganti; jangan menempel label baru di atas label lama.
