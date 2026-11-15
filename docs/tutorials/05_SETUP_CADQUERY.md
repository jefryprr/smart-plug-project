# 05 — Setup CadQuery

**Status:** `PASS` — STEP/STL dan render dihasilkan.

## Prasyarat

```powershell
uv pip install --python .venv\Scripts\python.exe cadquery trimesh matplotlib
```

## Build

```powershell
.venv\Scripts\python.exe hardware\mechanical\source\enclosure.py --preset both
.venv\Scripts\python.exe hardware\mechanical\source\render.py
```

Output: `hardware/mechanical/export/`, `render/`, `drawings/`, `FIT_ANALYSIS.md`.

## Aturan

- Dimensi modul adalah approximate sampai diukur.
- 3D print hanya prototipe mekanik; bukan enclosure listrik tersertifikasi.
- Jangan mengklaim fit PASS fisik dari render.
- Jika parameter berubah, regenerasi dan review ulang.
