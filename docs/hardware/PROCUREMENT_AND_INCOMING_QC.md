# Procurement and Incoming Inspection (QC)

**Status:** `BLOCKED` — no purchase has been made; prices/MPNs unapproved.
**Rule:** Do not connect any incoming part to mains. Incoming QC is visual/mechanical/electrical at **low voltage** only, unless a qualified lab procedure says otherwise.

## 1. Before ordering

- [ ] MPN, revision, datasheet, and seller verified.
- [ ] Safety-critical part approved by engineer (socket, plug, relay, fuse, PSU, terminal, PE, enclosure).
- [ ] Price/stock/date recorded; no Rp0 placeholders.
- [ ] Sample/quantity and customs/lead time considered.
- [ ] Counterfeit risk assessed (authorized distributor preferred).

## 2. On arrival (no mains)

1. Photograph packaging, label, front/back, connector, batch/date code.
2. Compare marking to MPN/revision; quarantine if different.
3. Measure dimensions with calipers; update `hardware/mechanical/source/components.py`.
4. Inspect for damage, contamination, bent pins, cracked case, loose terminal.
5. Verify connector pitch/pinout against the actual datasheet.
6. For PZEM/CT: record CT ratio/marking, cable length, terminal labels; do not assume V3 docs.
7. For the off-board relay module: verify two independent SPDT channels (not DPST), active-LOW inputs, JD-VCC jumper/pinout, 5 V coil, contact marking, and per-channel continuity.
8. For the HLK-5M05 PSU: verify 4-pin marking (AC/AC/−Vo/+Vo), 38×23×18 mm body, 5 V/1 A/5 W label, input range, batch/certificate, ripple/startup, no-load, isolation/leakage, and thermal rise. Treat unmarked/counterfeit modules as rejected.
9. For socket/plug: verify PE contacts, shutter, retention, material marking.
10. For enclosure: verify material/UL94 marking, wall thickness, dimensions.

## 3. Quarantine

Quarantine and revise design freeze if:
- marking/revision differs from the approved MPN;
- dimensions differ enough to affect fit/clearance;
- datasheet is missing or inconsistent;
- counterfeit/refurbished suspicion;
- terminal/contact rating cannot be verified.

## 4. Record

`research/datasheets/MANIFEST.md` update + a new row in `bom/BOM_MASTER.csv` if the part changes. Add photos to `research/incoming/` (not committed if sensitive) and note the measurement date.

## 5. Do not

- Do not power a suspect PSU/relay/socket.
- Do not perform hipot/insulation tests without a qualified lab.
- Do not “try it on mains” to see if it works.
- Do not substitute a visually similar part without re-approval.
