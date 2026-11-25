# Deep Hardware, Schematic, and Wiring Review

**Project:** ESP32-S3 IoT Smart Plug  
**Design revision:** `REV_D_CORE_ONLY`  
**Review date:** 2026-11-24  
**Review type:** static engineering review of hardware, schematic, PCB, wiring, BOM, and interfaces  
**Status:** `NOT_BUILDABLE_AS_IS` / `ENGINEERING_REVIEW_REQUIRED` / `HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_MAINS_USE`

> **Safety boundary**
>
> This review is a desktop review. No mains energization, hipot, thermal, load,
> relay lifecycle, EMC, surge, IP, or PE continuity test was performed. Nothing
> in this document authorizes 230 VAC use, fabrication release, or a “ready for
> use” claim. Mains work must be defined and performed by competent personnel
> under a lab procedure.

---

## 1. Executive verdict

The project has a coherent **concept**, a routed SELV carrier, a routed mains-entry
PSU board, a documented protection order, and a serious safety documentation
set. That is a good foundation.

It is **not yet a buildable mains device**. The main reasons:

1. The PZEM voltage-sense L/N connection is missing from the wiring harness.
2. The protective-earth stud is described in the safety documents but bypassed
   in the actual harness.
3. The fuse and thermal cutoff are single-pole, while the selected Type F plug
   is reversible. Protection can end up in the neutral conductor.
4. There is no component-level schematic. The KiCad “schematic” is a block
   diagram; the PCB netlists are manually generated in Python.
5. The relay module is a generic active-LOW assumption with two independent
   SPDT channels and no populated feedback. A welded channel can leave one
   conductor live.
6. The isolation case relies on one PZEM internal barrier and one HLK barrier,
   neither of which has batch/hipot evidence.
7. Creepage/clearance, thermal rise, fuse-clip/terminal heating, and the 8 A
   path are not proven.
8. The enclosure has local mechanical collisions that the AABB fit check does
   not catch.

**Overall buildability scorecard**

| Area | Status | Meaning |
|---|---|---|
| Requirements and ratings | `PARTIAL` | 8 A / 1840 W decision exists; evidence incomplete |
| System architecture | `PARTIAL` | Concept clear; PZEM voltage sense missing |
| Component-level schematic | `FAIL` | Block diagram only |
| PCB layout | `PARTIAL` | Routed, DRC 0/0, but no schematic parity and ignored checks |
| BOM | `PARTIAL` | Many stale/duplicate/unused lines |
| Wiring harness | `FAIL` | PZEM L/N and PE stud missing; CT location not specified |
| Isolation/safety case | `BLOCKED` | Single barrier, no hipot, no creepage calculation |
| Thermal/protection | `BLOCKED` | No 8 A closed-box test; TCO placement/clamping open |
| Mechanical enclosure | `PARTIAL` | Concept fits globally; local interfaces collide |
| Firmware/hardware interface | `PARTIAL` | GPIO map consistent; relay polarity/HIL unverified |
| Manufacturing/test readiness | `BLOCKED` | No assembly drawing, test points, or released test plan |
| Regulatory | `BLOCKED` | Classification and applicable standards still open |

**Verdict:** use this as a **review baseline**, not as a fabrication package.
The SELV carrier can be developed on the bench with low voltage. The mains PSU
board and the complete device should not be fabricated or energized until the
P0 items in section 8 are closed.

---

## 2. What the design is supposed to do

### 2.1 Power and switching intent

```text
Type F plug L/N/PE
  -> PSU board TB1
  -> F1 10 A 250 VAC time-lag fuse (L only)
  -> MOV1 275 VAC (L-N)
  -> TF1 SF96E 99 C thermal cutoff (L only)
  -> TB2 L/N
  -> relay module CH1 (L) and CH2 (N)
  -> Type F socket L/N
  -> load

HLK-5M05 AC input from L_LOAD/N_MAINS
  -> +5 V -> F2 1.1 A PTC -> D1 SMBJ5.0A TVS
  -> J5 carrier / J6 relay / J7 PZEM (conditional)

PZEM-004T V4:
  voltage sense L/N (intended)
  CT around L only
  5 V/GND from J7
  TX/RX through 74HCT125 and 10k/20k divider
```

### 2.2 Ratings and assumptions

