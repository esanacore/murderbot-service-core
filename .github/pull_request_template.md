## Summary

<!-- What does this change do, and why? -->

## Type of change

- [ ] Software (services/, host-agents/, tools/)
- [ ] Hardware documentation / design (docs/power-design.md, docs/wiring.md, hardware/, electronics/, cad/)
- [ ] Documentation only
- [ ] CI / tooling

## Checklist (see AGENTS.md "Definition of done")

- [ ] `ruff check`, `ruff format --check`, and `mypy` pass locally (`services/`)
- [ ] `pytest` passes, and new/changed behavior has a test
- [ ] Hardware-facing code sits behind a `Protocol`/mock interface (no untested hardware branches)
- [ ] Relevant `docs/*.md` updated
- [ ] `hardware/bom.csv` updated if a physical part changed
- [ ] `CHANGELOG.md` `[Unreleased]` updated
- [ ] No secrets, credentials, or copyrighted media added (checked the diff, not just filenames)
- [ ] New/updated ADR in `docs/decisions/` if this changes the architecture

## Failure-domain check (required for anything touching ATX, power, audio, or RGB)

- [ ] This change cannot cause a personality-service (audio/RGB/telemetry) failure to affect PiKVM or ATX control (see `docs/architecture.md`)
- [ ] Default state on error/crash is: ATX open, RGB off, audio muted (see `AGENTS.md` rule 5)

## Testing performed

<!-- What did you actually run/verify? Bench hardware tests go in docs/testing.md's matrix, not just here. -->
