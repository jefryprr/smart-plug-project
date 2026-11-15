# ADR-008 — Hardware Toolchain and Source of Truth (REV_B)

**Status:** Accepted with deviations  
**Date:** 2026-11-16

## Context

The PRD prefers KiCad, Circuit-Synth, WireViz, CadQuery, and FreeRouting. In this
environment:

- KiCad/KiCad CLI: **10.0.8 portable** in `tools/kicad`
- Circuit-Synth: **not used**
- WireViz: installed in `.venv`, Graphviz portable available
- CadQuery: installed in `.venv`
- FreeRouting: 1.9.0 jar downloaded for evaluation, but the final carrier was
  routed with a deterministic `pcbnew` grid router because DSN export was not
  reliable headlessly.

## Decision

- Use **KiCad native files** for the system block schematic and the routed SELV
  carrier.
- `hardware/generators/generate_kicad.py` emits the block schematic/project.
  `scripts/generate_carrier_pcb.py` places footprints and nets;
  `scripts/route_carrier.py` routes the 100 × 70 mm carrier with `pcbnew`.
- Use **WireViz** for harnesses (5 rendered YAMLs; duplicate relay harness
  removed).
- Use **CadQuery** for parametric enclosure/assembly (STEP/STL/render).
- Do not fake Gerber, DRC, ERC, or 3D KiCad renders.
- The functional schematic/netlist is `hardware/schematic/` and
  `hardware/carrier/netlist.csv`; the KiCad schematic remains block-level.

## Consequences

- Routed carrier DRC **0/0** at 0.15 mm, ERC 0 on the block schematic.
- Routed Gerber/drill/POS exist, but no fabrication release.
- No physical fit/hipot/thermal/load validation.
- A future KiCad install/version change must re-run DRC and regenerate
  manufacturing artifacts.
- FreeRouting can be retried if a reliable DSN export is available.

## Alternatives

- Hand-write Gerber: rejected as fake.
- Skip KiCad: rejected because native files are required.
- Use FreeRouting: deferred; DSN export was not reliable in this environment.
