# Responsive Matrix — REV_D_CORE_ONLY

| Breakpoint | Layout | Verified |
|---|---|---|
| ≥1280 px | Full nav, 2-column overview, 4 summary cards | Playwright 1440×960 |
| 980–1279 px | Overview collapses to 1 column; summary 2 columns | CSS media query; not screenshot-tested |
| 720–979 px | Nav wraps; device cards 2 columns; readings 2 columns | CSS media query; not screenshot-tested |
| ≤719 px | Nav scrolls; 1-column cards; 2-column readings; stacked settings | Playwright 390×844 |

## Rules

- No horizontal page scroll at 320 px width.
- Charts scroll inside their container, not the page.
- Tables scroll horizontally.
- Touch targets ≥44 px.
- Device tabs scroll horizontally on mobile.
- Login page stacks aside above form below 980 px.

## Evidence

- `docs/ui-ux/screenshots/11-mobile-dashboard.png`
- `docs/ui-ux/screenshots/12-mobile-device.png`
- Playwright test `tests/e2e/ui.spec.ts` mobile project.

## Gaps

- Tablet viewport not screenshot-tested.
- Very long device names/rooms not fuzzed.
- 320 px edge case not tested.
