# Phase 1 Engineering Report — REV_C_PSU_BOARD

**Date:** 15 November 2026
**Agent:** OpenCode (DeepSeek V4.1 Flash 1017)
**PRD:** v1.0
**Design revision:** `REV_C_PSU_BOARD`
**Phase 1 status:** `PARTIAL_PROVISIONAL` / `ENGINEERING_REVIEW_REQUIRED`
**Hardware status:** `HARDWARE_VALIDATION_REQUIRED`
**Fabrication:** `NOT_RELEASED`

---

## 1. Ringkasan eksekusi

Fase 1 menghasilkan artefak digital untuk bentuk produk inline smart outlet:
riset komponen, BOM riset + matriks pengadaan Indonesia bertanggal, GPIO map, 4 harness WireViz, KiCad block
schematic + routed 100?70 SELV carrier, CadQuery enclosure/assembly, firmware C core +
host tests, dan dokumen keselamatan. Tidak ada klaim siap fabrikasi atau siap
digunakan.

**Yang benar-benar lulus digital:**
- Firmware core: 75 checks, 0 failures.
- API/device simulator: 38 tests (termasuk command → MQTT → ACK).
- Web: build + 5 Playwright tests + axe login/dashboard.
- Static wiring/GPIO/BOM crosscheck: PASS.
- WireViz/CadQuery/KiCad-file parse: PASS.
- KiCad 10.0.8 ERC 0; routed SELV carrier DRC 0/0 at 0.15 mm; routed Gerber/drill/POS.
- ESP-IDF v6.1 target build: PASS; `.bin` exists (no flash).
- Android debug APK: PASS (arm64-v8a, v2 debug signature; no device test).

**Yang tetap BLOCKED:**
- Component-level schematic/connectivity/routing and functional Gerber.
- Firmware flash/boot-waveform, OTA/rollback test, sensor/network integration.
- Physical fit/thermal/PE/isolation/load tests.
- Android device/emulator test and release signing.
- Engineering/regulatory sign-off.

---

## 2. Keputusan pengguna (Q01–Q28)

Semua jawaban tercatat di `docs/decisions/USER_ANSWERS.md/.yaml`. Ringkasan:

| Area | Keputusan |
|---|---|
| Bentuk | Inline outlet berkabel (Q01=B) |
| Soket | Analisis kompatibilitas; lean Type E/F (Q02=D) |
| Arus | **8 A final / ~1.840 W** (amendment pengguna); elektronik/SMPS saja |
| Beban | Campuran elektronik/SMPS (Q04=B) |
| Pemutusan | Dua channel L/N, bukan DPST linked (Q05=A) |
| Ukuran | 220×120×70 CONFIRMED (Q06=C, 2026-11-15); 150×100/180×120 fail clearance |
| Budget | Rp500–750 ribu (Q07=B) |
| Board | ESP32-S3-DevKitC-1 N16R8 resmi (Q08=B) |
| Metering | Bandingkan; PZEM V4 provisional (Q09=D) |
| Relay | Modul optocoupler 2 channel off-board (amendment Q10) |
| Modul | Pilih berdasar isolasi/dimensi (Q11=D) |
| Safety | Prototipe lab (Q12=A) |
| UI | OLED kecil, RGB built-in + panel (Q13=A, Q14=C) |
| Provisioning | BLE + SoftAP fallback (Q15=C) |
| Offline | Fisik + jadwal + RTC (Q16=C) |
| Cloud | Hybrid, self-host first (Q17=C) |
| Akun | Sederhana, tenant-ready (Q18=D) |
| Notifikasi | Telegram first (Q19=A) |
| HA | MQTT Discovery (Q20=A) |
| Histori | Lokal pendek + cloud panjang (Q21=A) |
| Stack | Next.js + backend TS, Docker (Q22=A/C) |
| Firmware | ESP-IDF (Q23=A) |
| Android | Expo dev build (Q24=A) |
| Power restore | Default OFF (Q25=C) |
| Fasilitas | Hanya komputer (Q26=A) |
| Fase | Digital paralel, safety gate tetap (Q27=C) |
| Komponen | Belum ada (Q28=B) |

---

## 3. BOM dan persetujuan komponen

