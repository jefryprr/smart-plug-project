# 07 — Baca BOM dan Datasheet

## BOM

- `bom/BOM_MASTER.csv` — BOM rekayasa, harga tidak dimasukkan.
- `bom/BOM_PROCUREMENT.csv` — daftar belanja bertanggal 2026-11-16; 40 listing-verified, 17 estimated.
- `bom/BOM_SUMMARY.json` — `PROCUREMENT_PRICED_2026-11-16`; CORE/FULL totals.
- `bom/COMPONENT_APPROVALS.yaml` — belum ada persetujuan fabrikasi.
- `research/PROCUREMENT_INDONESIA.md` — seller, harga, stok, risiko.
- `research/datasheets/MANIFEST.md` — hash/tautan.

## MPN vs nama pasaran

- Nama "PZEM-004T V4" bukan identitas batch.
- "Relay 10 A" tanpa contact arrangement bukan DPST.
- Socket "universal" tanpa sertifikasi bukan otomatis aman.

## Checklist

1. Manufacturer + MPN + revision.
2. Datasheet resmi + tanggal akses.
3. Rating sesuai aplikasi (bukan rating CT).
4. Dimensi terukur.
5. Failure mode/isolation.
6. Harga/stock bertanggal.
7. Status approval.

Jangan membeli berdasarkan BOM ini.
