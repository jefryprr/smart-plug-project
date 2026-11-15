# Thermal Risk and Derating — REV_A_PROVISIONAL

**Status:** `BLOCKED_PENDING_THERMAL_TEST`
**Ambient target:** 25–40 °C (belum ditetapkan); enclosure internal lebih tinggi.

## 1. Perkiraan disipasi

| Sumber | Perkiraan losses | Catatan |
|---|---:|---|
| PSU IRM-05-5 | ~1.0–1.7 W | Efisiensi ~75–85%, output 5 W; datasheet perlu |
| Relay coil RT2 | ~0.4 W | 5 V coil, ~80 mA |
| Relay contact/terminal | UNKNOWN | Tergantung arus, contact resistance, terminal |
| ESP32-S3 + Wi-Fi | ~0.5–1.0 W | Burst |
| OLED/RGB/sensor | ~0.1 W | Kecil |
| Fuse holder/terminal | UNKNOWN | Hotspot utama |
| **Total kasar** | **~2–4 W + contact losses** | Bukan hasil pengukuran |

## 2. Perkiraan kenaikan suhu enclosure

Luas permukaan eksternal kasar (150×100×70 mm):
`2 × (150×100 + 150×70 + 100×70) = 65.000 mm² = 0.065 m²`.

Dengan koefisien konveksi/radiasi efektif kasar 5–10 W/(m²·K):
- 3 W → ΔT ≈ 3 / (0.065 × 5…10) ≈ **4.6–9.2 K**.
- Ini hanya estimasi; hotspot lokal dapat jauh lebih tinggi.
- Enclosure tertutup, tidak ada ventilasi, dan komponen berdekatan dapat menaikkan ΔT.

## 3. Hotspot yang wajib diukur

1. Terminal fuse holder.
2. Terminal relay L/N.
3. Terminal socket L/N.
4. Body relay.
5. PSU case.
6. PZEM terminal/CT.
7. Enclosure near relay/terminal.
8. OLED/ESP32 (kurang kritis).

## 4. Derating

- Relay 8 A × 0.8 = 6.4 A pada ambient 40 °C, sebelum koreksi enclosure.
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