- `bom/BOM_MASTER.csv` - **57 baris**, BOM rekayasa; harga tidak dimasukkan ke BOM ini.
- `bom/BOM_PROCUREMENT.csv` - **57 baris daftar belanja prototype**, 40 baris punya listing bertanggal, 17 baris `ESTIMATED`.
- `bom/BOM_SUMMARY.json` - status `PROCUREMENT_PRICED_2026-11-16`; CORE Rp717.087, FULL Rp834.687.
- `bom/BOM_PROCUREMENT.md` - tabel CORE/FULL, harga, seller, URL, verdict budget.
- `bom/BOM_TOOLS_AND_TEST.csv` — 6 alat, belum dibeli.
- `bom/BOM_CONSUMABLES.csv` — 5 item.
- `bom/COMPONENT_APPROVALS.yaml` — tidak ada komponen `approved_for_fabrication`.
- `research/candidates.csv` — 45 kandidat.
- `research/COMPONENT_RESEARCH.md` — narasi, skor bukti, dan ringkasan sourcing.
- `research/PROCUREMENT_INDONESIA.md` — riset pemasok, harga, stok, risiko, dan skenario budget.
- `research/datasheets/MANIFEST.md` — 12 PDF tersimpan + hash (termasuk HLK-5M05), plus arsip PZEM V1.0 (docx/txt); sisanya link-only/licensed.

**Status safety-critical:**
- Socket/plug: `DOCUMENTATION_DEFICIENT` (Simon 16 A / BOSS BP16; sertifikasi/PE belum).
- PZEM V4: `DOCUMENTATION_DEFICIENT` (100 A closed CT Rp150.000; batch belum).
- Relay: modul optocoupler 2 channel off-board, 10 A class claim, dua SPDT independen (bukan DPST).
- PE hardware/enclosure: `BLOCKED`; 220×120×70 sudah dikonfirmasi (Q06=C), enclosure ABS exact-size Rp99.684 tetapi flame rating/material belum divalidasi.
- Fuse/MOV/TCO: `PENDING`/documentation deficient.

**Konsekuensi:** rating final 8 A/1.840 W; batas beban eksplisit. Dua channel module tidak mechanically linked; residual risk harus diuji. Budget CORE elektronik **tidak masuk** Rp750.000 (Rp757.087 all-in, ~Rp7.087 over); addendum mekanik ~Rp28k membuat marketplace ~Rp785.087 all-in, restock ~Rp733.619 (di bawah cap); FULL di atas budget.

### 3A. Riset pengadaan Indonesia (2026-11-15)

Riset harga mencakup 57 baris; 40 baris punya listing bertanggal dan 17 baris `ESTIMATED`. Detail ada di `research/PROCUREMENT_INDONESIA.md` dan `bom/BOM_PROCUREMENT.csv`.

| Konfigurasi | Subtotal | + ongkir Rp40.000 | Status |
|---|---:|---:|---|
| Elektronik inti | Rp433.633 | — | di dalam budget |
| CORE (safety/function minimum) | Rp717.087 | Rp757.087 | ~Rp7k di atas cap |
| CORE + mechanical addendum | Rp745.087 | Rp785.087 | ~Rp35k di atas cap |
| CORE dengan restock EasyWare | Rp665.619 | Rp705.619 | di bawah cap |
| FULL (+ OLED/RTC/RGB/konektor) | Rp834.687 | Rp874.687 | di atas budget |

**Keputusan:** ESP32-S3 N16R8 compatible Rp139.968 (deviasi Q08=B eksplisit), PZEM V4 100 A CT Rp150.000 dengan **isolasi internal** (tanpa ADuM/B0505S), HLK-5M05 Rp49.000, relay 2 channel Rp16.650, 74HCT125 + divider, **tanpa TMP102**, enclosure 220x120x70 Rp99.684, PCB carrier 100x70 routed. Harga listing bukan quote dan bukan approval; status safety tidak berubah.

---

## 4. Sumber dan trade-off utama

| Keputusan | Trade-off | Alasan |
|---|---|---|
| Inline box 220×120×70 | Lebih besar dari wall plug | Ruang side-by-side PZEM/relay/PSU + bracket; 150×100 dan 180×120 gagal clearance |
| Dua channel | Module off-board, dua SPDT independen, 10 A claim | Plug Type F reversibel; PE tidak diputus; bukan DPST linked |
| PZEM V4 + barrier UART | BOM/space tambahan | Modul belum terbukti isolated |
| HLK-5M05 | Kecil/murah, 38×23×18 mm | 5 V 1 A, 5 W; efficiency ~70%, isolation/cert batch unverified |
| ESP-IDF | Setup lebih berat | OTA rollback/security/provisioning |
| SQLite dev + Postgres target | Dua adapter | Tes lokal tanpa Docker; produksi belum |
| Synthetic demo | Bukan data nyata | Tidak ada hardware; label wajib |

