# Design System — REV_C_PSU_BOARD

## Principles

1. Safety status is never conveyed by color alone.
2. `commanded` and `observed` are distinct labels.
3. Pending is not success; stale is not live.
4. Missing data is not zero.
5. Destructive/risky actions require confirmation and explain consequences.

## Tokens

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#f3f6fb` | `#0a1120` | Page background |
| `--surface` | `#ffffff` | `#121b2c` | Cards/panels |
| `--text` | `#14213d` | `#e8eef8` | Primary text |
| `--muted` | `#5b677a` | `#9daabd` | Secondary text |
| `--accent` | `#0f6b5c` | `#49d7b8` | Primary action |
| `--danger` | `#b42318` | `#ff8a80` | Fault/destructive |
| `--warn` | `#9a5b00` | `#ffc46b` | Caution/stale |
| `--ok` | `#067647` | `#6ee7a8` | Online/applied |
| `--info` | `#175cd3` | `#9cc2ff` | Informational |

## Typography

- System UI stack: Segoe UI, system-ui, sans-serif.
- Headings: 1.05–2.2 rem, tight letter spacing.
- Body: 0.95–1rem, line-height 1.55.
- Monospace: Cascadia Code/Consolas for IDs and JSON.

## Components

| Component | Purpose | Safety rule |
|---|---|---|
| `StatusBadge` | Availability/output/severity | Text + dot, not color-only |
| `DeviceSummaryCard` | Device overview | Shows commanded, last seen, data source |
| `PowerControl` | ON/OFF/emergency OFF | Polls ACK; no optimistic success |
| `ElectricalReadings` | V/A/W/PF/Hz/kWh | Invalid -> dashes + warning |
| `UsageAndCost` | kWh/IDR estimate | Labels estimate; missing tariff partial |
| `EnergyGraph` | Energy bars | Missing bucket hatched/empty |
| `EventList` | Fault/command audit | Severity text, timestamp, payload |
| `DeviceHealth` | Diagnostics | No secrets; unknown shown as unknown |
| `ScheduleEditor` | Weekly schedule | Version conflict; ON blocked if clock invalid |
| `DeviceSettings` | Rename/tariff/budget/OTA/revoke | Confirm risky actions |

## Layout

- Max width 1280 px; mobile-first.
- Panels: 14 px radius, 1 px border, subtle shadow.
- Grids collapse at 980 px and 720 px.
- Touch targets ≥44 px.
- Focus ring: 3 px accent with offset.

## Content rules

- Use Indonesian for user-facing text.
- `ON (commanded)` not `ON` alone unless observed feedback exists.
- `Tidak tersedia` for missing feedback; `Tidak ada data` for empty history.
- Avoid "real-time" unless measured; use "sampel terakhir" and timestamp.
- Never show a success toast before ACK.
