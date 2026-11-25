# Polarity and Protective Earth Assessment — REV_D_CORE_ONLY

**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW`
**Konteks:** Q02=D (analisis kompatibilitas Indonesia; lean Type E/F), Q05=A (tinjau pemutusan dua kutub).

## 1. Masalah polaritas

- Plug Type F (Schuko) dapat dimasukkan dengan orientasi terbalik.
- Tidak ada jaminan L/N tetap pada posisi yang sama setiap kali dicolok.
- Sakelar satu kutub dapat meninggalkan konduktor lain tetap bertegangan.
- Warna kabel bukan bukti polaritas pada instalasi yang salah.

## 2. Keputusan yang diminta

| Opsi | Deskripsi | Penilaian |
|---|---|---|
| A. Dua kutub | 2-channel optocoupler module: CH1 L, CH2 N; PE kontinu; bukan DPST linked | **Ditinjau**; konservatif untuk plug reversibel, dengan residual risk channel tidak linked |
| B. Satu kutub | Hanya L atau hanya N diputus | Hanya jika arsitektur keselamatan dan pemasangan membuktikan; belum |
| C. Engineer memilih | Studi standar | Diperlukan jika A tidak memenuhi ruang/rating |

**Rekomendasi:** pertahankan dua channel (L/N) sebagai arah desain, dengan rating provisional **6 A/1.380 W** (dibatasi BLX-A 6.3 A holder). Module bukan DPST mechanically linked; uji tiap channel dan dokumentasikan residual risk. Jangan kembali ke satu kutub hanya untuk mengejar rating lebih tinggi.

## 3. PE path

```
Plug PE → dedicated PE terminal/stud → socket PE
```

Aturan:
- PE tidak melalui relay, fuse, MOV, atau PCB trace sebagai satu-satunya jalur.
- Gunakan screw/stud dengan lock washer, torsi, dan label.
- Jangan menggunakan anodized/painted surface sebagai konduktor.
- Sediakan test point kontinuitas.
- PE harus tetap kontinu saat relay OFF, fuse open, atau PSU mati.
- Jangan menyebut PE sebagai "GND" di wiring; gunakan nama `PE`.

## 4. Skenario uji

| Uji | Metode | Status |
|---|---|---|
| Kontinuitas PE plug→socket | Multimeter/4-wire, < batas engineer | `BLOCKED` (alat tidak ada) |
| Kontinuitas PE saat relay OFF/ON | Ulangi pada kedua state | `BLOCKED` |
| Reverse plug orientation | Uji fungsional dan inspeksi | `BLOCKED` |
| Tarik/putar socket | Uji retensi mekanik | `BLOCKED` |
| Torsi terminal PE | Tool torsi terkalibrasi | `BLOCKED` |
| Insulation resistance PE↔L/N | Lab kompeten | `BLOCKED` |

## 5. Kesimpulan

- Dua kutub adalah arah yang lebih dapat dipertahankan untuk plug reversibel.
- PE kontinu adalah syarat mutlak; desain belum membuktikannya.
- Jangan memberi label "polaritas aman" atau "PEOK" tanpa uji.

**Status:** `BLOCKED`.
