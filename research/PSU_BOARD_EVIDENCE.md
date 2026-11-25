# REV_D_CORE_ONLY PSU Board — Research Evidence

**Design revision:** `REV_D_CORE_ONLY`  
**Compiled:** 2026-11-16  
**Scope:** separate 50 × 65 mm mains-entry PSU board (HLK-5M05, TB1/TB2, F1, MOV, TCO, 3× JST 5 V).  
**Status of this document:** design input, not a safety approval. Every `UNVERIFIED` item still needs a competent engineer and physical test.

Source hierarchy used: manufacturer datasheet → official test/certificate → official product page → public standard guidance → manufacturer application note → authorised distributor → forum only as a lead. No value below is copied from an AI-generated page or from a paywalled standard.

> **2026-11-24 superseding note — actual Shopee parts.** The evidence rows E-04 (Phoenix MKDS), E-05 (10 A Littelfuse), E-06 (Littelfuse 111 clips), and E-08 (SEFUSE SF96E) describe the earlier preferred parts, **not** the parts actually bought. The cart now uses:
> - TB1/TB2: **KF129-2P**, 5.08 mm, 300 V/25 A claim, new listing with 0 reviews/0 sold → `UNVERIFIED`; PCB uses a Phoenix pad layout only.
> - F1: **Littelfuse 215-series 6.3 A / 250 V** slow-blow → `PROVISIONAL`; breaking capacity/MPN still unverified.
> - Fuse holder: **BLX-A 6.3 A / 250 V**, 5×20 mm → `PROVISIONAL`; this is the limiting part for continuous current (6 A maximum), not 10 A.
> - TCO: **generic 96 °C / 10 A**, not SEFUSE SF96E → `UNVERIFIED`; do not claim SF96E.
> - MOV: **generic 10D271K**, 10 mm, 10 pcs pack → `UNVERIFIED`; the D12/7.5 mm PCB footprint is provisional.
> - PTC: **1.0 A** 1206, not 1.1 A.
> The 8 A rating in this document is therefore **superseded** by a provisional 6 A limit. See `safety/ELECTRICAL_RATING_CHAIN.md` and `reports/PCB_DESIGN_RESEARCH_AND_REVIEW_2026-11-24.md`.

## 1. Evidence table

