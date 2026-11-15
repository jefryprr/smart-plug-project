# ADR-010 — Time, Energy, and Cost Semantics

**Status:** Accepted
**Date:** 2026-11-15
**Related:** FR-004, FR-006..009, NFR-04

## Context
Energy counters are cumulative and can reset/rollover. Tariffs change over time. Timezones/DST affect daily buckets. Presenting raw totals as daily kWh is wrong.

## Decision
- Store meter energy as cumulative `energy_kwh_total`; compute deltas only with monotonic sequence/valid quality.
- Reset/rollover/gap => delta 0 + explicit gap event, not negative or fake consumption.
- Cost = Σ(delta × tariff effective at interval start); historical tariffs are not rewritten silently.
- Store UTC; present in `Asia/Jakarta` by default; bucket labels include timezone.
- Missing data is `null`/`data_available=false`, never zero.
- IDR rounding only at presentation.

## Consequences
- Analytics buckets can be empty; UI shows “Tidak ada data”.
- Tariff changes require an explicit effective date.
- Counter reset creates a new segment and audit event.
- Tests cover reset, non-monotonic sequence, gap, tariff history, missing tariff.

## Alternatives
- Sum cumulative counters: rejected (wrong after reset).
- Convert to daily kWh in firmware: rejected (loss of raw data).
- Assume one fixed tariff: rejected (historical cost wrong).