---

## 5. Spesifikasi: proposed vs verified

| Parameter | Proposed | Verified? |
|---|---|---|
| Input | 230 VAC / 50 Hz | `PROVISIONAL` |
| Output target | **8 A / ~1.840 W** | Dipilih pengguna; thermal test required |
| Output kontinu provisional | 8 A | `UNVERIFIED` |
| Relay module | 2-channel optocoupler, off-board, 10 A class claim | `DOCUMENTATION_DEFICIENT` |
| Fuse | 10 A time-lag | `PENDING` |
| 5 V PTC/TVS (PSU board) | 1.1 A hold PTC + SMBJ5.0A on the PSU total output | `PROVISIONAL` |
| PSU | Hi-Link HLK-5M05, 5 V 1 A / 5 W | `PENDING_APPROVAL`; thermal/cert test |
| Socket/plug | Type F/E-F 16 A class | `DOCUMENTATION_DEFICIENT` |
| PE | Kontinu, tidak diputus | `PROVISIONAL` |
| Isolation | PZEM V4 internal optocouplers; 74HCT125/divider; no ADuM/B0505S | `DOCUMENTATION_DEFICIENT` |
| Enclosure | 220x120x70 CONFIRMED (Q06=C), ABS/PC FR; 150x100/180x120 rejected | `BLOCKED` (material/PE/fit) |
| Clearance/creepage | TBD | `BLOCKED` |

---

**Koreksi antarmuka DevKitC-1:** carrier memakai dua socket 1x22 dengan jarak baris **22,86 mm** (J1A=J1, J1B=J3). Socket 2x22 IDC sebelumnya tidak kompatibel secara fisik. Lihat `docs/decisions/ADR-015-DEVKITC-1-SOCKET.md`.

## 6. Arsitektur isolasi/proteksi

```
Mains: Plug → Fuse → MOV → Thermal cutoff → 2-channel relay module (L/N) → Socket
PE:    Plug PE ──────────────────────────────→ Socket PE (no relay/fuse)
PSU:   Mains → HLK-5M05 → 5 V SELV
Meter: PZEM V4 + CT around L → internal optocoupler → 74HCT125/divider → ESP32 UART
SELV:  ESP32 carrier → OLED/button/RGB/RTC; relay driver (no temperature sensor)
```

Detailed docs:
- `safety/ISOLATION_PLAN.md`
- `safety/ELECTRICAL_RATING_CHAIN.md`
- `safety/PROTECTION_COORDINATION.md`
- `safety/CLEARANCE_CREEPAGE_WORKSHEET.md`
- `safety/POLARITY_AND_EARTH_ASSESSMENT.md`
- `safety/THERMAL_RISK_AND_DERATING.md`
- `safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md`

---

## 7. Lokasi artefak

| Kategori | Path |
|---|---|
| Riset | `research/` |
| BOM | `bom/` |
| Datasheet | `research/datasheets/` |
| GPIO | `hardware/interfaces/gpio_map.*` |
| Wiring | `hardware/wiring/*.yaml`, `renders/` |
| KiCad | `hardware/kicad/smartplug.kicad_pro/.kicad_sch/.kicad_pcb` |
| PCB preview | `hardware/pcb/render/placement_preview.*` |
| CAD | `hardware/mechanical/source/`, `export/`, `render/`, `drawings/` |
| Firmware | `firmware/` |
| Safety | `safety/` |
| Validation | `validation/` |
| Reports | `reports/` |

---

## 8. ERC/DRC/toolchain commands dan status

**KiCad CLI:** `10.0.8` (portable extract `tools/kicad/bin/kicad-cli.exe`).

```powershell
$env:PATH = "$PWD\tools\kicad\bin;$env:PATH"
kicad-cli sch erc --output reports/kicad/erc.json hardware/kicad/smartplug.kicad_sch
kicad-cli pcb drc --output reports/kicad/drc.json hardware/kicad/smartplug.kicad_pcb
kicad-cli pcb export gerbers -o hardware/manufacturing/provisional/Gerber -l F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts hardware/kicad/smartplug.kicad_pcb
kicad-cli pcb export drill -o hardware/manufacturing/provisional/Drill --generate-map --map-format pdf hardware/kicad/smartplug.kicad_pcb
```