| Item | Value | Status |
|---|---|---|
| Mains | 230 VAC, 50 Hz | Design input |
| Final load rating | 8 A / ~1840 W, electronics/SMPS only | User decision; not tested |
| Relay module | 2-channel, 5 V, active-LOW assumed, 10 A vendor claim | `DOCUMENTATION_DEFICIENT` |
| Fuse | 10 A, 250 VAC, time-lag, 1500 A interrupting (datasheet) | `PENDING_APPROVAL` |
| TCO | SF96E 99 C RFT, 84 C holding, 10 A / 250 VAC | `PROVISIONAL` |
| PSU | HLK-5M05, 5 V / 1 A / 5 W | Batch/certificate unverified |
| PZEM | PZEM-004T V4, 100 A CT | Batch/isolation unverified |
| Enclosure | 220 x 120 x 70 mm, 3D printed ABS/PC FR target | Material/UL94 unverified |

---

## 3. Findings summary

Severity:

- `BLOCKER`: must be fixed before any mains fabrication or energization.
- `HIGH`: must be fixed before a prototype build or before claiming a function.
- `MEDIUM`: fix before fabrication/review; may cause rework.
- `LOW`: documentation/consistency cleanup.

| ID | Severity | Area | Finding | Evidence | Required action |
|---|---|---|---|---|---|
| C-01 | `BLOCKER` | Wiring | PZEM voltage-sense L/N is not connected anywhere | `metering_harness.yaml` has U2 L/N labels but no connections; `WIRING_CONNECTIONS.csv` has no U2:L/U2:N | Add fused PZEM L/N from TB2 L/N (before relay) to PZEM; update harness/render |
| C-02 | `BLOCKER` | PE | PE stud is bypassed; harness goes plug PE directly to socket PE | `main_harness.yaml` connection 6; `CONNECTIVITY_DIFF.json` pe members `P1:PE, WPE, X1:PE` | Decide stud vs direct PE; if stud, wire P1:PE -> stud -> X1:PE and add test point |
| C-03 | `BLOCKER` | Protection | F1 and TF1 are in L only; Type F plug is reversible, so protection can be in N | `psu/netlist.csv` F1/TF1 L path only; `POLARITY_AND_EARTH_ASSESSMENT.md` reversible plug | Use 2-pole breaker/fuse/TCO arrangement or a non-reversible plug, with engineer approval |
| C-04 | `BLOCKER` | Schematic | No component-level schematic; KiCad is a text/label block diagram | `hardware/kicad/README.md`; `psu_drc.json` schematic_parity empty; PCB nets in Python | Draw symbol-level schematics, assign footprints, ERC, import netlist, PCB parity |
| C-05 | `BLOCKER` | Relay | Active-LOW and contact behavior are assumptions; two SPDT channels are not linked; no feedback populated | `board_config.h`; `OFFBOARD_MODULES.md`; `gpio_map.yaml`; `main_harness.yaml` | Verify exact module; test each channel; add feedback or use mechanically linked DPST |
| C-06 | `BLOCKER` | Isolation | Single PZEM internal barrier plus single HLK barrier; no batch/hipot/leakage evidence | `ISOLATION_PLAN.md`; `PZEM_INTERNAL_ISOLATION.md`; ADR-016 | Batch inspection + hipot; fallback external ADuM/B0505S if PZEM fails |
| C-07 | `BLOCKER` | Creepage | No IEC 60664-1 calculation; 2 mm slot and 6-12 mm spacing are provisional; terminals are 250 V | `CLEARANCE_CREEPAGE_WORKSHEET.md`; `research/PSU_BOARD_EVIDENCE.md` | Engineer calculation with OVC/PD/material/altitude; upgrade 300 V terminals |
| C-08 | `BLOCKER` | Thermal | 8 A closed-box thermal, fuse clip, terminal, TCO, HLK, relay not tested; TCO not clamped | `THERMAL_CALCULATION.md`; `PSU_BOARD_EVIDENCE.md`; PSU footprint | 8 A/40 C test; clamp TCO to hottest spot; derate or redesign if >84 C |
| C-09 | `BLOCKER` | Mechanical | Relay shelf, USB cover, and gasket collide with body/lid local features | Local CadQuery boolean check: 92.3 mm3, 845.5 mm3, 2592 mm3 | Fix interfaces before printing final body |
| H-01 | `HIGH` | Metering | CT conductor/location/direction not specified; 100 A CT at 8 A accuracy unknown | `metering_harness.yaml`; `OFFBOARD_MODULES.md` | Specify L-only, after relay, direction arrow, calibration |
| H-02 | `HIGH` | 5 V | DevKit 5 V pin is tied to PSU J5; USB may backfeed the PSU rail | `carrier/netlist.csv` J1A pin 21; DevKit schematic not checked | Verify DevKit diode; add ideal diode/Schottky or service rule |
| H-03 | `HIGH` | Mechanical | Button, RGB window, and USB opening have no verified mount/light pipe/alignment | `enclosure.py`; `components.py`; no bracket in BOM | Add button bracket, light pipe, USB cable route; verify |
| H-04 | `HIGH` | BOM | Duplicate D1, unused enclosure/standoffs/HLK plate, M3x8 qty, PE terminal mismatch | `BOM_ELECTRICAL.csv`; `BOM_PROCUREMENT.csv`; `MECHANICAL_BOM.csv` | Clean BOM, one D1, update quantities, remove unused lines |
| H-05 | `HIGH` | PCB | DRC ignores courtyard/via/footprint checks; no schematic parity; footprint review incomplete | `psu_drc.json`; `carrier_drc.json`; `fabrication_notes.md` | Rerun with all checks; vendor footprint review; assembly courtyard |
| H-06 | `HIGH` | Cable | NYYHY 3x1.5 is not a flexible cord; ferrules/strain relief/torque not specified | `main_harness.yaml`; BOM E-039 | Use H05VV-F 3G1.5 or engineer-approved cord; ferrules; anchor |
| H-07 | `HIGH` | Plug | Plug row says 2P, socket says 2P+E; PE contact unverified | BOM E-035 vs E-034 | Confirm 2P+E plug; measure PE contact |
| H-08 | `HIGH` | Fuse holder | Open 10 A clips at 8 A are marginal; not touch-proof | `PSU_BOARD_EVIDENCE.md` E-06 | Closed holder or thermal test + tool-access label |
| H-09 | `HIGH` | Testability | No 5 V/GND/PZEM/relay/PE test points; no assembly drawing or test plan | Carrier/PSU PCB; docs | Add test points and assembly/test drawing |
| H-10 | `HIGH` | Material/IP | ABS/PC FR certificate, gasket leak, IP44, impact unverified | `ENCLOSURE_MATERIAL_REVIEW.md` | Material certificate; leak/IP/impact test |
| H-11 | `HIGH` | Firmware | Relay active level, boot waveform, PZEM UART, no-feedback behavior not HIL-tested | `board_config.h`; validation only host tests | Low-voltage HIL fixture; boot-safe waveform |
| H-12 | `BLOCKER` | Regulatory | No product classification, EMC/surge, label/manual, lab report | `REGULATORY_PLAN_INDONESIA.md` | Engineer/regulatory review; do not market |
| M-01 | `MEDIUM` | PZEM | 100 A CT at 8 A is 8% of range; accuracy/phase error unknown | `OFFBOARD_MODULES.md` | Calibrate against reference; document accuracy |
| M-02 | `MEDIUM` | PSU fab | 2 oz Cu / 0.5 mm clearance capability and stackup not quoted | `fabrication_notes.md` | Fab quote + stackup + DFM review |
| M-03 | `MEDIUM` | Docs | Carrier footprint count inconsistent (23 vs 25; 16 vs 22 assembled) | `README.md` vs `fabrication_notes.md` | Correct docs and BOM |
| M-04 | `LOW` | Docs | Old 180 mm/58x94 references remain in some research files | `research/OFFBOARD_MODULES.md` etc. | Update or mark historical |

