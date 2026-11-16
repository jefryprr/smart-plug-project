# Research Log — REV_C PSU Board

**Date:** 2026-11-16  
**Agent:** OpenCode digital engineering  
**Scope:** mains-entry PSU board (HLK-5M05, TB1/TB2, fuse, MOV, TCO, JST outputs), 8 A path, creepage, PZEM isolation.  
**Rule:** research first, no-stop. No physical procurement, fabrication, or mains energisation was performed.

## 1. Search and retrieval log

| # | Query / target | Source tried | Result | Fallback / decision |
|---|---|---|---|---|
| 1 | Phoenix MKDS 1,5/2-5,08 rating and order code | `phoenixcontact.com` product page | HTTP 403 to the agent | Used the indexed product summary (5.08 mm, 17.5 A, 250 V) and order code **1715721**. Marked page access limited; torque `UNVERIFIED`. |
| 2 | Phoenix MKDS 3/2-5.08 (≥300 V upgrade) | Phoenix / Mouser | Series summary only; no KiCad footprint in the portable library | Kept the routed **MKDS 1,5** footprint and documented the 250 V vs ≥300 V gap. No silent footprint guess. |
| 3 | TDK SIOV S10K275 values | `product.tdk.com` product page | HTTP 403 | Downloaded the official SIOV leaded StandarD PDF (47 pages) with a browser user-agent; read pp. 9–10 directly. |
| 4 | JST XH ratings | `jst-mfg.com/product/pdf/eng/eXH.pdf` | Returned a 239-byte HTML block, not a PDF | Downloaded the Farnell mirror of the same JST datasheet (229,169 bytes, 9 pages); values cross-checked with the JST catalogue. |
| 5 | Littelfuse 215 10 A ratings | `littelfuse.com` product page + datasheet | Product page OK; the `assetguid=...` datasheet URL in the old BOM was a placeholder and returned 419 bytes | Used the product page and the indexed 215 datasheet table: 1500 A @ 250 VAC, 0.0066 Ω, 333.565 A²s. Replaced the fake URL in the BOM. |
| 6 | Littelfuse 111 clip | `littelfuse.com` 111 series page | Product page OK (250 V, 10 A, 5×20 mm) | Changed the BOM from a closed Schurter holder to the **111 clips** that match the routed footprint. |
| 7 | SEFUSE 99 °C TCO | SEFUSE vendor site / RS mirror PDF | Vendor site had no searchable table; RS mirror PDF downloaded (223,045 bytes, 2 pages) | **Key finding:** SF96E = 99 °C rated functioning temperature (marked 96 °C), holding 84 °C, 10 A/250 VAC. **SF169E = 172 °C.** Corrected the BOM. |
| 8 | One-shot vs resettable alternative | Bourns LC datasheet | Downloaded (685,321 bytes, 6 pages) | LC is a **resettable mini-breaker**; rejected for a one-shot TCO. Documented the rejection. |
| 9 | Creepage/clearance public guidance | TI SLUP421 / SLUP419 | Downloaded both (1,228,561 and 392,176 bytes) | Used the public 250 V-class, OVC II, PD2, MG III examples (basic 4.0 mm, reinforced 8.0 mm). The paid IEC tables were **not** reproduced. |
| 10 | IPC-2221 trace width | AdvancedPCB calculator + Altium article | Public formula and constants | Calculated 2.64 mm at 2 oz for 8 A/10 °C; design uses 4 mm at 2 oz target. Marked `CALCULATED`, not tested. |
| 11 | PZEM internal isolation | Tasmota docs, Components101, reverse-engineered schematic | Existing `research/PZEM_INTERNAL_ISOLATION.md` | Confirmed internal optocouplers as the only barrier; OUT3 conditional; ADR-016. |
| 12 | HLK-5M05 footprint/pinout | Distributor datasheet already in repo | 3-page PDF with dimension drawing; pins 1/2 AC, 3 −Vo, 4 +Vo | Used the drawing. Physical sample and batch certificate still `UNVERIFIED`. |
| 13 | Fuse continuous derating | Littelfuse product data | No explicit continuous-derating rule found in the retrieved page | Flagged 8 A / 10 A = 80 % as marginal and `PROVISIONAL`; thermal test decides 10 A vs 12 A. No invented “75 % rule” citation. |

## 2. Failed or limited sources

- **Phoenix product page:** HTTP 403. The order code and series ratings came from the indexed summary; the 2-position certificate/torque is still open.
- **TDK product page:** HTTP 403. Worked around with the official PDF.
- **JST official PDF:** returned HTML. Worked around with the Farnell mirror; the official URL is retained in the BOM for traceability.
- **Littelfuse assetguid URLs:** several were placeholders (419 bytes / 404). Replaced with stable product-page URLs.
- **IEC 60664-1 / IEC 62368-1:** paywalled and not reproduced. Only public TI application-note examples were used; the worksheet remains `BLOCKED_INPUTS_INCOMPLETE` for a real calculation.
- **No physical samples:** HLK, terminal, fuse, MOV, TCO, JST, relay, PZEM, enclosure. All sample-dependent claims are `UNVERIFIED`.

## 3. Decisions taken from the research

1. **TCO = SEFUSE SF96E** (99 °C RFT, 84 °C holding, 10 A/250 VAC). SF169E removed.
2. **Fuse = Littelfuse 0215010.MXP** (10 A, 250 VAC, time-lag, 1500 A interrupting) with **111 clips**. The 10 A rating is retained per the user, but 8 A continuous is flagged.
3. **MOV = TDK S10K275** (275 VRMS, 430 V VV, 710 V clamp at 25 A, 43 J).
4. **Terminal = Phoenix MKDS 1,5/2-5,08** (17.5 A / 250 V), because it matches the routed footprint. The ≥300 V target is **not met**; MKDS 3 is the documented upgrade.
5. **JST XH** for the three 5 V outputs (3 A / 250 V per contact).
6. **2 oz copper target** and 4 mm L/N traces; 1 oz would need ~5.3 mm by the IPC-2221 calculation.
7. **PZEM internal optocouplers only**; no ADuM/B0505S; OUT3 `PROVISIONAL`.
8. **PE stays off-board** on a dedicated chassis stud; no PE net on the PSU board.

## 4. What this log does not prove

- It does not prove creepage/clearance compliance, hipot, leakage, thermal rise, fuse breaking, MOV endurance, TCO trip, relay life, or PE continuity.
- It does not prove the HLK batch is genuine or certified.
- It does not authorise fabrication or mains energisation.

## 5. Artefacts written from this research

- `research/PSU_BOARD_EVIDENCE.md`
- `research/datasheets/MANIFEST.md` (new PDFs + SHA-256)
- `docs/decisions/ADR-016-PZEM-ISOLATION-REV-C.md`
- `hardware/psu/README.md`
- `safety/CLEARANCE_CREEPAGE_WORKSHEET.md`, `safety/THERMAL_CALCULATION.md`, `safety/PROTECTION_COORDINATION.md`
