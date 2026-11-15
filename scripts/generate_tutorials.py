#!/usr/bin/env python3
"""Generate the minimum tutorial set required by PRD section 25.2."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tutorials"
OUT.mkdir(parents=True, exist_ok=True)

COMMON = """**Status proyek:** `REV_A_PROVISIONAL` — digital artifacts only; no hardware validation.
**Prinsip:** jangan pernah menganggap perintah/alat berhasil hanya karena file ada. Simpan log dan exit code.
"""

TUTORIALS = {
"00_READ_FIRST.md": """# 00 — Baca Dulu

""" + COMMON + """
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
""",
"01_SETUP_WINDOWS_OPENCODE.md": """# 01 — Setup Windows 11 + OpenCode

""" + COMMON + """
## Prasyarat

- Windows 11, PowerShell 7 (disarankan), Git, Node 24+, Python 3.11.
- Repo di `C:\\Users\\<nama>\\Zed\\SMART-PLUG-V2` (contoh; jangan hardcode di source).

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
uv pip install --python .venv\\Scripts\\python.exe pyyaml kiutils wireviz cadquery trimesh matplotlib numpy pillow reportlab svglib
```

## Jalankan tes

```powershell
npm run test
powershell -ExecutionPolicy Bypass -File firmware\\test\\host\\run_tests.ps1
```

## Batas hak akses

- Jangan meminta admin kecuali perlu.
- Jangan mengubah firewall/membuka port publik tanpa izin.
- Jangan commit `.env` atau token.
""",
"02_SETUP_KICAD.md": """# 02 — Setup KiCad

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
""",
"03_SETUP_CIRCUIT_SYNTH.md": """# 03 — Setup Circuit-Synth

**Status:** `NOT_USED` / `DEVIATION`

## Keputusan

PRD menyarankan Circuit-Synth, tetapi generator yang dipakai adalah `hardware/generators/generate_kicad.py` (native S-expression) karena:
- KiCad portable tersedia, tetapi generator tidak memakai API Circuit-Synth.
- File yang dihasilkan adalah block schematic, bukan schematic komponen penuh.
- Menghindari klaim kompatibilitas API yang tidak diuji.

## Jika ingin mencoba Circuit-Synth

```powershell
uv pip install --python .venv\\Scripts\\python.exe circuit-synth
python -c "import circuit_synth; print(circuit_synth.__version__)"
```

Lakukan smoke test satu sheet, buka di KiCad, dan bandingkan hasilnya. Catat deviasi di ADR-008.

## Jangan

- Jangan mengklaim schematic komponen penuh dari generator block.
- Jangan menimpa file KiCad manual tanpa backup/ADR.
""",
"04_SETUP_WIREVIZ.md": """# 04 — Setup WireViz

**Status:** `PASS` — 4 harness dirender (SVG/PNG/PDF/GV).

## Prasyarat

- Python `.venv` dengan `wireviz`, `svglib`, `reportlab`.
- Graphviz `dot` di PATH. Repo memakai portable `tools/graphviz/Graphviz-16.1.1-win64/bin`.

## Render

```powershell
$env:PATH = "$PWD\\tools\\graphviz\\Graphviz-16.1.1-win64\\bin;$env:PATH"
.venv\\Scripts\\python.exe scripts\\render_wiring.py
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
""",
"05_SETUP_CADQUERY.md": """# 05 — Setup CadQuery

**Status:** `PASS` — STEP/STL dan render dihasilkan.

## Prasyarat

```powershell
uv pip install --python .venv\\Scripts\\python.exe cadquery trimesh matplotlib
```

## Build

```powershell
.venv\\Scripts\\python.exe hardware\\mechanical\\source\\enclosure.py --preset both
.venv\\Scripts\\python.exe hardware\\mechanical\\source\\render.py
```

Output: `hardware/mechanical/export/`, `render/`, `drawings/`, `FIT_ANALYSIS.md`.

## Aturan

- Dimensi modul adalah approximate sampai diukur.
- 3D print hanya prototipe mekanik; bukan enclosure listrik tersertifikasi.
- Jangan mengklaim fit PASS fisik dari render.
- Jika parameter berubah, regenerasi dan review ulang.
""",
"06_INSTALL_SUPPORT_TOOLS.md": """# 06 — Install Support Tools

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
""",
"07_READ_BOM_AND_DATASHEETS.md": """# 07 — Baca BOM dan Datasheet