---

## 4. Critical findings in detail

### C-01 PZEM voltage-sense L/N is missing

The metering harness defines the PZEM connector with `L` and `N` pins:

```yaml
U2:
  type: PZEM-004T V4
  pinlabels: [L, N, CT_P, CT_N, +5V, GND, TX, RX]
```

But the `connections:` list only connects:

- CT_P/CT_N,
- +5V/GND,
- TX/RX.

There is no connection for `U2:L` or `U2:N`. `validation/WIRING_CONNECTIONS.csv`
confirms this: no `U2:L`/`U2:N` rows exist.

Why the static check still says `PASS`: `validate_connectivity.py` builds a net
for every node that appears in a connection. `U2:L` and `U2:N` never appear, so
they are simply absent. The isolation check looks for a net that contains both
a PZEM mains node and a PZEM TTL node; an unconnected mains node cannot fail
that test. This is a false PASS caused by missing connections, not by correct
isolation.

**Consequence:** as documented, the PZEM has no voltage sense and cannot measure
voltage. If someone wires L/N ad hoc,
the location is undefined: before the fuse, after the fuse, before the relay,
or after the relay. Each choice changes safety and metering behavior.

**Required fix:**

- Add a fused PZEM voltage sense from **TB2 L/N** (after F1/TF1, before the
  relay) to PZEM L/N.
