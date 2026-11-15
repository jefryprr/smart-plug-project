# 00 — Baca Dulu

**Status proyek:** `REV_A_PROVISIONAL` — digital artifacts only; no hardware validation.
**Prinsip:** jangan pernah menganggap perintah/alat berhasil hanya karena file ada. Simpan log dan exit code.

## Apa yang boleh dikerjakan sendiri

- Membaca dokumen, menjalankan software, menguji API/web/simulator.
- Assembly mekanik tanpa listrik.
- Solder low-voltage (dengan latihan/QC).
- Memeriksa file KiCad/CAD secara digital.

## Apa yang TIDAK boleh dilakukan tanpa pengawasan

- Membuka enclosure saat mains aktif.
- Menghubungkan 230 VAC ke prototipe.
- Hipot/dielectric/insulation resistance test.
- Uji beban/termal/short-circuit.
- Mengubah PE, fuse, relay, atau enclosure safety.

## Status saat ini

- Firmware core: 74 host checks PASS.
- API: 38 tests PASS.
- Web: build + 5 Playwright tests PASS, axe no serious/critical on login/dashboard.
- KiCad 10.0.8: ERC 0 on block schematic; routed 100x70 SELV carrier DRC 0/0; routed Gerber/drill/POS exported.
- ESP-IDF v6.1 target build: PASS (no flash).
- Android debug APK: PASS (not installed); Docker/Postgres: BLOCKED.
- Physical tests: BLOCKED (no hardware/lab).

## Urutan aman

1. Baca `PRD.md`, `docs/decisions/USER_ANSWERS.md`, `safety/`.
2. Jalankan tes digital.
3. Siapkan alat/lab dan engineer.
4. Lakukan uji low-voltage.
5. Baru pertimbangkan mains dengan prosedur lab.
