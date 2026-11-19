# Screen Specifications — REV_D_CORE_ONLY

Screenshots are real Playwright outputs in `docs/ui-ux/screenshots/`.

## `/login`

- Email/password, demo hint, safety aside.
- Error on invalid credentials; no user enumeration.
- Screenshot: `01-login.png`.

## `/dashboard`

- Summary cards: total, online, fault/lockout, demo.
- Device cards with availability, commanded output, last seen, firmware, demo chip.
- Empty state links to pairing.
- Screenshot: `02-dashboard.png`.

## `/devices/[id]/overview`

- Header: name, room, ID, role, availability, commanded, lockout.
- `PowerControl`: ON/OFF/emergency OFF, pending/ACK, lockout/offline banners.
- `ElectricalReadings`: V/A/W/PF/Hz/kWh; invalid handling.
- `UsageAndCost`: 24h estimate, missing tariff warning.
- `EnergyGraph`: 24h bars; missing data.
- `EventList`, `DeviceHealth`.
- Screenshot: `03-device-overview.png`.

## `/devices/[id]/analytics`

- Range 24h/7d/30d; totals; graph; bucket table with samples/gaps/missing.
- Screenshot: `04-analytics.png`.

## `/devices/[id]/schedules`

- Weekly schedules, day chips, time/duration/action, enable, save with version.
- Warning: local execution, clock validity.
- Screenshot: `05-schedules.png`.

## `/devices/[id]/automation`

- Rule catalog with statuses (backend rule, not active, firmware/BLOCKED).
- Current schedules and events.
- Screenshot: `06-automation.png`.

## `/devices/[id]/events`

- Severity filter; event list; payload details.
- Screenshot: `07-events.png`.

## `/devices/[id]/diagnostics`

- Health grid, command counts, last error, raw JSON details.
- Screenshot: `08-diagnostics.png`.

## `/devices/[id]/settings`

- Rename/room, notification test, tariff history/add, budget, OTA request, revoke.
- Risk confirmations; OTA is request-only.
- Screenshot: `09-device-settings.png`.

## `/onboarding/pair-device`

- Pairing code, optional name, success redirect.
- Demo code hint (dev only).

## `/settings/tariffs`, `/settings/notifications`, `/settings/account`, `/settings/security`

- Per-device links, test provider, profile/roles, security posture.
- No revoke-all-sessions claim.

## `/admin/firmware-releases`

- Honest status: release management not implemented; OTA request only.
- Role-gated notice.

## Mobile

- 390×844 screenshots: `11-mobile-dashboard.png`, `12-mobile-device.png`.