- Keep the PZEM in the mains zone.
- Use ferrules and a dedicated 2-pin terminal or a properly rated splice.
- Add the connection to the harness, render, and validation script.
- Add a check that fails if `U2:L` or `U2:N` is floating.

### C-02 PE stud is bypassed

The safety documents and architecture say:

```text
Plug PE -> dedicated PE stud/terminal -> socket PE
```

The actual main harness says:

```yaml
- [P1: PE, WPE: [1], X1: PE]
```

The PE stud is not in the net. `CONNECTIVITY_DIFF.json` reports:

```json
"members": ["P1:PE", "WPE:1", "X1:PE"]
```

This means the PE path is continuous from plug to socket, but the dedicated
stud/test point is unused. The enclosure has a PE boss at `(45,50)` with a
4.3 mm blind hole, and the BOM has a DIN-rail PE terminal plus a stud kit. The
mechanical, electrical, and BOM descriptions do not agree.

**Consequence:** either the stud is unnecessary (then remove it from the safety
case and enclosure), or the harness is incomplete (then the PE bond/test point
is missing). Both cannot be true.

**Required fix:**

- Decide the PE architecture. For a plastic Class II PSU with a Class I socket,
  a direct plug-to-socket PE is electrically sufficient, but a test point and
  strain-relieved terminal are still good practice.
- If the stud is kept, wire `P1:PE -> stud -> X1:PE`, use a ring terminal, lock
  washer, and test point, and add it to the harness and continuity check.
- If the stud is removed, delete the enclosure boss and BOM line or mark them
  as future/optional.

### C-03 Single-pole fuse and TCO on a reversible plug

The PSU board puts F1 and TF1 in the L conductor only:

```text
TB1 L -> F1 -> MOV -> TF1 -> TB2 L
TB1 N -> TB2 N
```

The selected Type F (Schuko) plug can be inserted in either orientation. The
safety assessment acknowledges this and chooses two-pole **relay** switching,
but the fuse and TCO remain single-pole.

**Consequence:** in a reversed plug, the fuse and TCO are in the neutral
conductor. A L-to-PE fault or a L-side overcurrent may not be cleared by the
fuse. The relay may still open both poles, but a welded or failed channel can
leave L connected. The fuse/TCO coordination is no longer valid.

**Required fix (engineer decision):**

- Use a 2-pole breaker/fuse arrangement, or a 2-pole thermal disconnect, or
- use a non-reversible plug/socket architecture with a documented polarity, or
- prove that the selected protection remains effective in both orientations
  under the applicable standard.

This is not a “software” problem. It is a mains protection architecture
decision.

### C-04 No component-level schematic

`hardware/kicad/README.md` states:

> “The KiCad schematic is a system block schematic (text/labels), not a
> symbol-level production schematic.”

The PCB netlists are defined in Python:

- `scripts/generate_carrier_pcb.py` has a `NETS` dictionary.
- `scripts/generate_psu_pcb.py` assigns pads to nets manually.

`reports/kicad/psu_drc.json` has `"schematic_parity": []`. The ERC report has
0 violations because there are no component symbols to check.

**Consequence:** a wrong net in the Python dictionary will not be caught by
ERC. The PCB can be DRC-clean and still electrically wrong. A fabricator or
reviewer cannot review the circuit from a normal schematic. The BOM, netlist,
and PCB are only as good as the script.

**Required fix:**

- Draw a real symbol-level schematic for the carrier and the PSU board.
- Assign footprints and reference designators.
- Run ERC on the real schematic.
- Import the netlist into the PCB (or run a formal parity check).
- Add test points and no-connect flags.
- Review the schematic against `netlist.csv`, `gpio_map`, and the wiring YAML.

### C-05 Relay module assumptions

The firmware and hardware assume:

- active-LOW inputs,
- two independent SPDT channels,
- both channels driven by one AO3400,
- CH1 switches L, CH2 switches N,
- relay OFF at boot via 100 kΩ gate pulldown,
- no contact feedback populated.

The module is a generic “10 A class” board. Its exact relay brand, contact
arrangement, input polarity, JD-VCC behavior, and contact rating are not
verified. A module with active-HIGH inputs would turn the relay ON when the
MOSFET is OFF, which is the opposite of the boot-safe intent.

