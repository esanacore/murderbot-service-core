# Contributing to Murderbot Service Core

Thanks for your interest. This is currently a solo hobbyist project run at
professional-engineering rigor, so the process below applies whether you're
the maintainer working alone or an outside contributor.

This project follows [Eric's Engineering Constitution](constitution/CONSTITUTION.md);
these project-specific ground rules take priority over its universal
defaults where they differ (`constitution/INTEGRATION.md`). AI agents:
also read `AGENTS.md` and `constitution/AI_WORKFLOW.md` before starting.

## Ground rules

1. **PiKVM is the critical service.** Any change that touches power, ATX
   control, or capture must explain, in the PR description, how it cannot
   regress PiKVM availability. See `docs/architecture.md` for the failure
   domains.
2. **No fabricated hardware facts.** Pinouts, PSU ratings, current draw, and
   similar values must cite a datasheet, a manual, or a measurement (with
   instrument and method). Unmeasured values are marked `TBD` — see
   `AGENTS.md`.
3. **No secrets, credentials, or copyrighted media** in the repository. See
   `SECURITY.md` and `assets/README.md`.
4. **Use feature branches and pull requests**, even for solo work, so CI and
   the review checklist run on every change.
5. **Every hardware change** requires an updated BOM row
   (`hardware/bom.csv`), a wiring/diagram update if applicable, and — if it
   changes the architecture — a new or amended ADR in `docs/decisions/`.

## Development setup

```bash
git clone <this repo>
cd murderbot-service-core
cd services
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install   # from repo root: pre-commit install -c ../.pre-commit-config.yaml
pytest
```

## Code style

- Python, type-hinted, formatted and linted with `ruff`, type-checked with
  `mypy`. Configuration lives in `services/pyproject.toml`.
- Hardware-facing code (GPIO, audio, RGB, telemetry) must be written behind
  a `Protocol`/abstract interface with a mock implementation, so unit tests
  do not require a Raspberry Pi. See `services/src/murderbot_core/hardware/`
  for the pattern.
- No global mutable state; prefer explicit configuration objects passed
  into constructors (see `docs/software.md`).

## Commit / PR process

1. Open an issue first for anything beyond a trivial fix (use the templates
   under `.github/ISSUE_TEMPLATE/`).
2. Branch from `main`: `feature/<short-name>` or `fix/<short-name>`.
3. Keep commits small and reviewable; write commit messages that explain
   *why*, not just *what*.
4. Open a PR using the template — it includes a checklist covering tests,
   docs, BOM, and safety-domain isolation.
5. CI (lint, type-check, unit tests, markdown/link check) must pass before
   merge.
6. Update `CHANGELOG.md` under `[Unreleased]`.

## Documentation is not optional

Every subsystem is expected to eventually document: purpose, architecture,
interfaces, dependencies, power requirements, known limitations, future
improvements, and testing procedures (see `docs/`). If your change touches
a subsystem lacking that documentation, add or stub it rather than skipping
it — an explicit `TBD` is acceptable; silence is not.

## Questions

See [`SUPPORT.md`](SUPPORT.md).
