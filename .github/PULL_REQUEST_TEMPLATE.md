# Pull Request

## Summary

<!-- What changed and why? Link issues/ADRs. -->

## Type

- [ ] Bug fix
- [ ] Feature
- [ ] Documentation
- [ ] Tests
- [ ] Hardware/PCB/CAD
- [ ] Safety/research evidence
- [ ] CI/tooling
- [ ] Refactor (no behavior change)

## Evidence

<!-- Paste the exact commands and results. Do not claim a test you did not run. -->

```text
command:
exit code:
log path:
```

## Safety and compatibility

- [ ] No mains was energized.
- [ ] No new `READY_FOR_FABRICATION` or `READY_FOR_USE` claim.
- [ ] PE/fuse/MOV/TCO/isolation are not bypassed.
- [ ] No mains added to the SELV carrier without a new review.
- [ ] Unverified values are marked `UNKNOWN`, `UNVERIFIED`, or `BLOCKED`.
- [ ] No real secrets, tokens, private keys, or personal data.
- [ ] API/MQTT contract changes are documented.

## Documentation

- [ ] README/docs index updated where needed.
- [ ] New terms added to `docs/GLOSSARY.md` where needed.
- [ ] Status/validation evidence updated.
- [ ] Screenshots refreshed if UI changed and contain no secrets.

## Checklist

- [ ] `npm run typecheck` passes.
- [ ] `npm test` passes.
- [ ] `npm run build -w @smartplug/web` passes (if web changed).
- [ ] Relevant hardware crosschecks pass (if hardware changed).
- [ ] The change is scoped; unrelated formatting is avoided.
