# 02 — Setup KiCad

**Status lingkungan:** `BLOCKED: KICAD_NOT_INSTALLED`

## Instalasi

1. Unduh KiCad resmi dari https://www.kicad.org/download/.
2. Pilih versi stabil yang kompatibel dengan Windows 11.
3. Catat versi dan hash installer.
4. Tambahkan `kicad-cli` ke PATH (biasanya `C:\Program Files\KiCad\<versi>\bin`).

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

- File saat ini adalah **system block schematic** dan **placement-only PCB**.
- Belum ada footprint/routing/DRC/Gerber.
- Jangan mengirim ke fabrikasi.
