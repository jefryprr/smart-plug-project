# AGENTS.md — aturan kerja agen

Dokumen ini merangkum aturan operasional yang mengikat pekerjaan pada repo ini. PRD utama tetap `PRD.md`; jika terjadi konflik, PRD menang.

## Batas keselamatan

1. Jangan pernah menyatakan desain 230 VAC siap produksi, siap digunakan, atau aman tanpa review engineer kompeten dan uji fisik.
2. Jangan mengaktifkan `hardware/manufacturing/released/` atau memberi label `READY_FOR_FABRICATION` sebelum gate F4.
3. Jangan menjalankan atau menulis prosedur energisasi mains untuk orang awam. Pekerjaan mains hanya untuk personel kompeten dengan prosedur lab.
4. PE tidak boleh diputus oleh relay, fuse, atau sakelar.
5. Uji mock/simulator tidak boleh dilaporkan sebagai HIL atau uji PLN.
6. Nilai yang belum diverifikasi harus `UNKNOWN`, `UNVERIFIED`, atau `BLOCKED`; jangan diisi angka rekaan.

## Alur kerja

- Satu `design_revision` untuk semua artefak.
- Setiap perubahan GPIO/komponen/firmware harus memicu crosscheck dan regresi terkait.
- Semua perintah build/test yang diklaim harus punya log di `reports/` dan exit code yang dicatat.
- Jangan menyimpan secret, token, private key, atau password nyata di repo.
- Hentikan pekerjaan pada gate keselamatan yang belum disetujui; lanjutkan pekerjaan digital independen.

## Status yang dipakai

`PASS`, `FAIL`, `BLOCKED`, `UNVERIFIED`, `PROVISIONAL`, `DIGITAL_COMPLETE`, `ENGINEERING_REVIEW_REQUIRED`, `HARDWARE_VALIDATION_REQUIRED`, `READY_FOR_FABRICATION`, `READY_FOR_USE`.

Status digital tidak otomatis menjadi status keselamatan fisik.
