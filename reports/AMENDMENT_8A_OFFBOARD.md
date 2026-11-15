# Amendment — 8 A Final, Off-Board Modules, Toolchains

**Design revision:** `REV_A_PROVISIONAL`
**Date:** 2026-11-15
**Status:** `PARTIAL_DIGITAL` / `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED`
**Fabrication:** `NOT_RELEASED`

This report records the user-requested amendment after the initial handoff and
the toolchain work completed in this session. It supersedes earlier statements
where they conflict.

## 1. 8 A is sufficient for the declared load class

8 A × 230 V = **1,840 W** (approximately). That is enough for the declared
household electronics/SMPS class: TV, router, charger, small fan, lamps, and
similar. It is **not** a rating for heaters, kettles, irons, hair dryers,
large motors, or continuous mixed loads above 8 A.

The final rating remains the lowest verified value after thermal/lifecycle
testing. The number 8 A is a user decision, not a certification result.

## 2. Off-board PZEM and 2-channel relay module

- **PZEM-004T V4 split-CT**: off the PCB, on a 58 × 94 × 2 mm plate with four
  M3 holes and a cable-tie slot. The voltage terminals are still mains; the CT
  clamps around L only. UART is 5 V TTL and needs a level/isolation barrier.
  Official V4 batch documentation is still missing; the local archive is V1.0,
  not a V4 manual.
- **Common 2-channel 5 V optocoupler relay module**: off the PCB, on a
  55 × 26 × 2 mm plate. It is assumed active-LOW. One GPIO drives a MOSFET that
  pulls both IN1/IN2 low. The module contains two independent SPDT relays, **not
  a mechanically linked DPST**; one channel can weld while the other moves.
- Both modules stay in the mains zone. No mains trace or terminal is routed onto
  the SELV carrier. The carrier remains low-voltage only.
- The relay module's optocoupler does **not** provide galvanic isolation when
  VCC/GND are shared with the ESP32 side. Do not describe it as an isolation
  barrier or a safety-rated two-pole disconnect.

Study and sources: `research/OFFBOARD_MODULES.md`,
`research/datasheets/handsontec_2ch_relay.pdf`,
`research/datasheets/digikey_ts0010d_2ch_relay.pdf`,
`research/datasheets/pzem_004t_specification_archive.docx`.

## 3. Enclosure correction: 180 × 120 was a false PASS

The earlier 180 × 120 coarse check passed only because the relay was placed
directly above the PZEM with a 0.5 mm vertical gap, and because brackets were
excluded from the AABB test. That is not a usable assembly.

| Preset | Result | Reason |
|---|---|---|
| 150 × 100 × 70 | **FAIL** | relay/fuse/terminal clashes |
| 180 × 120 × 70 | **REJECTED** | PZEM/relay/socket stacking with ~0.5 mm gap; brackets/wiring ignored |
| 220 × 120 × 70 | **PASS (coarse)** | side-by-side PZEM and relay, barrier at x≈−30, brackets/wiring clearance |

The working enclosure is **220 × 120 × 70 mm**, **confirmed by the user on
2026-11-15 (Q06=C)**. The mechanical package includes the updated STEP/STL,
mounting plan, dimensions, fit report, and PZEM/relay brackets. This is still a
coarse digital fit, not a physical or thermal validation.

## 4. KiCad 10.0.8

| Check | Result | Scope |
|---|---|---|
| `kicad-cli sch erc` | **0 violations** | text-only system block schematic |
| `kicad-cli pcb drc` | **0 violations / 0 unconnected** | placement-only 75 × 50 mm carrier |
| Gerber/drill | **exported** | placement-only, `NOT_FOR_FABRICATION` |
| Component-level schematic/netlist | `BLOCKED` | no approved MPNs/footprints |
| Functional routing/Gerber | `BLOCKED` | placement only |

The ERC/DRC result is not proof of a functional circuit. It proves the generated
block/placement files parse and pass their limited checks. See
`reports/kicad/`, `hardware/kicad/README.md`, and
`hardware/manufacturing/provisional/`.

## 4A. PSU replacement — Hi-Link HLK-5M05

The user replaced the Mean Well IRM-05-5 with the **Hi-Link HLK-5M05**.

