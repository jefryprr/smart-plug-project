# Changelog / Commit Rationale

**Design revision:** `REV_A_PROVISIONAL`
**Rule:** This is a human-readable summary. `git log` is the authoritative history.

| Commit | Change | Why | Tests | Compatibility/consequence |
|---|---|---|---|---|
| `cf37769` | Initial digital engineering package | Establish requirements, decisions, domain/API/web/simulator, hardware docs, CAD, firmware core | Domain/MQTT/API/simulator/C core/web E2E | Baseline; no hardware validation |
| `db9df6f` | Remove debug artifact; fill FR table | Clean repo; make 80 FR traceable in handoff | Document check | No code behavior change |
| `aa66f05` | Finalize FR table | Traceability in final report | 80 rows checked | No behavior change |
| `07bd661` | Add manifest/docs index/assembly docs | Complete 26 categories and handoff | Manifest 26 categories | No behavior change |
| `811ec7c` | Refresh manifest hashes | Align with source commit | SHA-256 recompute | Hash-only |
| `280eec1` | Add `.gitattributes` eol=lf | Reproducible hashes across Windows clone | Clone test | Line endings normalized; code unchanged |
| `fd87613` | Normalize tracked text to LF | Clone hash reproducibility | Clone compare | Line endings only |
| `2d3a193` | Set manifest source commit | Accurate handoff metadata | Clone compare | Hash metadata only |
| `8e63d9e` | Finalize validation/E2E wrappers/artifacts | Make `npx playwright test` and `validate_all --e2e` self-contained; regenerate artifacts | 19 PASS / 15 BLOCKED / 0 FAIL | E2E wrappers build deps if missing; no API contract change |
| `231595e` | Update final report source commit | Accurate report metadata | Document check | No behavior change |
| `92d63f4` | Refresh manifest | Align report hash | SHA-256 recompute | Hash-only |
| `d940d40` | Normalize generated text + manifest | Reproducible generated artifacts | Clone compare | Text encoding only |
| `ff8dff4` | Normalize test logs | Reproducible log hashes | Clone compare | Log encoding only |
| `6ac7219` | Add manifest note | Clarify source commit semantics | Document check | No behavior change |
| `c9a5c4c` | Include simulator tests in root `npm test` | Root test should cover all digital suites | 4 simulator tests PASS | No API change |
| `e691081` | Refresh manifest source commit | Metadata | Clone compare | Hash-only |
| `8241f43` | Add procurement QC, schematic wrapper, generator lockfile | Complete PRD 06.5/08.2 paths | Wrapper run; lockfile generated | No behavior change |
| `c5fd35c` | Normalize KiCad/lockfile line endings | Fresh-clone hash match | 127/127 artifacts match | Line endings only |
| uncommitted | 8 A final + off-board PZEM/2-channel module; KiCad 10.0.8 checks; ESP-IDF v6.1 build; 220×120 enclosure correction; Android debug APK | User amendment and toolchain completion | ERC 0, DRC 0, ESP-IDF build PASS, APK PASS, final gate in `VALIDATION_SUMMARY.json` | 150/180 enclosures rejected; debug APK is not release |

## Test status at handoff

- Digital gate after amendment: 23 PASS / 11 BLOCKED / 0 FAIL (baseline was 19 PASS / 15 BLOCKED).
- Requirements: 28 PASS / 25 PARTIAL / 24 NOT_STARTED / 3 BLOCKED.
- No `READY_FOR_FABRICATION` or `READY_FOR_USE`.

## Compatibility notes

- API/MQTT schema version 1; no breaking change after initial package.
- GPIO map remains `UNVERIFIED` (board revision not physical).
- KiCad/ESP-IDF/Android/Postgres toolchain fixes do not change digital contract.
- Regenerating CAD/KiCad changes UUIDs/hashes; regenerate manifest afterward.
