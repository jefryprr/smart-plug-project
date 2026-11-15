# ADR-011 — Synthetic Demo Data Labeling

**Status:** Accepted
**Date:** 2026-11-15
**Related:** UI safety, PRD 21.1

## Context
The environment has no hardware/lab. The web demo needs data, but synthetic readings must not be mistaken for real measurements or safety evidence.

## Decision
- Seed data is marked `data_source=SYNTHETIC_DEMO`.
- UI shows a persistent demo banner and per-card chip.
- Diagnostics/README state that data is synthetic.
- Simulator data is `SIMULATOR`; real device data would be `DEVICE`.
- Analytics/cost from synthetic data is labeled as a demo estimate.

## Consequences
- Screenshots are clearly demo.
- No test result from seed data is used as HIL/physical evidence.
- A real device must not inherit the demo flag.

## Alternatives
- Hide the demo flag: rejected as misleading.
- Use random data without labels: rejected.
