# Phase 1 Engineering Report — REV_A_PROVISIONAL

**Date:** 15 November 2026
**Agent:** OpenCode (DeepSeek V4.1 Flash 1017)
**PRD:** v1.0
**Design revision:** `REV_A_PROVISIONAL`
**Phase 1 status:** `PARTIAL_PROVISIONAL` / `ENGINEERING_REVIEW_REQUIRED`
**Hardware status:** `HARDWARE_VALIDATION_REQUIRED`
**Fabrication:** `NOT_RELEASED`

---

## 1. Ringkasan eksekusi

Fase 1 menghasilkan artefak digital untuk bentuk produk inline smart outlet:
riset komponen, BOM riset (unpriced), GPIO map, 6 harness WireViz, KiCad block
schematic + placement-only PCB, CadQuery enclosure/assembly, firmware C core +
host tests, dan dokumen keselamatan. Tidak ada klaim siap fabrikasi atau siap
digunakan.

**Yang benar-benar lulus digital:**
- Firmware core: 74 checks, 0 failures.
- API/device simulator: 38 tests (termasuk command → MQTT → ACK).
- Web: build + 5 Playwright tests + axe login/dashboard.
- Static wiring/GPIO/BOM crosscheck: PASS.
- WireViz/CadQuery/KiCad-file parse: PASS.

**Yang tetap BLOCKED:**
- KiCad ERC/DRC/Gerber/drill.
- ESP-IDF target build, firmware `.bin`, OTA/rollback test.
- Physical fit/thermal/PE/isolation/load tests.
- Engineering/regulatory sign-off.

---

## 2. Keputusan pengguna (Q01–Q28)

Semua jawaban tercatat di `docs/decisions/USER_ANSWERS.md/.yaml`. Ringkasan:

| Area | Keputusan |
|---|---|
| Bentuk | Inline outlet berkabel (Q01=B) |
| Soket | Analisis kompatibilitas; lean Type E/F (Q02=D) |
| Arus | Target 10 A; rating final = nilai terendah (Q03=B) |
| Beban | Campuran elektronik/SMPS (Q04=B) |
| Pemutusan | Tinjau dua kutub (Q05=A) |
| Ukuran | ≤150×100×70 mm (Q06=B) |
| Budget | Rp500–750 ribu (Q07=B) |
| Board | ESP32-S3-DevKitC-1 N16R8 resmi (Q08=B) |
| Metering | Bandingkan; PZEM V4 provisional (Q09=D) |
| Relay | Studi 2–3 alternatif (Q10=C) |
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

- `bom/BOM_MASTER.csv` — **46 baris**, harga **kosong** (`UNPRICED`).
- `bom/BOM_SUMMARY.json` — `subtotal_idr: null`, `priced_lines: 0`, `unpriced_lines: 46`.
- `bom/BOM_TOOLS_AND_TEST.csv` — 6 alat, belum dibeli.
- `bom/BOM_CONSUMABLES.csv` — 5 item.
- `bom/COMPONENT_APPROVALS.yaml` — tidak ada komponen `approved_for_fabrication`.
- `research/candidates.csv` — 41 kandidat.
- `research/COMPONENT_RESEARCH.md` — narasi dan skor bukti.
- `research/datasheets/MANIFEST.md` — 9 PDF tersimpan + hash; sisanya link-only/licensed.

**Status safety-critical:**
- Socket/plug: `DOCUMENTATION_DEFICIENT`.
- PZEM V4: `DOCUMENTATION_DEFICIENT`.
- Relay 10 A DPST: tidak ditemukan; provisional RT2 8 A.
- PE hardware/enclosure: `BLOCKED`.
- Fuse/MOV/TCO: `PENDING`/documentation deficient.

**Konsekuensi:** target 10 A tidak tercapai oleh relay 8 A; rating final harus 8 A atau lebih rendah, atau ganti contactor/enclosure.

---

## 4. Sumber dan trade-off utama

| Keputusan | Trade-off | Alasan |
|---|---|---|
| Inline box 150×100×70 | Lebih besar dari wall plug | Ruang untuk PZEM/relay/PSU; prototype serviceable |
| Dua kutub | Relay lebih besar/mahal, rating 8 A | Plug Type F reversibel; PE tidak diputus |
| PZEM V4 + barrier UART | BOM/space tambahan | Modul belum terbukti isolated |
| IRM-05-5 | Harga lebih tinggi | Dokumen resmi, 5 V 1 A |
| ESP-IDF | Setup lebih berat | OTA rollback/security/provisioning |
| SQLite dev + Postgres target | Dua adapter | Tes lokal tanpa Docker; produksi belum |
| Synthetic demo | Bukan data nyata | Tidak ada hardware; label wajib |

---

## 5. Spesifikasi: proposed vs verified

| Parameter | Proposed | Verified? |
|---|---|---|
| Input | 230 VAC / 50 Hz | `PROVISIONAL` |
| Output target | 10 A | **Tidak tercapai** |
| Output kontinu provisional | 8 A atau lebih rendah | `UNVERIFIED` |
| Relay | TE RT2 DPST-NO 8 A class | `PENDING_APPROVAL` |
| Fuse | 10 A time-lag | `PENDING` |
| PSU | 5 V 1 A | `PENDING` |
| Socket/plug | Type F/E-F 16 A class | `DOCUMENTATION_DEFICIENT` |
| PE | Kontinu, tidak diputus | `PROVISIONAL` |
| Isolation | ADuM1201 + B0505S | `PENDING` |
| Enclosure | 150×100×70, ABS/PC FR | `BLOCKED` |
| Clearance/creepage | TBD | `BLOCKED` |