The two channels are not mechanically linked. If one channel welds, the other
can still open. The load may remain connected to one live conductor. The
firmware cannot observe this because GPIO11 feedback is optional and not
populated.

**Required fix:**

- Test the exact module: active-LOW/HIGH, JD-VCC, COM/NO/NC continuity.
- Test each channel separately for weld/stuck-closed.
- Add contact feedback or use a mechanically linked DPST relay/contactor.
- If feedback is not added, never claim “physically OFF”; use “commanded OFF”
  and require an external disconnect.
- Test 8 A continuous and SMPS inrush.

### C-06 Single isolation barrier

The design uses:

- HLK-5M05 isolation (datasheet claim),
- PZEM-004T V4 internal optocouplers (module-level evidence),
- no external ADuM1201/B0505S.

Both are single barriers. The PZEM TTL side shares SELV ground with the ESP32.
If the PZEM optocoupler or creepage fails, mains can reach the ESP32, the USB
connector, and the user.

The `ISOLATION_PLAN.md` status is `BLOCKED_PENDING_ENGINEER_REVIEW`. There is no
hipot/leakage test, no batch inspection, and no certificate.

**Required fix:**

- Inspect the purchased PZEM batch for optocouplers/creepage.
- Hipot/leakage test mains-to-TTL.
- Hipot/leakage test HLK input-to-output.
- If the batch fails, add the external ADuM1201/B0505S barrier and revise the
  carrier/PSU.
- Keep USB disconnected while mains is present, and label it.

### C-07 Creepage/clearance and terminal ratings

The PSU board uses:

- 2 mm routed isolation notch,
- 4 mm L/N traces,
- 6-12 mm provisional spacing,
- 5.08 mm terminal blocks rated 250 V,
- 0.5 mm DRC clearance on the PSU board.

The clearance worksheet is `BLOCKED_INPUTS_INCOMPLETE`. OVC, pollution degree,
material group, altitude, coating, and the applicable standard are not fixed.
The terminal blocks are below the user’s ≥300 V target.

**Required fix:**

- Engineer calculates clearance/creepage per IEC 60664-1 (or the applicable
  standard) with the final OVC/PD/material/altitude.
- Upgrade TB1/TB2 to ≥300 V rated parts if required.
- Review the HLK bridge, fuse clips, TCO, and terminal spacing.
- Do not treat DRC 0/0 as a clearance proof.

### C-08 Thermal and TCO placement

The thermal estimate is 13-19 W and 18.5-27.6 K rise. The TCO is an axial part
on the PCB, not clamped to the HLK, fuse clip, or terminal. The BOM note says it
“must be mechanically clamped to the hottest terminal/HLK/PCB spot”, but the
footprint has no clamp.

The fuse clips are 10 A at 8 A continuous; the terminal blocks are 17.5 A but
250 V; the HLK is ~70% efficient; the relay contacts are a vendor claim. The
closed enclosure has no vent.

**Required fix:**

- 8 A / 40 C closed-enclosure thermal test.
- Measure relay body/contacts, fuse clips, TB1/TB2, TCO, HLK, PZEM, enclosure
  air, and lid.
- Clamp/position the TCO at the hottest spot; verify <84 C holding with margin.
- Derate or redesign if any hotspot exceeds the engineer-approved limit.
- Do not add a vent without thermal/IP review.

### C-09 Mechanical local collisions

The global AABB fit check is `PASS`, but local boolean checks show:

| Interface | Overlap |
|---|---:|
| Relay shelf vs wall bosses | **92.3 mm3** |
| USB cover vs body bosses | **845.5 mm3** |
| Gasket vs lid ring at z=60 | **2592 mm3** |

The gasket also contacts the body rim by only about 0.5 mm. The socket cutout is
round 45.6 while the requested cutout was 45.6 x 45.6; a square 40 x 40 socket
body will not pass through the round hole. The PE boss is a blind plastic hole.
The DevKit key holes are offset from the carrier inserts.

**Required fix:** see `PANDUAN_LENGKAP_ENCLOSURE.md`. Do not print the final
body until these interfaces are revised and rechecked.

---

## 5. High-priority findings

### 5.1 PZEM CT location and accuracy

The harness shows the CT connected to the PZEM, but not which conductor or
where. The requirement is L only, never L and N together. The CT should be on
the load L conductor after the relay so it measures load current, not HLK
current. Add a direction arrow and a single-conductor guide.

The 100 A CT at 8 A is 8% of range. Accuracy and phase error at low current are
unverified. Calibrate against a reference meter; do not claim revenue accuracy.

