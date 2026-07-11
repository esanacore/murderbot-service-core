# Agent Handoff

This document helps transition work between different AI agent sessions or different agents.

## How to Handoff

When you are finishing a task or session, record the state here or in a dedicated `HANDOFF.md` file:

1. **Current Status**: What was achieved?
2. **Next Steps**: What should the next agent do first?
3. **Known Blockers**: What issues were encountered?
4. **Context Hints**: Are there specific files or discussions the next agent should read?

## Handoff Log

Newest entry first. Copy the template below for a new entry.

### Session: 2026-07-11

- **Accomplishments**: Initial repository bootstrap (governance docs,
  `docs/`, `.github/`, hardware-independent `murderbot_core` package,
  35 passing tests); pushed to GitHub as
  `esanacore/murderbot-service-core` (public); adopted Eric's Engineering
  Constitution as the `constitution/` submodule and reconciled its
  template files with the pre-existing docs (`docs/decisions/` kept as
  the canonical ADR location over the constitution's `docs/adr/`
  default; `docs/architecture.md`/`docs/troubleshooting.md` kept over
  the constitution's uppercase equivalents; `PRODUCT_REQUIREMENTS.md`
  and `REQUIREMENTS_TRACEABILITY.md` populated from the existing
  FR-01..FR-10/NFR-01..NFR-03 IDs).
- **Pending Work**: P0 hardware backlog items in `../docs/backlog.md`
  (PSU rating, Pi/capture bridge selection) — all require physical
  access to the hardware, not further repo work. GitHub repository
  settings (branch protection, auto-delete-head-branches) recommended by
  `../constitution/INTEGRATION.md`'s "Repository Settings Checklist" not
  yet applied.
- **Verification Run**: `cd services && pytest` (35 passed), `ruff check`,
  `ruff format --check`, `mypy --strict` all clean;
  `constitution/scripts/check_compliance.sh`,
  `check_traceability.sh`, and `run_declared_tests.sh --strict` all pass.
- **Instructions for Next Agent**: Read `AGENTS.md` first (constitution
  override rules are there). Hardware work needs the human in the loop;
  don't fabricate values per `AGENTS.md` rule 1.

### Session: [Date/Time]

- **Accomplishments**: <!-- List here -->
- **Pending Work**: <!-- List here -->
- **Verification Run**: <!-- Tests run and results -->
- **Instructions for Next Agent**: <!-- Be specific -->
