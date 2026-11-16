# Deliverables

This folder is generated from actual artifacts. It does not contain placeholders.

- `manifest.json` — all 26 deliverable categories, 269 tracked artifacts (as of the REV_C documentation refresh), SHA-256 hashes, statuses, blockers, git commit.
- `CHECKSUMS.sha256` — SHA-256 list for the manifest artifacts.
- `FINAL_ENGINEERING_REPORT.md` — final handoff report.

The manifest includes the beginner guides, architecture/hardware/software/testing/safety docs, FAQ/glossary, repository policy files, and GitHub templates. `missing_artifacts: 0` means every path in the curated 26-category manifest exists; it does not mean every possible file in the working tree is included.

## Status

`device_hardware_status`: `ENGINEERING_REVIEW_REQUIRED`
`digital_status`: `PARTIAL_DIGITAL`
`phase_1_status`: `PARTIAL_PROVISIONAL`
`phase_2_status`: `PARTIAL_DIGITAL`
`release`: `NOT_FOR_FABRICATION`

## Rule

A hash in the manifest must match the actual file. If a file changes, regenerate the manifest. A missing/blocked artifact is listed with its blocker; it is not silently omitted.
