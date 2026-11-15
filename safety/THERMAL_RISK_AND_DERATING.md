# Thermal Risk and Derating — REV_B_NO_TEMP

**Status:** `BLOCKED_PENDING_THERMAL_TEST`
**Ambient target:** 25–40 °C (belum ditetapkan); enclosure internal lebih tinggi.

## 1. Perkiraan disipasi

| Sumber | Perkiraan losses | Catatan |
|---|---:|---|
| PSU HLK-5M05 | **~2.1 W at 5 W full load** | Efisiensi ~70% pada 220 V; datasheet distributor |
| Relay module, 2 channels | ~0.4–0.8 W | Two 5 V coils + optocoupler input; measure exact batch |
| Relay contact/terminal | UNKNOWN | Tergantung arus, contact resistance, terminal |
| ESP32-S3 + Wi-Fi | ~0.5–1.0 W | Burst |
| OLED/RGB/sensor | ~0.1 W | Kecil |
| Fuse holder/terminal | UNKNOWN | Hotspot utama |
| **Total kasar** | **~3–5 W + contact losses** | Bukan hasil pengukuran; HLK efficiency lowers margin vs IRM |

## 2. Perkiraan kenaikan suhu enclosure

Luas permukaan eksternal kasar (220×120×70 mm recommended):
`2 × (220×120 + 220×70 + 120×70) = 100.400 mm² = 0.1004 m²`.

Dengan koefisien konveksi/radiasi efektif kasar 5–10 W/(m²·K):
- 3 W → ΔT ≈ 3 / (0.1004 × 5…10) ≈ **3.0–6.0 K**.
- 5 W → ΔT ≈ 5 / (0.1004 × 5…10) ≈ **5.0–10.0 K**.
- 180×120 (0.0852 m²) would give ~3.5–7.0 K at 3 W, but that size fails real clearance review.
- Ini hanya estimasi; hotspot lokal dapat jauh lebih tinggi.
- Enclosure tertutup, tidak ada ventilasi, dan komponen berdekatan dapat menaikkan ΔT.
- Enclosure yang dipilih (MG Duradus ABS IP65, 220×120×70) belum terbukti flame-retardant/UL94 V-0; thermal aging dan hotspot lokal wajib diuji.

## 3. Hotspot yang wajib diukur

1. Terminal fuse holder.
2. Terminal relay L/N.
3. Terminal socket L/N.
4. Body relay.
5. PSU case.
6. PZEM terminal/CT.
7. Enclosure near relay/terminal.
8. ESP32 (kurang kritis).

**Tidak ada sensor suhu di REV_B.** Firmware tidak dapat mendeteksi hotspot; proteksi termal hanya fuse + TCO one-shot. Thermal test tertutup dan load test menjadi wajib, bukan opsional.

## 4. Derating

- Module relay 10 A class claim × 0.8 = **8 A** pada ambient 40 °C, sebelum koreksi enclosure. Ini asumsi vendor, bukan hasil uji.
- Jika temperature rise terminal > 30 K pada 6.4 A, turunkan rating.
- Fuse 10 A tidak boleh dianggap rating kontinu 10 A.
- Kabel 1.5 mm² harus dihitung dengan grouping/ambient.
- Jangan menaruh OLED/ESP32 di atas hotspot.

## 5. Uji yang diperlukan (lab kompeten)

- [ ] Thermocouple pada 8 titik, load bank resistif, 25%/50%/75%/100% rating provisional.
- [ ] Soak 1 jam dan 4 jam; catat stabil.
- [ ] Thermal camera.
- [ ] Uji enclosure tertutup vs terbuka (diagnostik).
- [ ] Uji overload terkendali.
- [ ] Uji relay lifecycle.
- [ ] Uji ambient 40 °C (oven/ruang terkontrol).
- [ ] Dokumentasi hasil dan sign-off.

**Status:** `BLOCKED`. Tidak ada klaim thermal aman.
