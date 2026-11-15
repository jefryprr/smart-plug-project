# 04 — Setup WireViz

**Status:** `PASS` — 5 harness dirender (SVG/PNG/PDF/GV).

## Prasyarat

- Python `.venv` dengan `wireviz`, `svglib`, `reportlab`.
- Graphviz `dot` di PATH. Repo memakai portable `tools/graphviz/Graphviz-16.1.1-win64/bin`.

## Render

```powershell
$env:PATH = "$PWD\tools\graphviz\Graphviz-16.1.1-win64\bin;$env:PATH"
.venv\Scripts\python.exe scripts\render_wiring.py
```

Output: `hardware/wiring/renders/`.

## Edit YAML

- `hardware/wiring/main_harness.yaml`
- sub-harness: display, metering, controller, i2c, AC engineer review.

Gunakan kode warna 2 huruf (`BN`, `BU`, `GNYE`, `RD`, `BK`, `WH`, `GY`, `OG`). `color` adalah jaket kabel; `colors` adalah warna per wire.

## Periksa

- PE tidak melalui relay/fuse.
- Mains dan SELV tidak bertemu.
- Kabel/terminal punya identitas.
- Diagram tidak menjamin keselamatan fisik.
