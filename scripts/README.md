# scripts/

Repository/development automation. Not for hardware bring-up procedures
(those live in `../docs/`, e.g. `../docs/pikvm-setup.md`) or one-off
engineering analysis (`../tools/`).

- `bootstrap-dev-env.sh` — creates `services/.venv`, installs
  `murderbot-core` in editable mode with dev dependencies, and installs
  the pre-commit hooks. Safe to re-run.
