# Session Plan

## Session goal
Work Phase 0 software forward: close the two concrete gaps flagged in
`TODO.md` and `docs/backlog.md` that are in scope before hardware bring-up.

## Tasks (in order)

1. **Wire `logging_setup.py` to read `configs/examples/logging.example.yaml`**
   - Backlog P3 item; TODO.md GAP-005 (0% test coverage today).
   - Add a `load_logging_config(path)` that parses the example schema
     (`level`, `destinations`) and a `configure_logging()` that accepts
     either an explicit level or a config path.
   - Add tests in `tests/test_logging.py` covering: valid config, missing
     file, invalid level, invalid destination, defaults.
   - Update `configs/examples/logging.example.yaml` header to remove the
     "NOT YET CONSUMED" note once it's real.

2. **Create the `core_service` entrypoint module**
   - `services/systemd/murderbot-core.service` references
     `murderbot_core.core_service`, which does not exist (TODO.md
     Technical Debt item).
   - Minimal, hardware-independent: load config, build an EventBus, build a
     HostStateMachine, wire transition logging. No hardware I/O — the
     invariant (no self-triggered pulses) holds trivially.
   - Keep it a stub for the audio/RGB/telemetry wiring layers (those are
     Phase 3/4/post-1.0 per AGENTS.md rule 9).

## Files expected to change
- `services/src/murderbot_core/logging_setup.py`
- `services/src/murderbot_core/core_service.py` (new)
- `tests/test_logging.py` (new)
- `tests/test_core_service.py` (new)
- `configs/examples/logging.example.yaml`
- `docs/backlog.md` (mark items done)
- `TODO.md` (mark items done)
- `CHANGELOG.md` (Unreleased entry)
- `docs/software.md` (if it describes the package layout)

## Risks
- `core_service` must not import hardware backends or pull in GPIO libs.
  Only `events`, `state_machine`, `config` — all already pure.
- Config path is runtime/deployed, not committed; entrypoint must accept a
  path argument, not hardcode one.
- Constitution workflow steps 17-19 (traceability, OTS, env contract): no
  new third-party deps and no new env vars, so those checks are N/A — will
  state that explicitly rather than silently skip.

## Resumption notes

- Start: CI green (35 passed, 96% cov). Constitution submodule now checked
  out at v1.52.0 (was missing from working tree).
- Open PR #30 (dependabot constitution bump 93510ce -> 15c0f01) is pending;
  unrelated to this work.

## Outcome

Both tasks completed and verified:

1. `logging_setup.py` reads `configs/examples/logging.example.yaml`'s
   schema (`level`, `destinations`) via `load_logging_config()` +
   `configure_logging(path=...)`. Safe defaults, graceful degradation on
   a bad config, idempotent reconfiguration that doesn't strip
   test-framework handlers. 17 tests in `tests/test_logging.py`.
2. `core_service.py` entrypoint implemented: loads hardware/profiles/
   logging config, builds the bus and state machine, wires one
   observation handler per consumed event type (logs the transition and
   feeds the machine). No hardware I/O. 7 tests in
   `tests/test_core_service.py`, including an import-inspection check
   that the core never binds a hardware/audio/rgb backend.

Final state: 60 tests passing, 98% coverage (331 stmts, 5 missed);
`ruff check`, `ruff format --check`, `mypy --strict` all clean;
`run_declared_tests.sh` passes; secrets sweep clean; Next Steps
procedure validated. Docs/backlog/TODO/CHANGELOG/TEST_PLAN updated and
consistent. Isolated critique pass (separate context) surfaced issues
that were folded back in: duplicate bus subscribers collapsed into one
handler, the event set derived from `HostStateMachine.consumed_event_types`
instead of a re-typed tuple, the hardware-isolation test strengthened to
also assert no hardware side effects during `build_core`, the CHANGELOG
heading duplication fixed, and the systemd unit's AGENTS.md rule
citation corrected.

**Cleared** — this session's outcomes are captured in commit messages,
`CHANGELOG.md`, and `docs/AGENT_HANDOFF.md`.