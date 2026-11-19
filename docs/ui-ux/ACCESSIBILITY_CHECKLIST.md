# Accessibility Checklist — REV_D_CORE_ONLY

## Automated

- [x] axe WCAG 2 A/AA on `/login` — no serious/critical violations.
- [x] axe WCAG 2 A/AA on `/dashboard` — no serious/critical violations.
- [ ] axe on every device tab (not run).
- [ ] axe on settings/onboarding (not run).

## Manual/keyboard

- [x] Skip link to main content.
- [x] All interactive controls are native `button`/`a`/`input`.
- [x] Visible focus ring (`:focus-visible`).
- [x] Form labels associated with inputs.
- [x] Command status uses `aria-live="polite"`.
- [x] Fault/offline banners use `role="alert"`/`status`.
- [x] Status badges include text, not color only.
- [ ] Full keyboard walkthrough of every tab (not completed).
- [ ] Screen reader walkthrough (NVDA/Orca) (not completed).

## Content

- [x] Indonesian labels.
- [x] Units on readings.
- [x] Timestamps with timezone.
- [x] Missing data labeled, not zero.
- [x] Estimated cost labeled as estimate.
- [x] `ON (commanded)` vs observed feedback distinction.

## Gaps

- Chart SVG has `role="img"` and an aria-label, but individual bars are not keyboard-focusable. Provide a data table alternative (analytics page already has a bucket table).
- Color contrast on disabled buttons may fall below AA; axe did not flag login/dashboard, but disabled states need manual review.
- No high-contrast/forced-colors testing.
- No screen reader testing.
