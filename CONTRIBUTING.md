# Contributing to SMART PLUG PROJECT

Thanks for considering a contribution. This repository mixes software, hardware, and safety evidence, so the bar is a little different from a normal app repo.

**Before you start:** read [`docs/START_HERE.md`](docs/START_HERE.md), [`docs/SAFETY.md`](docs/SAFETY.md), and [`AGENTS.md`](AGENTS.md).

---

## What we welcome

- Documentation fixes, typo fixes, broken links, and better explanations for beginners.
- Indonesian translations and accessibility improvements.
- Test coverage for domain, API, MQTT, web, simulator, and firmware host code.
- Datasheet corrections from primary sources, with URLs and dates.
- KiCad footprint/layout review from experienced hardware engineers.
- Reproducing the digital validation gate and reporting exact results.
- Screenshot updates that match the current UI.

## What we cannot accept

- Claims that the device is safe, certified, production-ready, or ready for fabrication without evidence and sign-off.
- Mains energization procedures aimed at laypeople.
- Fabricated test results, screenshots, logs, or datasheet values.
- Real secrets, tokens, private keys, signing keys, or personal data.
- Changes that put mains on the SELV carrier without a new safety review.
- Removing or bypassing PE, fuse, MOV, TCO, or lockout logic.
- Pressure to label a provisional design as `READY_FOR_FABRICATION` or `READY_FOR_USE`.

---

## Development setup

### Software

```powershell
npm ci
npm run typecheck
npm test
npm run build -w @smartplug/web
```

### Python validation/CAD

```powershell
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe pyyaml kiutils wireviz cadquery trimesh matplotlib numpy pillow reportlab svglib
.venv\Scripts\python.exe scripts\validate_all.py --e2e
```

### Firmware host tests

```powershell
powershell -ExecutionPolicy Bypass -File firmware\test\host\run_tests.ps1
```

### KiCad / CAD (optional)

See [`docs/tutorials/02_SETUP_KICAD.md`](docs/tutorials/02_SETUP_KICAD.md), [`docs/tutorials/04_SETUP_WIREVIZ.md`](docs/tutorials/04_SETUP_WIREVIZ.md), and [`docs/tutorials/05_SETUP_CADQUERY.md`](docs/tutorials/05_SETUP_CADQUERY.md).

---

## Pull request checklist

- [ ] The change is scoped and explained.
- [ ] Tests were run locally; commands and exit codes are in the PR description.
- [ ] New/changed behavior has a test where practical.
- [ ] Documentation is updated (README, docs index, or relevant guide).
- [ ] No real secrets, tokens, private keys, or personal data are included.
- [ ] No new claim of safety, certification, fabrication release, or production readiness without evidence.
- [ ] Hardware changes include a crosscheck and state which values remain `UNVERIFIED`.
- [ ] Screenshots are current and do not show secrets.
- [ ] The change does not add mains to the SELV carrier without a new review.

---

## Commit style

Use short, descriptive subjects in the imperative mood, for example:

```text
docs: add beginner hardware guide
fix(api): reject expired command TTL
hw(psu): document fuse clip rating gap
test(web): cover command APPLIED state
```

Explain *why* in the body when the change is not obvious. Link issues/ADRs where relevant.

---

## Evidence rules

- A test claim needs a command, exit code, and log path.
- A hardware value needs a primary source, URL, access date, and status (`VERIFIED`, `PROVISIONAL`, `UNVERIFIED`).
- Mock/simulator results must be labeled as such. Never report them as HIL or PLN tests.
- If a value is unknown, write `UNKNOWN`, `UNVERIFIED`, or `BLOCKED`. Do not invent it.
- If a source conflicts with existing docs, update the docs and record the conflict.

---

## Hardware contributions

Hardware changes are reviewed more strictly:

1. State the design revision (one revision for all artifacts).
2. Update BOM, wiring, mechanical, safety, validation, and reports together.
3. Run the relevant crosschecks (GPIO, wiring, BOM, PSU, isolation).
4. Mark any unverified creepage/clearance/thermal/hipot value explicitly.
5. Do not send Gerber files to fabrication or claim `READY_FOR_FABRICATION`.
6. Mains work is qualified-personnel/lab only.

---

## Code of conduct

By participating, you agree to follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Be respectful, assume good faith, and keep safety discussions evidence-based.

---

## Security

Do not open a public issue with a real secret or vulnerability details. Follow [`SECURITY.md`](SECURITY.md).

---

## License

By contributing, you agree that your contribution is licensed under the repository’s MIT License. Third-party material remains with its owner; see [`NOTICE.md`](NOTICE.md).