| Parameter | HLK-5M05 |
|---|---|
| Input | 90–264 VAC (rated 100–240) |
| Output | 5 VDC / 1 A / 5 W |
| Efficiency | ≥70% at 220 V full load |
| No-load | <0.1 W |
| Ripple | ≤70 mVp-p |
| Isolation | 2500 VAC input–output (datasheet claim) |
| Dimensions | **38 × 23 × 18 mm**, ~32 g, 4 pins |
| Pinout | 1/2 = AC, 3 = −Vo, 4 = +Vo |
| Operating temp | −20 to +60 °C |
| Protection | OCP 150–200%, short-circuit auto-recovery |

At 5 W output and 70% efficiency the module dissipates about **2.1 W**, higher
than the IRM-05-5. The smaller case and 60 °C limit make the enclosure thermal
test mandatory. The datasheet says “designed to meet” UL/CE, but the batch
certificate, isolation/leakage, creepage, and counterfeit status are
**unverified**. It is `PENDING_APPROVAL`, not a certified barrier.

Full study: `research/PSU_HLK_5M05.md`; datasheet:
`research/datasheets/hlk-5m05_distributor.pdf`.

## 5. ESP-IDF v6.1 target build

| Item | Value |
|---|---|
| Framework | ESP-IDF v6.1 |
| Target | esp32s3 |
| Toolchain | xtensa-esp-elf 15.2.0 / GCC 15.2.0 |
| Command | `powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1` |
| Result | **PASS** (exit 0) |
| Binary | `firmware/build/smartplug.bin` |
| Size | 192,464 bytes (0x2EFD0) |
| SHA-256 | `96BDF60D09D621F2D55DE1824B76BEB806F62D69277FAC1431BD7490BF9ABFC8` |
| Log | `reports/logs/firmware-idf-build.log` |
| Report | `reports/FIRMWARE_BUILD.md` |

This is a target build only. The board was not flashed; boot waveform, relay
timing, PZEM/OLED/Wi-Fi/MQTT/OTA integration, and bench tests remain blocked.

## 6. Android SDK / APK

Android command-line tools, platform 36/37, build-tools 36.0.0/37.0.0, NDK
27.1.12297006, CMake 3.22.1, and platform-tools were installed under
`D:\AI INSTALLS\Android\Sdk` to avoid filling C. Gradle uses
`D:\AI INSTALLS\gradle`.

| Item | Value |
|---|---|
| APK | `apps/android/android/app/build/outputs/apk/debug/app-debug.apk` |
| Size | 46,852,340 bytes |
| SHA-256 | `BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61` |
| ABI | arm64-v8a only |
| Signature | debug v2 verified |
| Build | `BUILD SUCCESSFUL in 21m 17s` |
| Log | `reports/logs/android-gradle-build.log` |
| Report | `reports/ANDROID_BUILD.md` |

The APK was not installed on a device/emulator, is not release-signed, and is
not production software. `SYSTEM_ALERT_WINDOW`/legacy storage permissions in
the debug manifest still need a production review.

## 7. Validation gate

`scripts/validate_all.py --e2e` final result: **23 PASS / 11 BLOCKED / 0 FAIL**.
The PASS count includes KiCad ERC/DRC/Gerber, the ESP-IDF target build, and all
existing software suites. The BLOCKED items are physical/lab, device-test,
PostgreSQL/Docker, and production MQTT/TLS checks. See
`reports/VALIDATION_SUMMARY.json`, `reports/TEST_MATRIX.csv`, and
`reports/FAILURES.md`.

## 8. Remaining blockers

- No approved component MPNs/footprints; no component-level schematic/routing.
- No physical PZEM/relay sample measurement, bracket fit, cable-bend, or
  tolerance-stack validation.
- No 8 A thermal, inrush, lifecycle, or per-channel weld test.
- No PE continuity, hipot, creepage/clearance, or isolation review.
- No flashed firmware, boot-waveform, or bench test.
- No production/release APK, release signing, or device/emulator installation test.
- No PostgreSQL/Docker deployment or MQTT TLS/ACL production test.
- No engineering/regulatory sign-off.

**Conclusion:** the 8 A decision is internally consistent for the declared
electronics/SMPS scope, and the digital package now includes KiCad checks, an
ESP-IDF build, and (if the APK build succeeds) an Android debug artifact. None
of this is a mains safety release. Do not fabricate or energize the prototype
without the stated reviews and physical tests.