### 5.2 5 V backfeed through the DevKit USB

The carrier connects the DevKit `5V` pin to the PSU J5 rail. If the DevKit has
no blocking diode, USB 5 V can backfeed the PSU output, the HLK output, the
relay module, and the PZEM. The design says “no USB while mains is energized”,
but USB with mains off can still backfeed the 5 V rail.

**Action:** verify the DevKit schematic; add an ideal diode/Schottky or a
service disconnect if backfeed is possible. Label the USB port.

### 5.3 Button, RGB, and USB mechanical interface

- The button is a panel switch on the lid, connected to carrier J6. The lid has
  a 12 mm hole but no switch bracket/retention. The 15 mm cap must reach the
  lid; verify.
- The RGB window is on the left wall; the DevKit LED is inside. A light pipe or
  diffuser is not modeled. The 5 mm hole may leak.
- The USB opening is on the front wall; the DevKit USB ports face along the
  board axis inside. Direct plug access is not aligned; an internal USB cable
  and strain relief are required.

### 5.4 BOM inconsistencies

- `D1` is used twice: E-015 1N4007 flyback and E-051 SMBJ5.0A TVS. The PSU board
  uses SMBJ5.0A; the 1N4007 is not on the board. Remove the duplicate/unused
  line or rename it.
- `E-037` MG Duradus enclosure (Rp99,684) is still in the BOM/procurement and
  BOM summary, but the user is 3D printing. The Shopee list has the enclosure at
  zero cost. The generic BOM overstates spend and may cause an unnecessary
  purchase.
- `E-046` nylon standoffs are not used (direct insert mounting).
- `E-010A/B` printed brackets duplicate the mechanical BOM.
- `E-044` M3x8 is one pack of 10, but 13 are used. The Shopee list has 2 packs;
  the generic BOM does not.
- `E-030` is a DIN-rail PE terminal, while the enclosure has an M4 stud boss.
  The mechanical and electrical PE hardware do not match.
- `E-035` plug says 2P; the socket says 2P+E. Confirm the plug has a PE contact.
- `E-029/E-055` terminal blocks are 250 V, below the ≥300 V target.
- `E-015` flyback diode is likely unnecessary for the module; verify.

### 5.5 DRC and footprint review

`psu_drc.json` ignores:

- missing courtyard,
- track not centered on via,
- footprint filter mismatch,
- footprint type mismatch.

These are exactly the checks that catch assembly and footprint problems.
`carrier_drc.json` ignores the same. The carrier fabrication notes also say 25
footprints/22 assembled, while the README/BOM say 23/16. Fix the documentation
and rerun DRC with all checks.

### 5.6 Cable, ferrules, and strain relief

The mains cord is NYYHY 3x1.5, which is a building wire, not a flexible cord.
For a plug-in device, use H05VV-F 3G1.5 or an engineer-approved equivalent.
Add ferrules, correct torque, a cable anchor inside the enclosure, and a bend
radius check. The gland provides strain relief at the wall, but the internal
wires to TB1 must not pull on the terminal block.

### 5.7 Fuse holder and touch protection

The PSU board uses open 5x20 fuse clips rated 10 A/250 V. At 8 A continuous,
the clips are marginal. The fuse is accessible only by opening the lid, but the
clips are not touch-proof. Use a closed holder if the footprint can change, or
add a tool-access label and thermal test.

### 5.8 Test points and assembly

There are no dedicated test points for:

- +5 V,
- GND,
- PZEM TX/RX,
- relay gate,
- PE.

Add them to the carrier/PSU. Add an assembly drawing with connector pin 1,
polarity, torque, and wire colors. Add a low-voltage bring-up procedure and a
mains lab test plan.

### 5.9 Material, IP, and enclosure

ABS/PC FR is a target, not a certificate. The gasket is flat with no groove and
only ~0.5 mm rim contact. IP44 is a socket rating, not an enclosure rating. The
3D print has layer lines, creep, and impact limits. Do not claim IP or
flammability without material data and tests.

### 5.10 Firmware interface

The GPIO map matches `board_config.h`, and the relay gate has a 100 kΩ pulldown.
That is good. Still missing:

- HIL test of the boot-safe waveform,
- active-LOW verification with the exact module,
- PZEM UART timing/CRC test on hardware,
- behavior when PZEM is absent/faulty,
- behavior when relay feedback is absent,
- watchdog/OTA recovery on hardware.

No temperature sensor is installed. The TCO/fuse are the only thermal
protection. Firmware must not claim temperature protection.

---

