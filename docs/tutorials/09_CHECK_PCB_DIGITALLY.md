# 09 — Periksa PCB Secara Digital

**Status:** `PARTIAL` — placement preview only.

## Saat ini

- `hardware/kicad/smartplug.kicad_pcb` adalah placement-only 75x50 mm.
- DRC 0 untuk geometri placement; tidak ada routing, net, atau footprint final.
- `hardware/pcb/render/placement_preview.png/.svg` adalah preview, bukan plot KiCad.

## Verifikasi KiCad (sudah dijalankan)

1. Buka PCB, periksa outline/mounting.
2. Jalankan DRC.
3. Periksa unrouted, clearance, courtyard, silkscreen.
4. Review mains/SELV barrier (jika PCB membawa mains — saat ini tidak).
5. Export Gerber/drill, re-import di viewer.
6. Catat command/exit code.

## Larangan

- Jangan menurunkan clearance agar PASS.
- Jangan mengecualikan seluruh rule.
- Jangan fabrikasi dari file provisional.