- ERC: **0 violations** on the block-level text-only schematic. This is not component-level connectivity.
- DRC: **0 violations / 0 unconnected** on the routed 100x70 SELV carrier (0.15 mm), 25 footprints (22 assembled + 3 fiducials), 18 nets; and on the routed 50x65 PSU board, 13 assembled + 3 holes + 3 fiducials, 8 nets.
- Gerber/drill/POS: **routed provisional** exported; `NOT_FOR_FABRICATION`.
- Native files parse with KiCad `pcbnew`: `PASS` (carrier 18 nets, PSU 8 nets).
- Production symbol-level schematic and vendor footprint review: `PENDING`; functional schematic/netlist and routed carrier exist.

---

## 9. Gambar dan render

- `docs/hardware/SYSTEM_ARCHITECTURE.png/.svg/.pdf`
- `hardware/wiring/renders/*.png/.svg/.pdf` (4 harness)
- `hardware/mechanical/render/*.png` (60 mm body + 10 mm lid, gasket, socket/gland/vent, top UI, USB cover, DevKit key)
- `hardware/mechanical/export/body_bottom_recommended.step/.stl`, `body_top_recommended.step/.stl`, `gasket`, `usb_cover`, `devkit_key`, `assembly_recommended.step`
- `hardware/mechanical/drawings/dimensions.svg`, `mounting_plan.svg`, `service_access.svg`, `assembly.pdf`
- `hardware/pcb/render/placement_preview.png/.svg`
- `docs/ui-ux/screenshots/*` (12 web screenshots)

All images are generated from actual files/models or clearly labeled as previews; none are photos of a physical prototype.

---

## 10. Assembly plan (digital)

`docs/tutorials/10_ASSEMBLY_PLANNING.md` and `hardware/mechanical/PRINT_PROTOTYPE_GUIDE.md`.

Order:
1. Incoming inspection/measurement.
2. Mechanical assembly without energy.
3. Low-voltage PCB/headers/OLED/button/RGB.
4. Mains modules off-board, PE stud, gland, terminals (qualified personnel).
5. Continuity/clearance/PE inspection.
6. Lab thermal/load/isolation tests.
7. Sign-off.

No mains assembly/energization was performed.

---

## 11. Firmware local

- Portable core: `firmware/core/smartplug_core.c`.
- Host tests: `firmware/test/host/test_core.c` — 75 checks.
- ESP-IDF minimal app: `firmware/main/app_main.c` — relay OFF at boot, button debounce, core state machine, ON blocked while sensors invalid.
- Partition/config: `firmware/partitions.csv`, `sdkconfig.defaults`.
- ESP-IDF build: `PASS` (v6.1, target esp32s3, 192.496-byte `.bin`, SHA-256 `498356348097F45F7853747C08037B05801D34BACAC65392BA466D857EFBCF0E`); build only, no flash.
- OLED/RGB/PZEM/Wi-Fi/MQTT/OTA components: `NOT_IMPLEMENTED`.
- Build evidence: `reports/FIRMWARE_BUILD.md`, `reports/logs/firmware-idf-build.log`.

Data model mirrors `DeviceState`, `Measurement`, `Health` in `packages/api-contract` and `packages/mqtt-contract`.

---

## 12. Hasil uji mock/digital

| Test | Result |
|---|---|
| Domain | 34 PASS |
| MQTT contract | 11 PASS |
| API + simulator | 38 PASS |
| Simulator | 4 PASS |
| Firmware core | 75 checks, 0 failures |
| Web build | PASS |
| Playwright | 5 PASS |
| axe login/dashboard | PASS (no serious/critical) |
| Static connectivity/GPIO/BOM | PASS |
| WireViz/CAD/KiCad parse | PASS |
| npm audit | 0 known vulnerabilities |

See `reports/TEST_MATRIX.csv` / `VALIDATION_SUMMARY.json`.

---

## 13. Physical blockers