## BOM

- `bom/BOM_MASTER.csv` — BOM rekayasa, harga tidak dimasukkan.
- `bom/BOM_PROCUREMENT.csv` — daftar belanja bertanggal 2026-11-16; 43 listing-verified, 11 estimated.
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
""",
"08_READ_SCHEMATIC_AND_GPIO.md": """# 08 — Baca Schematic dan GPIO

## Schematic

- Root: `hardware/kicad/smartplug.kicad_sch` (9 blok).
- Child: `AC_INPUT_OUTPUT`, `SAFETY_AND_SWITCH`, `AC_DC_POWER`, `PZEM_AND_CT`, `LOW_VOLTAGE_CONTROL`, `ESP32S3_CARRIER`, `DISPLAY_AND_BUTTONS`, `RTC_ONLY`, `SERVICE_AND_DEBUG`.
- Ini **system block schematic**, bukan komponen penuh.

## GPIO

- `hardware/interfaces/gpio_map.yaml/.csv/.md`
- `firmware/main/board_config.h`
- `validation/GPIO_CROSSCHECK.json` — status `UNVERIFIED` karena board revision belum diverifikasi.

## Aturan

- Jangan memakai GPIO0/3/45/46 (strapping), 19/20 (USB), 26–37 (flash/PSRAM).
- Relay control butuh pulldown eksternal.
- Jangan menganggap GPIO48/38 universal untuk RGB.
- Verifikasi board fisik sebelum final.
""",
"09_CHECK_PCB_DIGITALLY.md": """# 09 — Periksa PCB Secara Digital

**Status:** `PARTIAL` — placement preview only.

## Saat ini

- `hardware/kicad/smartplug.kicad_pcb` adalah routed SELV carrier 100x70 mm (DRC 0/0).
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
""",
"10_ASSEMBLY_PLANNING.md": """# 10 — Perencanaan Assembly (Tanpa Energi)

## Urutan

1. Inspeksi komponen dan ukur dimensi.
2. Pasang heat-set insert.
3. Pasang carrier/standoff.
4. Pasang OLED/button/RGB (SELV).
5. Pasang PSU/relay/fuse/PZEM di zona mains (belum disambung).
6. Pasang socket/PE stud/gland.
7. Routing kabel, strain relief, ferrule.
8. Periksa barrier dan clearance visual.
9. Dokumentasi foto dan ukuran.

## Larangan

- Jangan menyambung mains saat assembly.
- Jangan mengandalkan solder/header untuk menahan kabel.
- Jangan menutup enclosure jika ada kabel terjepit.
- Jangan menganggap 3D print aman untuk listrik.
""",
"11_SOLDERING_LOW_VOLTAGE.md": """# 11 — Soldering Low Voltage

**Ruang lingkup:** SELV/PCB low-voltage saja. **Bukan** kabel/terminal mains.

## Alat

- Solder SAC305, flux, ESD strap, magnification, multimeter.
- Ventilasi.

## Prosedur

1. Inspeksi PCB/part.
2. Solder komponen low-profile, jangan overheats.
3. Periksa bridge/short dengan multimeter.
4. Bersihkan flux.
5. Dokumentasi foto.

## QC

- [ ] Tidak ada bridge.
- [ ] Polaritas IC/LED benar.
- [ ] Tidak ada cold joint.
- [ ] Konektor terkunci.
- [ ] Tidak ada sisa logam.

## Stop

Jika ada kerusakan pad/trace atau komponen panas, berhenti dan perbaiki/rework.
""",
"12_MAINS_ASSEMBLY_FOR_QUALIFIED_PERSONNEL.md": """# 12 — Mains Assembly (Qualified Personnel Only)

**Status:** `BLOCKED` — no approved mains design, no lab.

## Prasyarat

- Engineer sign-off on rating chain, isolation, PE, fuse/relay/terminal/socket.
- Lab with isolation transformer, RCD, rated probes, fire safety.
- Two-person rule and written procedure.

## Scope

