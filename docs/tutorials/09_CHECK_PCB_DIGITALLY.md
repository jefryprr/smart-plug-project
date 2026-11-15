# 09 — Periksa PCB Secara Digital

**Status:** `PARTIAL` — placement preview only.

## Saat ini

- `hardware/kicad/smartplug.kicad_pcb` adalah placement-only 75×50 mm.
- Tidak ada routing, net, footprint final, atau DRC.
- `hardware/pcb/render/placement_preview.png/.svg` adalah preview, bukan plot KiCad.

## Setelah KiCad terpasang

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
