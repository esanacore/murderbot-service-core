# Command Reference

Quick reference for common commands. All Python commands assume the
`services/.venv` environment is active (`source services/.venv/bin/activate`)
— see [`SETUP.md`](SETUP.md).

## Development

- `bash scripts/bootstrap-dev-env.sh`: create/refresh the dev venv, install
  `murderbot-core` editable + dev deps, install pre-commit hooks.

## Testing

- `cd services && pytest`: run the full test suite (also `docs/TEST_PLAN.md`'s
  declared "Full suite" command).
- `cd services && pytest --cov=murderbot_core --cov-report=term-missing`: run
  with coverage.
- `cd services && pytest tests/test_state_machine.py`: run a single test file.
- `cd services && pytest -k <expression>`: run a subset by name.

## Linting & Formatting

- `cd services && ruff check .`: lint.
- `cd services && ruff format .`: format (add `--check` to verify without
  writing).
- `cd services && mypy src`: type-check (`--strict`, configured in
  `services/pyproject.toml`).
- `pre-commit run --all-files`: run every pre-commit hook against the whole
  tree.

## Hardware / BOM tooling

- `python3 tools/bom_report.py`: summarize `hardware/bom.csv` target-cost
  totals by phase and status.

## Constitution checkers

Run from the repo root, through the `constitution/` submodule:

- `bash constitution/scripts/check_compliance.sh`: verify required/recommended
  governance files are present.
- `bash constitution/scripts/check_traceability.sh`: verify every requirement
  ID in `PRODUCT_REQUIREMENTS.md` has a matching row in
  `REQUIREMENTS_TRACEABILITY.md`.
- `bash constitution/scripts/check_version_alignment.sh`: verify pinned
  constitution version references aren't stale.
- `bash constitution/scripts/run_declared_tests.sh .`: run this repo's
  declared "Full suite" command the same way CI does.

## Operations

No production/runtime deployment exists yet (`docs/OPERATIONS.md`) — this
project is pre-hardware-bring-up.