- PE bond, fuse/MOV/thermal cutoff, relay DPST, socket/plug, strain relief.
- Verify continuity, torque, creepage, barrier.
- No energization until inspection passes.

## Larangan untuk pemula

- Jangan membuka/menyentuh mains.
- Jangan melakukan hipot/insulation test tanpa alat dan operator kompeten.
- Jangan menyalakan beban tanpa proteksi lab.

## Bukti

- Foto, torsi, kontinuitas PE, insulation resistance, label.
- Sign-off engineer.
""",
"13_INSPECTION_BEFORE_POWER.md": """# 13 — Inspection Before Power

**Status:** `BLOCKED` — form only; no inspection performed.

## Checklist

- [ ] Revisi BOM/schematic/PCB/CAD cocok.
- [ ] PE kontinu, tidak melalui relay/fuse.
- [ ] Fuse/relay/terminal/socket rating terverifikasi.
- [ ] Clearance/creepage review.
- [ ] Strain relief/gland.
- [ ] Tidak ada kabel terjepit/logam lepas.
- [ ] Isolation barrier utuh.
- [ ] Label/rating benar.
- [ ] Lab/prosedur/peralatan siap.
- [ ] Engineer sign-off.

## Stop

Jika ada keraguan pada PE/isolasi/rating, **jangan energisasi**.
""",
"14_SETUP_ESP_IDF.md": """# 14 — Setup ESP-IDF

**Status lingkungan:** `PASS: ESP_IDF_6.1_INSTALLED`

## Instalasi

1. Ikuti dokumentasi resmi Espressif untuk Windows.
2. Pin versi stabil (catat commit/versi).
3. Target `esp32s3`.
4. Pastikan Python/CMake/Ninja/toolchain sesuai.

```powershell
idf.py --version
idf.py set-target esp32s3
```

## Build

```powershell
cd firmware
idf.py build
```

Jika berhasil, catat hash binary dan ukuran.

## Host core tests (tersedia sekarang)

```powershell
powershell -ExecutionPolicy Bypass -File firmware\\test\\host\\run_tests.ps1
```

74 checks PASS. Target build ESP-IDF v6.1 juga PASS; lihat `reports/FIRMWARE_BUILD.md`. Ini bukan bukti flash/bench.

## Jangan

- Jangan mengklaim `.bin` jika build belum jalan.
- Jangan mengaktifkan secure boot/eFuse tanpa approval.
""",
"15_FLASH_AND_CONFIGURE.md": """# 15 — Flash dan Konfigurasi

**Status:** `BLOCKED` — no board; firmware build exists but has not been flashed.

## Prasyarat

- Board terverifikasi, adaptor USB data, port COM.
- Firmware binary hash.
- Bench low-voltage, relay coil/load simulator.
- Prosedur recovery.

## Flash

```powershell
idf.py -p COMx flash monitor
```

## Setelah flash

- Verifikasi boot log, relay OFF.
- Jangan hubungkan mains.
- Uji tombol/ACK low-voltage.
- Catat firmware version/hash.

## Stop

Jika relay aktif saat boot atau board panas, lepas daya dan debug low-voltage.
""",
"16_LOCAL_MOCK_TEST.md": """# 16 — Local Mock Test

## Jalankan simulator + API + broker

Cara termudah: gunakan script E2E yang menjalankan aedes + simulator + API:

```powershell
node scripts\\e2e_api.mjs
```

Atau manual:
```powershell
npm run dev:api
npm run sim:dev
```

## Uji

- Login demo.
- ON/OFF → pending → APPLIED.
- Inject fault (simulator) → ON rejected.
- Telemetry/analytics.
- Event history.

## Batas

- Ini simulator, bukan HIL/PLN.
- Jangan menyalin hasil mock ke laporan fisik.
""",
"17_SETUP_BACKEND_DB_MQTT.md": """# 17 — Setup Backend, DB, MQTT

## Local (tanpa Docker/Postgres)

```powershell
npm install
npm run dev:api
```

API memakai SQLite (`data/smartplug.db`), seed demo. Health:
```powershell
Invoke-RestMethod http://localhost:4000/health/live
```

## Target PostgreSQL/Mosquitto (belum dieksekusi)

