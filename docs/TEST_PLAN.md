# Test Plan

Defines how this repository is tested, what coverage it targets, and where
gaps currently exist. See `testing.md` for the full bench/integration/
fault-injection matrix that covers hardware-dependent behavior this
document's automated suite cannot reach.

## Test Strategy

- **Unit tests**: isolated, hardware-independent behavior (event bus,
  state machine, config parsing, mock hardware/audio/RGB/telemetry
  interfaces). Location: `tests/` (repo root), run via `pytest` from
  `services/`.
- **Integration tests**: none automated yet — no runnable multi-service
  process exists (`software.md` "What's implemented today vs. planned").
- **End-to-end / bench tests**: real hardware behavior (PiKVM capture,
  ATX pulses, audio, RGB). Manual, tracked in `testing.md`'s matrix, not
  part of `pytest`.

## How to Run Tests

- Full suite: `cd services && pytest`
- With coverage: `cd services && pytest --cov=murderbot_core --cov-report=term-missing`
- A single test or subset: `cd services && pytest tests/test_state_machine.py`

## Coverage Targets

| Scope | Metric | Floor |
| --- | --- | --- |
| Repository default | Line / statement | 80% |
| State machine (`state_machine.py`) | Branch | 100% — every transition table entry and the FAULT-recovery guard clause must be exercised |
| ATX/GPIO interface contracts (`hardware/`) | Line | 100% of the mock; real backends are excluded from this target until they exist |

New or modified code should meet the floor on its own, not lean on
untouched legacy code.

## Continuous Coverage Evaluation

| Date | Overall coverage | Notes |
| --- | --- | --- |
| 2026-07-11 | 96% (226 stmts, 10 missed, 35/35 tests passing) | Baseline. `logging_setup.py` is 0% covered (trivial `logging.basicConfig` wrapper, GAP-005 below); everything else implemented is 96-100%. |

A downward trend is a signal to investigate, even when the number stays
above the floor.

## Coverage Gap Log

| Gap ID | Area / behavior | Risk | Related requirement | Status | TODO ref |
| --- | --- | --- | --- | --- | --- |
| GAP-001 | Real ATX/GPIO backend (no mock) | High — safety-critical fail-open behavior | FR-03, FR-07, NFR-02 | Open | `TODO.md` Technical Debt |
| GAP-002 | Real audio/RGB backends | Medium | FR-06, FR-08 | Open | `TODO.md` Technical Debt |
| GAP-003 | Runtime profile *selection* logic (vs. parsing) | Medium | FR-08 | Open | `TODO.md` Technical Debt |
| GAP-004 | Cross-service fault-injection (bench-only, no unit-test equivalent) | High — this is the core safety property of the whole design | FR-05, NFR-02 | Open | `testing.md` "Fault-injection tests" |
| GAP-005 | `logging_setup.py` untested (0% coverage) | Low | n/a | Open | `TODO.md` Testing |

## Requirement Coverage

The authoritative mapping lives in
[`REQUIREMENTS_TRACEABILITY.md`](REQUIREMENTS_TRACEABILITY.md). Every
requirement there currently has at least a software-layer test or an
explicit bench-test pointer — see that file's Coverage Summary.
