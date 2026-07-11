# docs/adr/ vs docs/decisions/

This project's Architecture Decision Records live at
[`../decisions/`](../decisions/), not in this directory. `docs/decisions/`
was established before this repository adopted
[Eric's Engineering Constitution](../../constitution/CONSTITUTION.md),
already contains real, populated ADRs (0001: single-Pi architecture; 0002:
repository structure and licensing), and is referenced throughout
`docs/`, `AGENTS.md`, and the PR template. Per
`../../constitution/INTEGRATION.md` ("project-specific rule wins"), this
repository keeps `docs/decisions/` as canonical rather than migrating.

This directory (`docs/adr/`) is kept present — rather than deleted —
because `constitution/scripts/check_compliance.sh` looks for it as a
recommended path, and because a future contributor who only knows the
constitution's convention should land here and be redirected rather than
conclude no ADRs exist.

See [`../decisions/README.md`](../decisions/README.md) for the actual ADR
index and format.