## 6. What is already good

This is not a “throw it away” review. Several foundations are solid:

- The 220 x 120 x 70 mm enclosure concept and the separation into SELV/mains
  zones are sensible.
- The PSU protection order (fuse -> MOV -> TCO -> HLK/TB2) is documented and
  logically ordered.
- The carrier is SELV-only and has a clean 74HCT125/divider interface.
- The relay gate has a mandatory 100 kΩ pulldown and a 1 kΩ series resistor.
- The GPIO map, firmware defines, and carrier netlist are consistent.
- The PSU board has a routed isolation notch and a 2 oz/4 mm target.
- DRC is 0/0 on both boards (with the caveats above).
- Gerber/drill/POS files exist, with fiducials and mounting holes.
- The safety documentation is unusually honest about `BLOCKED` and
  `UNVERIFIED` items.
- The BOM has traceable seller links and approval statuses.
- The mechanical fit check is reproducible, even though it is only AABB.

The project needs integration and evidence, not a complete restart.

---

## 7. Buildability assessment by subsystem

| Subsystem | Can it be built now? | Why |
|---|---|---|
| SELV carrier PCB | **Bench prototype only** | Routed, but no real schematic/parity; low voltage, so lower risk |
| PSU board | **No** | No real schematic, clearance/thermal/hipot open; mains |
| Relay module | **Bench only** | Exact module/active-LOW/rating unverified; no mains |
| PZEM interface | **No** | Voltage sense L/N missing; isolation unverified |
| Wiring harness | **No** | PZEM L/N and PE stud missing; CT location undefined |
| Enclosure | **Fit coupon only** | Local collisions, gasket, socket, PE, button/RGB/USB |
| Firmware | **Host/bench only** | HIL, relay polarity, UART, watchdog/OTA on hardware open |
| Complete device | **No** | P0 safety and buildability gaps |

### Suggested build stages

**Stage A — SELV bench prototype (no mains):**

- Fabricate the carrier (after schematic/parity review is started).
- Power from a current-limited 5 V bench supply.
- Use the DevKit, relay module, button, and a PZEM simulator/UART fixture.
- Test boot-safe relay OFF, GPIO map, UART levels, button, watchdog.
- Do not connect PZEM L/N or any mains.

**Stage B — mechanical fit prototype:**

- Print the enclosure coupon and the fixed brackets.
- Use dummy modules or unpowered real modules.
- Check gasket, socket, PE stud, button, RGB, USB cable, relay shelf.
- No mains.

**Stage C — mains prototype (lab only):**

- Only after P0 fixes and engineer review.
- Use a properly rated isolation transformer/bench supply, fused test fixture,
  and lab procedure.
- PE continuity, hipot/leakage, thermal, load/inrush, relay lifecycle.
- Not a household installation.

**Stage D — product/regulatory:**

- EMC/surge, IP/impact, material certificate, production test, label/manual,
  regulatory classification, sign-off.

---

## 8. Prioritized action plan

### P0 — before any mains PCB fabrication or energization

1. **Draw real schematics** for carrier and PSU; run ERC; import netlist; prove
   PCB parity.
2. **Add PZEM L/N** from TB2 L/N to PZEM; add the connection to the harness and
   validation.
3. **Resolve PE**: stud or direct; if stud, wire it and add a test point.
4. **Resolve reversible-plug protection**: 2-pole breaker/fuse/TCO or
   non-reversible plug; engineer decision.
5. **Verify the relay module**: active-LOW, JD-VCC, contact arrangement, 8 A
   rating, inrush, weld behavior; add feedback or DPST.
6. **Isolation evidence**: PZEM batch/hipot, HLK batch/hipot, leakage; fallback
   external barrier.
7. **Creepage/clearance calculation**: OVC/PD/material/altitude; upgrade 300 V
   terminals; review HLK bridge/slot.
8. **Thermal test plan**: 8 A/40 C, TCO clamp, fuse clips, terminals, HLK,
   relay; define pass limits with engineer.
9. **Fix mechanical interfaces**: relay shelf, USB cover, gasket, socket, PE,
   key; re-run local checks.

### P1 — before a prototype build

10. Clean the BOM: one D1, remove unused enclosure/standoffs/HLK plate, fix
    M3x8 quantity, PE hardware, plug 2P+E, 300 V terminals, ferrules, test
    points.
11. Update wiring harness: PZEM L/N, PE stud, CT location, wire schedule,
    colors, lengths, ferrules, torque, strain relief.