- `database/migrations/001_init.sql`, `002_indexes.sql`
- `infrastructure/docker-compose.dev.yaml`
- `infrastructure/broker/mosquitto.prod.conf`, `aclfile.template`

## Blocker

- Docker/Postgres/Mosquitto tidak terpasang.
- API PostgreSQL adapter belum ada.
- Dev broker anonymous; production butuh TLS+ACL.

## Jangan

- Jangan mengklaim deploy berhasil tanpa container/health check.
""",
"18_RUN_NEXTJS_WEB.md": """# 18 — Jalankan Web Next.js

```powershell
npm install
npm run dev:web
```

Buka http://localhost:3000. API harus jalan di port 4000.

## Build

```powershell
npm run build -w @smartplug/web
npm run start -w @smartplug/web
```

## E2E

```powershell
npx playwright test
```

5 tests PASS; screenshots di `docs/ui-ux/screenshots/`.

## Catatan

- Demo data sintetik berlabel.
- Jangan menganggap UI sebagai bukti status fisik.
- API URL rewrite ada di `apps/web/next.config.mjs`.
""",
"19_BUILD_ANDROID_APK.md": """# 19 — Build Android APK

**Status:** `PASS: DEBUG_APK_BUILT` (not installed on a device)
**Yang sudah ada:** source `apps/android/App.tsx`, typecheck PASS, Expo Android bundle export PASS, debug APK 46,852,340 bytes, SHA-256 `BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61`.

## Prasyarat

- Android SDK di `D:\\AI INSTALLS\\Android\\Sdk` (platform 36/37, build-tools 36/37, NDK 27.1.12297006).
- JDK 17.
- Gradle cache di `D:\\AI INSTALLS\\gradle`.

## Build

```powershell
cd apps\\android
npm install
npx expo prebuild --platform android --no-install
cd android
.\\gradlew.bat assembleDebug --console=plain "-PreactNativeArchitectures=arm64-v8a"
```

APK: `apps/android/android/app/build/outputs/apk/debug/app-debug.apk`.
Bukti build: `reports/ANDROID_BUILD.md`, `reports/logs/android-gradle-build.log`.

## Release

- Keystore terpisah, password di secret manager.
- Jangan commit keystore.
- EAS butuh akun/izin.

## Batas

- Debug APK `NOT_PRODUCTION`.
- BLE/push belum diimplementasikan.
- API base URL: emulator `10.0.2.2`, fisik IP LAN.
""",
"20_PAIR_DEVICE.md": """# 20 — Pair Device

## Demo lokal

- Buka `/onboarding/pair-device`.
- Kode demo `123456` (seed).
- Kode sekali pakai, expiry 30 hari di seed.

## Alur produksi (rencana)

1. Device unprovisioned, relay OFF.
2. BLE/SoftAP window.
3. Kode pairing sekali pakai.
4. Wi-Fi credential aman.
5. Claim di web/Android.
6. Window ditutup; audit.

## Keamanan

- Jangan menulis kode/SSID/password ke log.
- Jangan memakai kode demo di produksi.
- Pairing bukan bukti keselamatan listrik.
""",
"21_CONFIGURE_TELEGRAM_PUSH.md": """# 21 — Telegram / Push

## Telegram (MVP)

- Buat bot melalui BotFather (akun pengguna, izin).
- Set `TELEGRAM_BOT_TOKEN` dan `TELEGRAM_CHAT_ID` di environment/secret store.
- Jangan commit token.
- Test: `POST /devices/{id}/notifications/test`.
- Tanpa token, backend memakai mock dan menandai `provider=mock`.

## Android push

- Belum diimplementasikan.
- Butuh FCM/Expo credentials, token lifecycle, opt-out, revoke.
- Tombol aksi tidak boleh bypass auth/lockout.

## Rate limit

- Test notification 2/min; alert dedup di backend.
""",
"22_DEPLOY_STAGING_PRODUCTION.md": """# 22 — Deploy Staging/Production

**Status:** `BLOCKED` — no Docker/VPS/domain/TLS/credentials.

## Staging lokal

```powershell
Copy-Item infrastructure\\.env.docker.example infrastructure\\.env.docker
docker compose -f infrastructure/docker-compose.dev.yaml --env-file infrastructure\\.env.docker up --build
```

