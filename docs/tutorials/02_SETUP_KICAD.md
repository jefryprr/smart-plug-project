# 02 — Setup KiCad

**Status lingkungan:** `PASS: KICAD_10.0.8_PORTABLE`

## Instalasi

1. Unduh installer KiCad resmi 10.0.8 dari https://www.kicad.org/download/.
2. Ekstrak installer secara portable ke `tools/kicad` (bukan instalasi penuh) bila disk terbatas.
3. Catat versi dan hash installer.
4. Gunakan `tools/kicad/bin/kicad-cli.exe` atau tambahkan direktori itu ke PATH.

## Verifikasi

```powershell
kicad-cli version
```

## Buka proyek

- `hardware/kicad/smartplug.kicad_pro`
- `hardware/kicad/smartplug.kicad_sch`
- `hardware/kicad/smartplug.kicad_pcb`

## Jalankan ERC/DRC (setelah terpasang)

```powershell
kicad-cli sch erc --output reports/kicad/erc.json hardware/kicad/smartplug.kicad_sch
kicad-cli pcb drc --output reports/kicad/drc.json hardware/kicad/smartplug.kicad_pcb
```

Catat command, versi, exit code, dan temuan. Jangan mengecualikan rule untuk membuat PASS.

## Batas

- File saat ini adalah **system block schematic** dan **routed SELV carrier 100x70**.
- Belum ada footprint/routing/DRC/Gerber.
- Jangan mengirim ke fabrikasi.
