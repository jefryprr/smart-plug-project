# Standard Applicability Matrix — REV_A_PROVISIONAL

**Status:** `RESEARCH_REQUIRED`
**Rule:** This matrix records applicability, not certification. Full standard texts may be licensed/paid; do not reproduce them without a license.

| Standard | Edition/year | Applies? | Why/why not | Evidence needed | Status |
|---|---|---|---|---|---|
| IEC 60884-1 | 2022 (+ corrections) | Likely for plug/socket | Plugs and socket-outlets for household/similar | Product classification, full clause review | `OPEN` |
| IEC 60664-1 | 2020 + Amd 1:2025 | Yes for insulation coordination | Clearance/creepage/solid insulation | Inputs + licensed tables + engineer | `REQUIRED` |
| IEC 61058-1 | 2026 | Possibly for switching | Switches for appliances; depends on architecture | Applicability review | `OPEN` |
| IEC 60335-1 | Current | Possibly | Household appliance safety; product classification unclear | Regulatory review | `OPEN` |
| IEC 61010-1 | Current | Possibly | Measurement/control/lab equipment | Classification review | `OPEN` |
| IEC 61000-6-x / CISPR | Current | Likely for EMC | PSU/relay/ESP32 emissions/immunity | EMC test plan | `OPEN` |
| Relay standard (IEC 61810 / UL 508) | Current | Yes for relay | Contact rating/lifecycle | Exact MPN datasheet | `OPEN` |
| Fuse standard (IEC 60127) | Current | Yes for fuse | Breaking capacity/time-current | Exact fuse datasheet | `OPEN` |
| PSU safety (IEC 62368-1 / 61558) | Current | Yes for PSU | Isolation/thermal | Exact PSU certificate | `OPEN` |
| Enclosure flammability (UL94 / IEC 60695) | Current | Yes | Material fire behavior | Material datasheet | `OPEN` |
| PE/earthing requirements | Local/standard | Yes | Protective earth continuity | Standard + test | `OPEN` |
| SNI / Indonesian regulations | Current | Unknown | Market access/certification | Regulator/lab consultation | `RESEARCH_REQUIRED` |
| Radio (Wi-Fi/BLE) | Local | Likely | ESP32 module/product | Module certificate + product notification | `OPEN` |

## Gaps

- No licensed full text was reviewed for clearance/creepage values.
- No regulatory classification decision.
- No lab/accreditation selected.
- No certificate or declaration is claimed.

## Next actions

1. Classify the product and intended use (lab prototype vs consumer).
2. Obtain the applicable standards/editions through a licensed channel.
3. Fill `safety/CLEARANCE_CREEPAGE_WORKSHEET.md`.
4. Engage a lab/regulatory specialist.
5. Do not market/sell until compliance is demonstrated.
