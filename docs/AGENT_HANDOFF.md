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

### Session: 2026-11-14 (Phase 0 software push)

- **Accomplishments**: Wired `logging_setup.py` to read
  `configs/examples/logging.example.yaml`'s schema (`level`,
  `destinations`) via `load_logging_config()` + `configure_logging(path=...)`,
  with safe defaults, graceful degradation on a bad config, and
  idempotent reconfiguration that doesn't strip test-framework handlers.
  Added the `murderbot_core.core_service` entrypoint referenced by
  `services/systemd/murderbot-core.service`: loads hardware/profiles/
  logging config, builds the bus and state machine, and wires a single
  observation handler per consumed event type (logs the transition and
  feeds the machine). Performs no hardware I/O, so the safety invariant
  holds by construction. Struck the RTX 4080 from all docs (GPU moved to
  a separate gaming PC; host GPU model now `TBD`). Added 24 tests;
  coverage 98% (331 stmts, 5 missed, 60/60 passing).
- **Pending Work**: P0 hardware backlog items in `docs/backlog.md`
  (PSU 5VSB rating, Pi/capture bridge selection, host GPU POST behavior,
  safe PiKVM cable topology) — all require physical access to the bench.
  Audio/RGB/telemetry/health entrypoints remain stubs pending their
  phases. Open PR #30 (dependabot constitution bump) is unrelated.
- **Verification Run**: `cd services && pytest --cov` (60 passed, 98%),
  `ruff check`, `ruff format --check`, `mypy --strict` all clean;
  `constitution/scripts/run_declared_tests.sh .` passes; secrets sweep
  clean. Constitution submodule checked out at v1.52.0 (was missing from
  the working tree before this session).
- **Instructions for Next Agent**: Read `AGENTS.md` first (constitution
  override rules are there). Hardware work needs the human in the loop;
  don't fabricate values per `AGENTS.md` rule 1. Phase 2+ (ATX/audio/RGB
  backends) is out of scope until Phase 1's acceptance criteria are met —
  keep them as stubs. The `core_service` subscription set is derived from
  `HostStateMachine.consumed_event_types`; if you add state-affecting
  events, add them to the transition table, not to a literal tuple.

## Next Steps

**Human action required:** steps 1, 3, and 4.

1. [ ] **HUMAN** — Identify the host PC's GPU model and its POST/BIOS
      output behavior across HDMI/DisplayPort
   - **Why a human:** needs physical access to the live desktop PC; the
     GPU is no longer the RTX 4080 and its model is currently `TBD`.
   - **You need:** the host PC powered on, its GPU outputs, and a capture
     bridge connected to the bench Pi.
   - **Procedure:**
     1. Power the host and enter firmware setup.
     2. Note which physical output (HDMI/DisplayPort) carries POST/BIOS.
     3. Record the GPU model and output combination in
        `docs/testing.md` Phase 1 matrix and `docs/backlog.md`.
   - **Done when:** the P0 backlog row for GPU POST behavior has a
     recorded model, output combination, and evidence photo.

2. [ ] **AGENT** — Wire the audio/RGB/telemetry/health entrypoints once
      their phases are reached _(blocked by step 1 and Phase 1 sign-off)_
3. [ ] **HUMAN** — Acquire/select the Raspberry Pi 4 and compatible
      HDMI-to-CSI capture bridge, and record them in `hardware/bom.csv`
   - **Why a human:** needs a purchase and physical parts on the bench.
   - **Done when:** `hardware/bom.csv` has selected rows with a source.
4. [ ] **HUMAN** — Choose the safe PiKVM power/data cable topology and
      review it against the official PiKVM DIY V2 guide
   - **Why a human:** a wrong cable topology can backfeed power into the
     Pi or the capture bridge; this is a physical-safety decision.
   - **Done when:** `docs/pikvm-setup.md` has a reviewed cable diagram.
5. [ ] **AUTOMATED** — CI runs lint, format, mypy, and pytest on every
      push/PR; watch the `lint-type-test` job for red runs.
6. [ ] **AGENT** _(suggestion)_ — Add a `pytest` fixture that snapshots
      and restores the root logger's handlers, so future logging tests
      don't couple to global state.

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
