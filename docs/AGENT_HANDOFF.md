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

### Session: 2026-11-16 (finish Phase 0 logging + core_service, PR #33)

- **Accomplishments**: Reviewed, tested, and completed the unfinished
  2026-11-14 work below, which had been parked untested as one WIP
  commit. Fixed what the review found: `load_logging_config()` leaked
  `yaml.YAMLError`/`OSError` (so a malformed `logging.yaml` crashed
  startup instead of degrading); `configure_logging(level=...)` accepted
  unvalidated strings; `build_core()`'s fallback did not apply the
  documented defaults; the hardware-isolation test did not check what it
  claimed; and both delimiter rows in
  `docs/REQUIREMENTS_TRACEABILITY.md` were corrupted, failing
  `check_traceability.sh` for all 13 requirements. Added
  `tests/conftest.py` (root-logger restore), cleared
  `docs/SESSION_PLAN.md`, and wrote the session summary
  (`docs/sessions/2026-11-16-finish-phase0-logging-core-service.md`).
- **Pending Work**: `core_service.main()` has no transport event loop —
  it sets up, logs, and exits 0 — so `murderbot-core.service` is still
  an example unit. Audio/RGB/telemetry/health entrypoints do not exist.
  P0 hardware backlog items (`docs/backlog.md`) all need the bench.
- **Verification Run** (Python 3.14 venv at `services/.venv`; CI uses
  3.11): `cd services && pytest --cov=murderbot_core
  --cov-report=term-missing` — 74 passed, 99% (338 stmts, 4 missed);
  `ruff check .`, `ruff format --check .`, `mypy src` clean;
  `constitution/scripts/check_compliance.sh`, `check_traceability.sh`
  (13/13), `check_secrets.sh`, `check_next_steps.sh`,
  `check_session_summaries.sh`, `check_wiki_links.sh --strict`,
  `check_version_alignment.sh`, and `run_declared_tests.sh . --strict`
  all pass. Constitution submodule at v1.56.0. These numbers supersede
  the ones in the 2026-11-14 entry.
- **Known Blockers**: none for the software; everything further is
  gated on hardware.
- **Instructions for Next Agent**: Read `AGENTS.md` first. The
  `core_service` subscription set is derived from
  `HostStateMachine.consumed_event_types`; add state-affecting events to
  the transition table, not to a literal tuple. Hardware wiring must be
  a separate module that subscribes to the bus —
  `tests/test_core_service.py` fails if `core_service` loads any of
  `murderbot_core.hardware`/`.audio`/`.rgb`/`.telemetry`.

#### Next Steps

**Human action required:** steps 1, 3, 4, and 5.

1. [ ] **HUMAN** — Review and merge pull request #33
   - **Why a human:** merging is the maintainer's decision, and the
     branch carries three changes the session plan did not list (the
     GPU-model wording across the docs, the `secrets-scan` CI job, and
     the `tools/bom_report.py` phase ordering) that need an owner's
     yes or no.
   - **You need:** review access to the repository.
   - **Procedure:**
     1. Read the "Outside the session plan" section of the pull request
        description and decide whether each item stays.
     2. Confirm every CI check on the pull request is green.
     3. Merge, or ask for the unwanted items to be reverted.
   - **Done when:** the pull request shows as merged and CI on `main` is
     green.
2. [ ] **AUTOMATED** — CI (`CI`, `Constitution *` workflows) runs on the
      merge commit, including the new `Secrets scan` job; watch for a red
      run. _(blocked by step 1)_
3. [ ] **HUMAN** — Identify the host PC's GPU model and its POST/BIOS
      output behavior across HDMI/DisplayPort
   - **Why a human:** needs physical access to the desktop PC; the GPU
     model is recorded as `TBD`.
   - **You need:** the host PC powered on, its GPU outputs, and a capture
     bridge connected to the bench Pi.
   - **Procedure:**
     1. Power the host and enter firmware setup.
     2. Note which physical output (HDMI/DisplayPort) carries POST/BIOS.
     3. Record the GPU model and output combination in
        `docs/testing.md` Phase 1 matrix and `docs/backlog.md`.
   - **Done when:** the P0 backlog row for GPU POST behavior has a
     recorded model, output combination, and evidence photo.
4. [ ] **HUMAN** — Acquire/select the Raspberry Pi 4 and compatible
      HDMI-to-CSI capture bridge, and record them in `hardware/bom.csv`
   - **Why a human:** needs a purchase and physical parts on the bench.
   - **Done when:** `hardware/bom.csv` has selected rows with a source.
5. [ ] **HUMAN** — Choose the safe PiKVM power/data cable topology and
      review it against the official PiKVM DIY V2 guide
   - **Why a human:** a wrong cable topology can backfeed power into the
     Pi or the capture bridge; this is a physical-safety decision.
   - **Done when:** `docs/pikvm-setup.md` has a reviewed cable diagram.
6. [ ] **AGENT** — Give `core_service.main()` a real transport event
      loop and add the audio/RGB/telemetry/health entrypoints, each with
      its roadmap phase _(blocked by steps 3–5 and Phase 1 sign-off)_
7. [ ] **AGENT** _(suggestion)_ — Extend the CI lint job to run `ruff`
      (and optionally `mypy`) over `tests/` and `tools/`, which it does
      not cover today (`TODO.md` Testing).

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