## Production checklist

- Domain/DNS/TLS.
- MQTT TLS + password + ACL.
- PostgreSQL adapter (belum ada).
- Secrets/backup/monitoring.
- Security review.
- User approval for paid services.

## Jangan

- Jangan mengklaim URL/deploy yang tidak ada.
- Jangan memakai dev broker anonymous di production.
""",
"23_TESTING_AND_VALIDATION.md": """# 23 — Testing dan Validasi

## Jalankan

```powershell
npm run test
npm run typecheck
npm run build -w @smartplug/web
npx playwright test
powershell -ExecutionPolicy Bypass -File firmware\\test\\host\\run_tests.ps1
.venv\\Scripts\\python.exe scripts\\validate_connectivity.py
```

## Status saat ini

- Domain 34 tests PASS.
- MQTT 11 tests PASS.
- API 38 tests PASS (incl. simulator integration).
- Firmware core 74 checks PASS.
- Web 5 Playwright tests PASS; axe login/dashboard PASS.
- Static connectivity PASS.
- KiCad ERC 0 and routed carrier DRC 0/0 PASS; physical validation still BLOCKED.
- ESP-IDF v6.1 target build and Android debug APK PASS; Docker/Postgres remain BLOCKED.

## Arti status

- `PASS` digital ≠ HIL/PLN.
- `BLOCKED` bukan PASS.
- Jangan menghapus warning untuk membuat PASS.
""",
"24_OPERATIONS_AND_TROUBLESHOOTING.md": """# 24 — Operations dan Troubleshooting

Lihat:
- `docs/operations/RUNBOOK.md`
- `INCIDENT_RESPONSE.md`
- `BACKUP_RESTORE.md`
- `ROLLBACK_SERVER.md`
- `KEY_ROTATION.md`
- `DEVICE_REPLACEMENT.md`
- `TROUBLESHOOTING.md`

## Prinsip

- Cloud down tidak otomatis berarti relay OFF.
- Lockout harus menang atas perintah ON.
- Jangan bypass safety untuk "membuatnya bekerja".
- Insiden listrik: isolasi di breaker oleh personel kompeten.
""",
"25_FINAL_HANDOFF.md": """# 25 — Final Handoff

## Mulai dari

1. `README.md`
2. `deliverables/FINAL_ENGINEERING_REPORT.md`
3. `deliverables/manifest.json`
4. `reports/PHASE_1_ENGINEERING_REPORT.md`
5. `reports/PHASE_2_SOFTWARE_REPORT.md`
6. `safety/REVIEW_SIGNOFF_TEMPLATE.md`

## Yang siap digital

- API/web/simulator/firmware core tests.
- BOM research + dated Indonesian procurement matrix (unapproved).
- KiCad block schematic + routed 100x70 carrier, ERC 0 / DRC 0/0, Gerber/drill/POS.
- ESP-IDF v6.1 target build and `.bin`.
- WireViz harnesses.
- CadQuery enclosure/assembly + PZEM/relay brackets.
- Docs/runbooks.

## Yang belum

- Component-level schematic/routing/functional Gerber.
- Firmware integration/flash tests, Android device test, Docker/Postgres.
- Physical mains/thermal/PE/isolation tests.
- Engineering/regulatory sign-off.

## Tindakan manusia

- Pilih/verifikasi komponen & socket/plug/enclosure.
- Sediakan lab/engineer.
- Jalankan uji fisik.
- Review safety/regulatory.
- Jangan gunakan mains sebelum itu.
""",
}

for filename, content in TUTORIALS.items():
    (OUT / filename).write_text(content.strip() + "\n", encoding="utf-8")

index = ["# Tutorials — Index", "", "Dokumentasi untuk engineer pemula. Baca `00_READ_FIRST.md` terlebih dahulu.", ""]
for filename in sorted(TUTORIALS):
    title = TUTORIALS[filename].splitlines()[0].replace("# ", "")
    index.append(f"- [{title}]({filename})")
index += ["", "**Status:** `REV_A_PROVISIONAL`. Tidak ada tutorial yang mengizinkan energisasi mains oleh pemula."]
(OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
print(f"Wrote {len(TUTORIALS)} tutorials + index")
