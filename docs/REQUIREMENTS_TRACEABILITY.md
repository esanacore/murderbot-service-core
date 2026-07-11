# Requirements Traceability Matrix

Links each requirement in [`PRODUCT_REQUIREMENTS.md`](PRODUCT_REQUIREMENTS.md)
to its verifying tests and current status. This project is pre-hardware
bring-up, so most rows are `Not Started` by design — see `../ROADMAP.md`.

It is a living document. Update it in the same change that adds, modifies,
or verifies a requirement.

## Conventions

- **Requirement ID**: matches the ID in `PRODUCT_REQUIREMENTS.md` (`FR-01`...`FR-10`, `NFR-01`...`NFR-03`).
- **Status**: `Not Started`, `In Progress`, `Verified`, or `Deferred`.
- Hardware-dependent requirements cannot be `Verified` until the matching
  row in `testing.md`'s bench/integration matrix has recorded evidence
  (photo, scope capture, or measurement).

## Functional Requirements

| Requirement ID | Level | Description | Verifying Tests | Status |
| --- | --- | --- | --- | --- |
| FR-01 | MUST | Reachable while PC off, PSU connected | `testing.md` Phase 1 stability test | Not Started |
| FR-02 | MUST | Remote BIOS-level keyboard/mouse/video | `testing.md` Phase 1 POST/BIOS test | Not Started |
| FR-03 | MUST | Isolated remote power/reset | `testing.md` Phase 2 pulse-timing test | Not Started |
| FR-04 | MUST | Startup triggers from main-rail state | `tests/test_state_machine.py::test_main_rail_on_moves_standby_to_host_starting` (software logic only — hardware-side trigger is `testing.md` Phase 2) | In Progress |
| FR-05 | MUST | Audio/RGB faults don't disable PiKVM/ATX | `testing.md` "Fault-injection tests" (bench-only; no unit-test equivalent since it requires real service processes) | Not Started |
| FR-06 | MUST | NeoPixel data level-shifted 3.3V to 5V | `testing.md` Phase 4 logic-level test | Not Started |
| FR-07 | MUST | No high-current loads from Pi GPIO power pins | `power-design.md` power-path inspection | Not Started |
| FR-08 | SHOULD | Per-profile config (Windows/Linux/boot/idle/fault) | `tests/test_config.py::test_load_profiles_parses_named_profiles` (parsing only — runtime profile *selection* logic not yet implemented) | In Progress |
| FR-09 | SHOULD | Keyed/labeled connectors + test points | `wiring.md` physical design review | Not Started |
| FR-10 | SHOULD | CI: lint, unit tests, doc checks on PR | `../.github/workflows/ci.yml` | Verified |

## Non-Functional Requirements

| Requirement ID | Level | Description | Verifying Tests | Status |
| --- | --- | --- | --- | --- |
| NFR-01 | MUST | No public PiKVM exposure; no committed secrets | `../.gitignore` secret patterns + `../.pre-commit-config.yaml`'s `detect-private-key` hook (partial — no CI secret-scan yet, see `backlog.md`) | In Progress |
| NFR-02 | MUST | Fail-open ATX on any service crash | `tests/test_state_machine.py::test_fault_detected_from_any_non_fault_state`, `::test_fault_cleared_returns_to_standby_only_if_main_rail_confirmed_off` (state-machine logic only; real GPIO fail-open behavior is `testing.md` Phase 2 fault-injection) | In Progress |
| NFR-03 | MUST | Hardware code behind Protocol + mock | `tests/test_hardware_interfaces.py` (all rows) | Verified |

## Coverage Summary

| Metric | Count |
| --- | --- |
| Total requirements | 13 |
| Verified | 2 |
| In progress | 4 |
| Not started | 7 |
| Requirements without a verifying test (gaps) | 0 — every row has at least a partial/software-layer test or an explicit bench-test pointer |
