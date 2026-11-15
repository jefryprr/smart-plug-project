# 03 — Setup Circuit-Synth

**Status:** `NOT_USED` / `DEVIATION`

## Keputusan

PRD menyarankan Circuit-Synth, tetapi generator yang dipakai adalah `hardware/generators/generate_kicad.py` (native S-expression) karena:
- KiCad tidak terpasang untuk verifikasi round-trip.
- File yang dihasilkan adalah block schematic, bukan schematic komponen penuh.
- Menghindari klaim kompatibilitas API yang tidak diuji.

## Jika ingin mencoba Circuit-Synth

```powershell
uv pip install --python .venv\Scripts\python.exe circuit-synth
python -c "import circuit_synth; print(circuit_synth.__version__)"
```

Lakukan smoke test satu sheet, buka di KiCad, dan bandingkan hasilnya. Catat deviasi di ADR-008.

## Jangan

- Jangan mengklaim schematic komponen penuh dari generator block.
- Jangan menimpa file KiCad manual tanpa backup/ADR.
