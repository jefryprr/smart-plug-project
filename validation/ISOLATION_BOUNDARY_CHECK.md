# Isolation Boundary Check — REV_D_CORE_ONLY

**Status:** static wiring check only. Manual engineering review is still required.

- Overall static status: **PASS**
- PE path: **PASS**
- Relay contacts separate: **PASS**
- Relay coil SELV: **PASS**
- PZEM internal isolation (static): **PASS**
- Mains/SELV separation: **PASS**
- GPIO crosscheck: **PASS**
- BOM crosscheck: **PASS**

## Limitations
- This is not a KiCad netlist, ERC, or DRC.
- It does not prove creepage, clearance, dielectric strength, PE continuity, or thermal safety.
- Wiring YAML is a design intent; physical harness must be continuity-tested by a qualified person.
- `PASS` here means static consistency only.
- PSU OUT3 (J7) is conditional on PZEM batch inspection + hipot/leakage (ADR-016).
- The PSU board fuse/MOV/TCO are board-level parts, not harness nodes; their order is checked by `scripts/validate_psu.py`.
