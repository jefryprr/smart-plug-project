# 01 — Setup Windows 11 + OpenCode

**Status proyek:** `REV_A_PROVISIONAL` — digital artifacts only; no hardware validation.
**Prinsip:** jangan pernah menganggap perintah/alat berhasil hanya karena file ada. Simpan log dan exit code.

## Prasyarat

- Windows 11, PowerShell 7 (disarankan), Git, Node 24+, Python 3.11.
- Repo di `C:\Users\<nama>\Zed\SMART-PLUG-V2` (contoh; jangan hardcode di source).

## Verifikasi

```powershell
git --version
node --version
npm --version
python --version
```

## Install dependency repo

```powershell
npm install
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe pyyaml kiutils wireviz cadquery trimesh matplotlib numpy pillow reportlab svglib
```

## Jalankan tes

```powershell
npm run test
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
```

## Batas hak akses

- Jangan meminta admin kecuali perlu.
- Jangan mengubah firewall/membuka port publik tanpa izin.
- Jangan commit `.env` atau token.