| Blocker | Status | Next action |
|---|---|---|
| Board/ESP32-S3 physical revision | `BLOCKED` | Buy official board; photo/revision check |
| PZEM V4 batch/datasheet | `BLOCKED` | Obtain sample/official manual; measure |
| Relay/fuse/socket/PSU/terminal | `BLOCKED` | Approve MPNs/ratings |
| PE hardware/enclosure material | `BLOCKED` | Select rated parts |
| Clearance/creepage | `BLOCKED` | Licensed standard + engineer |
| Thermal/load/PE/isolation | `BLOCKED` | Qualified lab |
| ESP-IDF build | `PASS` (build only) | Flash/boot-waveform and integration still blocked |
| Android SDK/APK | `PASS` (debug) | arm64-v8a APK built; device install/UI test still pending |
| PostgreSQL/Docker | `BLOCKED` | Install, migrate, test |

---

## 14. Safety review

- No engineer/regulatory sign-off exists.
- `safety/REVIEW_SIGNOFF_TEMPLATE.md` is blank.
- FMEA is draft; residual risk register has high items.
- PE/isolation/thermal/relay weld are not physically validated.
- 3D print is prototype-only.
- **No claim of `READY_FOR_FABRICATION` or `READY_FOR_USE`.**

---

## 15. Kualitas per kategori Fase 1

| Category | Status | Evidence |
|---|---|---|
| 01 Riset komponen | `PARTIAL` | 45 candidates, 48 BOM rows; 39 priced listings + 9 estimates |
| 02 BOM | `PARTIAL` | Engineering BOM unpriced; dated procurement matrix CORE/FULL |
| 03 Datasheet | `PARTIAL` | 9+ PDFs hashed; PZEM/socket deficient |
| 04 Arsitektur | `PASS` (digital) | Diagram PNG/SVG/PDF |
| 05 Schematic | `PARTIAL` | Block text-only; ERC 0 but not component connectivity |
| 06 Wiring | `PASS` (render) | 3 harnesses; physical untested |
| 07 GPIO | `UNVERIFIED` | Static crosscheck; board revision unknown |
| 08 PCB | `PARTIAL` | Placement-only; DRC 0; routing blocked |
| 09 Manufacturing | `PARTIAL/BLOCKED` | Placement-only Gerber/drill; functional board blocked |
| 10 PCB visualization | `PARTIAL` | Placement preview only |
| 11 Enclosure 3D | `PARTIAL` | 220×120 confirmed PASS coarse; 150×100/180×120 rejected; brackets exported |
| 12 Enclosure render | `PARTIAL` | Renders/drawings recommended; no physical fit |
| 13 Firmware | `PARTIAL` | Core + ESP-IDF target build PASS; integration/flash blocked |
| 14 Firmware config | `PARTIAL` | Partitions/sdkconfig accepted by build; no flash |
| 15 Web | `PASS` (digital) | Build/E2E/axe |
| 16 Android | `PASS` (debug) | arm64-v8a APK built and signature-verified; not installed/tested |
| 17 Backend | `PASS` (digital) | 38 tests |
| 18 Database | `PARTIAL` | SQLite tested; Postgres schema only |
| 19 MQTT | `PASS` (digital) | Contract + aedes integration |
| 20 Notifications | `PARTIAL` | Mock test; Telegram not live |
| 21 Deployment | `BLOCKED` | Compose config only |
| 22 Testing | `PARTIAL` | 27 PASS / 11 BLOCKED (KiCad carrier + PSU, research, ESP-IDF build) |
| 23 Validation | `PARTIAL` | Static + ERC 0 + routed DRC 0/0 + Gerber; physical blocked |
| 24 Security | `PARTIAL` | Threat model/audit; gaps |
| 25 Docs | `PASS` (digital) | 26 tutorials + reports |
| 26 Handoff | `PARTIAL` | Manifest/report generated; blockers explicit |

---

## 16. Kesimpulan Fase 1

Fase 1 **belum** `DIGITAL_COMPLETE` karena schematic/routing komponen, integrasi firmware (PZEM/OLED/Wi-Fi/MQTT/OTA), uji perangkat Android, dan deployment belum selesai. ERC 0, DRC routed 0/0, Gerber routed, dan ESP-IDF v6.1 target build sudah `PASS` sebagai bukti digital. Yang dapat diklaim adalah **provisional digital completeness** untuk riset, BOM riset, wiring, CAD, firmware core, web/API, dan dokumentasi. Hardware tetap `ENGINEERING_REVIEW_REQUIRED` dan `HARDWARE_VALIDATION_REQUIRED`.