12. Add test points: +5 V, GND, PZEM TX/RX, relay gate, PE.
13. Add button bracket, RGB light pipe, USB internal cable/strain relief.
14. Rerun DRC with all checks; review footprints/courtyards; fix docs counts.
15. Add assembly drawing, connector pin 1, polarity, labels, and a low-voltage
    bring-up procedure.

### P2 — before use

16. PE continuity/earth bond, insulation resistance, hipot/dielectric, leakage
    current.
17. Thermal/load/inrush/relay lifecycle.
18. EMC/surge, IP/leak, impact, material flammability.
19. Firmware HIL, watchdog, OTA rollback, fault injection.
20. Regulatory classification, label/manual, lab report, engineer sign-off.

---

## 9. Open decisions for the user/engineer

These cannot be guessed by the AI:

1. **Reversible plug protection:** 2-pole breaker/fuse/TCO, or change to a
   non-reversible plug/socket architecture?
2. **Relay feedback:** add an aux contact/current sensor, or use a mechanically
   linked DPST relay/contactor, or accept “commanded OFF only” with a label?
3. **PZEM isolation:** keep the internal optocoupler-only design, or add the
   external ADuM1201/B0505S barrier?
4. **PE architecture:** keep the dedicated stud or use a direct plug-to-socket
   PE with a test point?
5. **Enclosure:** 3D-printed ABS/PC FR prototype, or a certified enclosure?
6. **Load profile:** what exact SMPS/electronic loads and inrush current?
7. **Regulatory target:** Indonesia/SNI, CE, or prototype-only? This changes
   the test plan.

---

## 10. Files reviewed

- `PRD.md`, `AGENTS.md`
- `hardware/kicad/README.md`, `hardware/kicad/*.kicad_sch`,
  `smartplug.kicad_pcb`, `psu_rev_d.kicad_pcb`
- `reports/kicad/erc.json`, `drc.json`, `carrier_drc.json`, `psu_drc.json`
- `hardware/carrier/README.md`, `netlist.csv`, `placement.json`
- `hardware/psu/README.md`, `netlist.csv`, `placement.json`
- `hardware/wiring/main_harness.yaml`, `metering_harness.yaml`, `README.md`,
  `renders/*`
- `hardware/interfaces/gpio_map.yaml`, `.csv`, `.md`
- `firmware/main/board_config.h`
- `bom/BOM_MASTER.csv`, `BOM_ELECTRICAL.csv`, `BOM_PROCUREMENT.csv`,
  `BOM_SUMMARY.json`
- `hardware/manufacturing/provisional/BOM_PCBA.csv`,
  `BOM_PCBA_PSU.csv`, `fabrication_notes.md`
- `safety/ISOLATION_PLAN.md`, `ELECTRICAL_RATING_CHAIN.md`,
  `PROTECTION_COORDINATION.md`, `CLEARANCE_CREEPAGE_WORKSHEET.md`,
  `POLARITY_AND_EARTH_ASSESSMENT.md`, `FAILURE_MODE_AND_EFFECTS_ANALYSIS.md`,
  `THERMAL_CALCULATION.md`, `RESIDUAL_RISK_REGISTER.csv`
- `research/PSU_BOARD_EVIDENCE.md`, `PZEM_INTERNAL_ISOLATION.md`,
  `OFFBOARD_MODULES.md`
- `validation/CONNECTIVITY_DIFF.json`, `WIRING_CONNECTIONS.csv`,
  `PSU_CROSSCHECK.json`
- `hardware/mechanical/BOM_FIT_CHECK.json`, `BOM_FIT_VERIFICATION.md`,
  `parameters.yaml`, `source/enclosure.py`, `source/components.py`
- `docs/ARCHITECTURE.md`, `docs/hardware/SYSTEM_ARCHITECTURE.md`

---

## 11. Limitations of this review

- No physical sample was measured.
- No mains test, hipot, thermal, load, EMC, surge, IP, or impact test was run.
- No component-level schematic existed to review; the review is based on block
  diagrams, netlists, placement files, and generated PCB data.
- The mechanical collision numbers come from local CadQuery boolean checks
  during this review; they are not a substitute for a tolerance-stack analysis.
- The PZEM/HLK/relay/socket/plug datasheet and batch evidence is incomplete.
- The review does not certify compliance with any standard.

**Final status:** `NOT_BUILDABLE_AS_IS` / `ENGINEERING_REVIEW_REQUIRED` /
`HARDWARE_VALIDATION_REQUIRED` / `NOT_FOR_MAINS_USE`.
