# 06 — Install Support Tools

| Tool | Status | Catatan |
|---|---|---|
| Graphviz | Portable 16.1.1 | `tools/graphviz`; hash dicatat |
| Zig | Portable 0.17.1 | `tools/zig`; host C tests |
| FreeCAD | `NOT_INSTALLED` | Untuk validasi STEP independen |
| Blender | `NOT_INSTALLED` | Render opsional |
| MeshLab | `NOT_INSTALLED` | Validasi STL |
| Inkscape | `NOT_INSTALLED` | Konversi SVG/PDF |
| ImageMagick | `NOT_INSTALLED` | Batch image |
| Docker | `NOT_INSTALLED` | Compose/Postgres/Mosquitto |
| JDK | 17 tersedia | FreeRouting butuh JDK |

## Prinsip

- Instalasi admin minta izin.
- Jangan mengunduh skrip remote tanpa audit.
- Catat versi, hash, tanggal, dan command.
- Tool yang tidak ada = `BLOCKED`, bukan alasan membuat file palsu.