| # | Topic | Value used in the design | Source (primary) | URL | Accessed | Revision | Confidence | Conflict / note |
|---|---|---|---|---|---|---|---|---|
| E-01 | HLK-5M05 package | 38 × 23 × 18 mm; 4 pins; pin 1/2 = AC, pin 3 = −Vo, pin 4 = +Vo | Hi-Link HLK-5M05 datasheet, distributor copy (3 pages, dimension drawing) | https://5.imimg.com/data5/JI/JR/RP/SELLER-1833510/hlk-5m05-power-module.pdf | 2026-11-16 | UNKNOWN | MEDIUM | Drawing read visually; **physical sample pinout still unverified**. Official page: https://www.hlktech.net/index.php?id=1243 |
| E-02 | HLK-5M05 ratings | 5 V / 1 A / 5 W; 90–264 VAC; max input current ≤0.2 A; inrush ≤10 A; ~70 % efficiency at 220 V full load → ~2.1 W heat | Same datasheet | as E-01 | 2026-11-16 | UNKNOWN | MEDIUM | Efficiency is read from the datasheet curve; exact batch efficiency/thermal `UNVERIFIED`. |
| E-03 | HLK-5M05 isolation | Claimed 2500 VAC input–output; "meets UL, CE requirements" | Same datasheet + official product page | as E-01 | 2026-11-16 | UNKNOWN | LOW | **Claim only.** No UL file number, CB certificate, batch label, or hipot report in hand. `PENDING_APPROVAL`. |
| E-04 | Terminal block | Phoenix MKDS 1,5/2-5,08; 5.08 mm; 17.5 A; 250 V; 1.5 mm²; screw clamp; order code 1715721 | Phoenix product page / series data | https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mkds-15-2-508-1715721 | 2026-11-16 | UNKNOWN | MEDIUM | Page returned HTTP 403 to the agent; values taken from the indexed product summary. **250 V is below the user's ≥300 V target**; torque and 2-pos certificate `UNVERIFIED`. Upgrade path: MKDS 3/2-5,08 (320 V), requires a new footprint. |
| E-05 | Mains fuse | Littelfuse 0215010.MXP; 5 × 20 mm; 10 A; 250 VAC; time-lag (T); ceramic; 1500 A interrupting at 250 VAC; 0.0066 Ω cold; 333.565 A²s; 100 mV at 10 A; 4 W at 1.5 In | Littelfuse 215 series product page and datasheet | https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/cartridge-fuses/5x20mm-fuses-cartridge-fuses/215/0215010 | 2026-11-16 | UNKNOWN | HIGH | 8 A continuous = 80 % of rating. Time-lag fuses are commonly derated for continuous duty; a 12 A may be needed after thermal test. Do not change without analysis. |
| E-06 | Fuse clips | Littelfuse 111 series, 01110506Z; 5 × 20 mm; 250 V; 10 A; PCB mount | Littelfuse 111 product page | https://www.littelfuse.com/products/fuses-overcurrent-protection/fuse-holders-fuse-blocks-accessories/fuse-accessories/fuse-clips/111/111505 | 2026-11-16 | UNKNOWN | HIGH | 10 A clip at 8 A is marginal. The 215 datasheet lists a 445 clip as the recommended accessory; the routed footprint is 111. Closed holder (Schurter 0031.8201) would need a new footprint. |
| E-07 | MOV | TDK/EPCOS B72210S0271K101 (S10K275): VRMS 275 V; VDC 350 V; VV 430 V ±10 %; vc,max 710 V at 25 A; imax 2500 A (8/20 µs); In 1500 A; Wmax 43 J; Pmax 0.40 W | TDK SIOV leaded StandarD datasheet, pp. 9–10 | https://www.tdk-electronics.tdk.com/inf/70/db/var/SIOV_Leaded_StandarD.pdf | 2026-11-16 | UNKNOWN | HIGH | Datasheet table read directly. MOV end-of-life/short mode and fuse coordination still need a surge study. |
| E-08 | Thermal cutoff | SEFUSE SF96E: rated functioning temperature **99 °C**; marking 96 °C; holding temperature **84 °C**; 10 A / 250 VAC; one-shot organic pellet | SEFUSE SF/E series datasheet (RS mirror), ratings table | https://docs.rs-online.com/68de/0900766b81546f0c.pdf | 2026-11-16 | UNKNOWN | HIGH | **Correction:** SF169E is 172 °C, not 99 °C. The earlier BOM was wrong. SF96E is the 99 °C part. Batch certificate/trip test `UNVERIFIED`. Normal hotspot must stay <84 °C with margin. |
| E-09 | TCO alternatives | Bourns LC series is a **resettable mini-breaker** (resets when ambient drops 10 °C below trip and power is cycled) | Bourns LC datasheet | https://www.bourns.com/docs/product-datasheets/lc.pdf | 2026-11-16 | UNKNOWN | HIGH | Rejected as a one-shot TCO. KSD301 auto-reset thermostats are also not equivalent. |
| E-10 | JST 5 V outputs | JST XH: 2.5 mm pitch; 3 A AC/DC (AWG #22); 250 V AC/DC; −25 to +85 °C | JST XH datasheet (Farnell mirror of official eXH.pdf) | https://www.farnell.com/datasheets/5448.pdf | 2026-11-16 | UNKNOWN | HIGH | Official JST URL is https://www.jst-mfg.com/product/pdf/eng/eXH.pdf (blocked to the agent). 3 A per contact > 1 A total budget. |
| E-11 | 8 A trace width | IPC-2221 external: A = (I / (k·ΔT^b))^(1/c), k=0.048, b=0.44, c=0.725. 8 A, ΔT=10 °C → 287 mil² → **2.64 mm at 2 oz**, **5.29 mm at 1 oz** | AdvancedPCB IPC-2221 calculator + Altium IPC-2221 article | https://www.advancedpcb.com/en-us/tools/trace-width-calculator/ ; https://resources.altium.com/p/ipc-2221-calculator-pcb-trace-current-and-heating | 2026-11-16 | formula | CALCULATED | Design uses 4 mm at **2 oz target** → about 1.5× the calculated minimum. This ignores connector/fuse/TCO heat and enclosure airflow. Not a thermal test. |
| E-12 | 8 A copper loss | 4 mm × 70 µm copper, 60 mm long: R ≈ 3.7 mΩ, P ≈ 0.24 W at 8 A | Calculation from copper resistivity 1.72 × 10⁻⁸ Ω·m | — | 2026-11-16 | — | CALCULATED | Short, wide traces are not the main heat source; terminals, fuse clips, TCO, and HLK dominate. |
| E-13 | Fuse loss at 8 A | 0.0066 Ω × 8² = **0.42 W** in the fuse element | E-05 | as E-05 | 2026-11-16 | — | CALCULATED | Clip contact resistance adds unknown loss. Thermal test required. |
| E-14 | Creepage / clearance guidance | Public TI example, 250 V-class, OVC II, PD2, material group III: **basic creepage 4.0 mm; reinforced 8.0 mm**; reinforced clearance 3.8 mm at ≤2000 m, 5.7 mm at 5000 m (×1.48) | TI SLUP421 "Demystifying clearance and creepage distance" | https://www.ti.com/lit/pdf/SLUP421 | 2026-11-16 | — | GUIDANCE_ONLY | The paywalled IEC 60664-1 tables were not reproduced. Board uses provisional 6–12 mm spacing and a 2 mm slot; this is **not** a compliance calculation. OVC, PD, CTI/material group, altitude, and coating are still open. |
| E-15 | PZEM UART isolation | PZEM-004T V4 uses internal optocouplers between mains/measurement and TTL; TTL side is SELV when intact | Tasmota PZEM docs; Components101 block diagram; reverse-engineered schematic | https://tasmota.github.io/docs/PZEM-0XX/ ; https://components101.com/modules/pzem-004t-energy-meter-module-pinout-datasheet ; https://github.com/TheHWcave/Peacefair-PZEM-004T- | 2026-11-16 | UNKNOWN | MEDIUM | Single barrier. Batch inspection + mains-to-TTL hipot/leakage required. OUT3 is `PROVISIONAL`; ADR-016. |
| E-16 | 5 V load budget | Carrier + relay + PZEM estimated peak ≈0.58 A; HLK 1 A; total design limit 1 A | Internal estimate | `docs/hardware/SYSTEM_ARCHITECTURE.md` | 2026-11-16 | — | UNVERIFIED | Not measured. Do not add loads without a new budget and thermal check. |
| E-17 | Enclosure fit | 220 × 120 × 70 mm confirmed by user; PSU board 50 × 65 mm placed at x=56..106, y=−55..10, z=8..38; socket y=34.9; gland y=10; PE stud (60,50); relay shelf above PSU | `hardware/mechanical/parameters.yaml`, `hardware/mechanical/FIT_ANALYSIS.md` | local | 2026-11-16 | REV_D_CORE_ONLY | DIGITAL_FIT_PASS | AABB fit only. No tolerance stack, cable bend, thermal expansion, or impact test. |
| E-18 | PE path | Dedicated chassis stud (60,50); plug PE → stud → socket PE; no PE net on the PSU board; never switched or fused | IEC Class I practice; project safety plan | `safety/ISOLATION_PLAN.md` | 2026-11-16 | REV_D_CORE_ONLY | DESIGN_RULE | Continuity, stud torque, and fault-current test `UNVERIFIED`. |
| E-19 | TCO thermal constraint | SF96E holding temperature 84 °C; 8 A terminal/fuse/TCO/HLK hotspots must stay below 84 °C with margin | E-08 + thermal calculation | `safety/THERMAL_CALCULATION.md` | 2026-11-16 | — | UNVERIFIED | If the 8 A test exceeds 84 °C at the TCO, relocate/derate before release. |
| E-20 | Fuse continuous derating | 10 A fuse at 8 A = 80 % of rating; common time-lag continuous-duty guidance is ~75 % | Engineering note, not a datasheet guarantee (E-05 gives the ratings, not a derating rule) | — | 2026-11-16 | — | PROVISIONAL | The design keeps 10 A per user instruction, but flags that a 12 A may be required by the thermal test. Do not silently upsize. |

## 2. Protection order (as built)

```
TB1 L -> F1 -> L_FUSED -> MOV1 (L-N) -> TF1 -> L_LOAD -> TB2 L
                                                    -> PS1 pin 1 (HLK AC L)
TB1 N -> N_MAINS -> TB2 N / MOV1 N / PS1 pin 2 (HLK AC N)
PS1 +Vo -> F2 PTC -> +5V -> J5 / J6 / J7 / D1 / C1 / C2
PS1 -Vo -> GND
```

- F1 is before the MOV, so a failed MOV is cleared by F1.
- TF1 is after the MOV in the L path, so it removes both the load and the HLK input.
- PE is not on the board.

## 3. Historical 8 A trace check (superseded by the 6 A holder limit)

IPC-2221 external-layer formula (E-11):

```
A = (I / (k * dT^b))^(1/c)
A = (8 / (0.048 * 10^0.44))^(1/0.725)
  = 287 mil^2  (approx. 0.185 mm^2)
W(2 oz) = 287 / (2 * 1.378) = 104 mil = 2.64 mm
W(1 oz) = 287 / (1 * 1.378) = 208 mil = 5.29 mm
```

The historical check used 4 mm L/N traces and a 2 oz target. The actual design now uses 4 mm at the terminal feeds and 2.5 mm on the fuse/TCO bus for a **6 A provisional** limit. Width is still **not** evidence that the terminals, BLX-A holder, TCO, or HLK stay below their limits; the 6 A closed-enclosure test is the only acceptable proof.

## 4. Conflicts resolved in this revision

| Conflict | Resolution | Evidence |
|---|---|---|
| TCO `SF169E` labelled 99 °C | **Wrong.** SF169E is 172 °C. Replaced with **SF96E** (99 °C RFT, 84 °C holding). | E-08 |
| BOM closed holder 0031.8201 vs routed 111 clips | BOM changed to **Littelfuse 01110506Z clips (2 pcs)** matching the PCB. Closed holder listed as an alternate requiring a footprint change. | E-06 |
| BOM MKDS 3/2-5.08 vs routed MKDS-1,5 footprint | BOM changed to **MKDS 1,5/2-5,08** (17.5 A / 250 V). The ≥300 V target is **not met**; MKDS 3 upgrade documented. | E-04 |
| PZEM REV_A external ADuM/B0505S vs REV_B internal optocouplers | REV_D_CORE_ONLY uses **internal optocouplers only**; OUT3 conditional. | `ADR-016` |
| HLK "UL/CE" claim vs no certificate | Treated as a **claim**; `PENDING_APPROVAL`; batch/hipot required. | E-03 |

## 5. Open items that are not answered by research

- HLK-5M05 batch certificate, UL file, isolation/hipot, ripple, thermal.
- Terminal block torque, 2-position certificate, 250 V vs 300 V decision.
- Fuse holder/clip thermal at 8 A in the closed enclosure; 10 A vs 12 A decision.
- TCO trip test at 99 °C, holding at 84 °C, mounting/clamping method.
- MOV surge/end-of-life coordination and fuse clearing.
- PZEM batch internal isolation, creepage, hipot/leakage; OUT3 go/no-go.
- Board creepage/clearance to IEC 60664-1: OVC, PD, material group, altitude, coating.
- PE continuity/fault-current test; enclosure flammability/impact/IP.
- 8 A load, inrush, relay lifecycle, socket/plug temperature.

## 6. Source files with hashes

See `research/datasheets/MANIFEST.md` for SHA-256 of the downloaded PDFs (SEFUSE, TDK SIOV, JST XH, TI SLUP421/SLUP419, Bourns LC, HLK distributor copy).