---

## 6. Arsitektur isolasi/proteksi

```
Mains: Plug → Fuse → MOV → Thermal cutoff → Relay DPST → Socket
PE:    Plug PE ──────────────────────────────→ Socket PE (no relay/fuse)
PSU:   Mains → IRM-05-5 → 5 V SELV
Meter: PZEM V4 + CT around L → ADuM1201/B0505S barrier → ESP32 UART
SELV:  ESP32 carrier → OLED/button/RGB/TMP102/RTC; relay driver
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

**KiCad CLI:** `NOT_INSTALLED`.

```powershell
kicad-cli sch erc --output reports/kicad/erc.json hardware/kicad/smartplug.kicad_sch
kicad-cli pcb drc --output reports/kicad/drc.json hardware/kicad/smartplug.kicad_pcb
```

- Status: `BLOCKED`.
- Native files parse with `kiutils`: `PASS`.
- Schematic is a **system block schematic**, not component-level.
- PCB is **placement-only** 75×50 mm, no routing/nets/footprints final.
- Gerber/drill: `BLOCKED`; `hardware/manufacturing/provisional/Gerber/README_BLOCKED.md`.

---

## 9. Gambar dan render

- `docs/hardware/SYSTEM_ARCHITECTURE.png/.svg/.pdf`
- `hardware/wiring/renders/*.png/.svg/.pdf` (6 harness)
- `hardware/mechanical/render/isometric.png`, `front.png`, `back.png`, `top.png`, `bottom.png`, `exploded.png`, `cutaway.png`
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
- Host tests: `firmware/test/host/test_core.c` — 74 checks.
- ESP-IDF minimal app: `firmware/main/app_main.c` — relay OFF at boot, button debounce, core state machine, ON blocked while sensors invalid.
- Partition/config: `firmware/partitions.csv`, `sdkconfig.defaults`.
- ESP-IDF build: `BLOCKED: ESP_IDF_NOT_INSTALLED`; no `.bin`.
- OLED/RGB/PZEM/Wi-Fi/MQTT/OTA components: `NOT_IMPLEMENTED`.

Data model mirrors `DeviceState`, `Measurement`, `Health` in `packages/api-contract` and `packages/mqtt-contract`.

---

## 12. Hasil uji mock/digital

| Test | Result |
|---|---|
| Domain | 34 PASS |
| MQTT contract | 11 PASS |
| API + simulator | 38 PASS |
| Simulator | 4 PASS |
| Firmware core | 74 checks, 0 failures |
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
| ESP-IDF build | `BLOCKED` | Install toolchain, build |
| Android SDK/APK | `BLOCKED` | Install SDK, build |
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
| 01 Riset komponen | `PARTIAL` | 41 candidates, 46 BOM rows, unpriced |
| 02 BOM | `PARTIAL` | CSV/MD/YAML/JSON; unpriced/unapproved |
| 03 Datasheet | `PARTIAL` | 9 PDFs hashed; PZEM/socket deficient |
| 04 Arsitektur | `PASS` (digital) | Diagram PNG/SVG/PDF |
| 05 Schematic | `PARTIAL/BLOCKED` | Native block schematic; ERC blocked |
| 06 Wiring | `PASS` (render) | 6 harnesses; physical untested |
| 07 GPIO | `UNVERIFIED` | Static crosscheck; board revision unknown |
| 08 PCB | `PARTIAL/BLOCKED` | Placement-only; DRC/routing blocked |
| 09 Manufacturing | `BLOCKED` | No Gerber/drill/DRC |
| 10 PCB visualization | `PARTIAL` | Placement preview only |
| 11 Enclosure 3D | `PARTIAL` | STEP/STL generated; dimensions approximate |
| 12 Enclosure render | `PARTIAL` | Renders/drawings generated; no physical fit |
| 13 Firmware | `PARTIAL` | Core built/tested; ESP-IDF blocked |
| 14 Firmware config | `PARTIAL` | Partitions/sdkconfig; no build |
| 15 Web | `PASS` (digital) | Build/E2E/axe |
| 16 Android | `PARTIAL` | Typecheck/bundle; APK blocked |
| 17 Backend | `PASS` (digital) | 38 tests |
| 18 Database | `PARTIAL` | SQLite tested; Postgres schema only |
| 19 MQTT | `PASS` (digital) | Contract + aedes integration |
| 20 Notifications | `PARTIAL` | Mock test; Telegram not live |
| 21 Deployment | `BLOCKED` | Compose config only |
| 22 Testing | `PARTIAL` | 19 PASS / 15 BLOCKED |
| 23 Validation | `PARTIAL` | Static checks; ERC/DRC blocked |
| 24 Security | `PARTIAL` | Threat model/audit; gaps |
| 25 Docs | `PASS` (digital) | 26 tutorials + reports |
| 26 Handoff | `PARTIAL` | Manifest/report generated; blockers explicit |

---

## 16. Kesimpulan Fase 1

Fase 1 **belum** `DIGITAL_COMPLETE` karena ERC/DRC/Gerber, ESP-IDF build, dan beberapa komponen firmware/PCB belum ada. Yang dapat diklaim adalah **provisional digital completeness** untuk riset, BOM riset, wiring, CAD, firmware core, web/API, dan dokumentasi. Hardware tetap `ENGINEERING_REVIEW_REQUIRED` dan `HARDWARE_VALIDATION_REQUIRED`.
