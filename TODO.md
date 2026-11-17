# TODO

This file is the living roadmap for the project, per
[Eric's Engineering Constitution](constitution/CONSTITUTION.md) Principle 3.

The authoritative, priority-ranked hardware/software backlog lives in
[`docs/backlog.md`](docs/backlog.md) and the phased plan in
[`ROADMAP.md`](ROADMAP.md) — this file is the constitution-mandated entry
point that mirrors and supplements it. When the two drift, `docs/backlog.md`
is canonical for hardware-phase sequencing; update both in the same change.

## Features

- [ ] Phase 1: PiKVM core bring-up and bench proof (`ROADMAP.md`).
- [ ] Phase 2: Standby power + optoisolated ATX control (`docs/backlog.md` P0/P1 items).
- [ ] Phase 3: Startup audio (I2S amplifier, printed enclosure).
- [ ] Phase 4: Addressable RGB with brightness cap.
- [ ] Post-1.0: REST API, web dashboard, Home Assistant integration (`ROADMAP.md`).

## Technical Debt

- [x] `services/systemd/murderbot-core.service`'s entrypoint module
      `murderbot_core.core_service` is implemented (config load + bus +
      state machine + transition logging). See `docs/software.md`.
- [ ] The other `services/systemd/*.service` units still reference
      entrypoint modules that don't exist (`murderbot_core.audio_service`,
      `.rgb_service`, `.telemetry_service`, `.health_check`) — each lands
      with its roadmap phase (`AGENTS.md` rule 9).
- [ ] `murderbot_core.core_service.main()` has no transport event loop
      yet: it sets up, logs, and exits 0. Blocking on a real event source
      (PiKVM GPIO daemon / host-agent socket) is Phase 2+ work; until
      then `murderbot-core.service` must not be enabled on a device.
- [ ] `hardware.yaml`'s `*_enabled` flags are parsed but not yet consumed
      by any code path (`docs/software.md` note) — the first real backend
      must gate on them.
- [x] `logging_setup.py` reads `configs/examples/logging.example.yaml`'s
      schema (`level`, `destinations`) and is covered by
      `tests/test_logging.py`. See `docs/backlog.md` P3 item.

## Refactoring

- [ ] None identified yet — revisit once real GPIO/audio/RGB backends exist
      and the `Protocol` interfaces have been exercised against real hardware.

## Testing

- [ ] Bench/integration/fault-injection test matrix in `docs/testing.md` is
      entirely unexecuted (pre-hardware-bring-up). Each row needs evidence
      recorded once Phase 1+ starts.
- [x] GAP-005 (`docs/TEST_PLAN.md`): `logging_setup.py` test coverage
      added — `tests/test_logging.py`, 100% line coverage.
- [ ] CI lints and formats only `services/` (`ruff check .` runs there),
      so `tests/` and `tools/` are not covered by `ruff`/`mypy`. Decide
      whether to extend the CI job to them.

## Documentation

- [ ] Fill in `docs/wiring.md` pinouts as they're confirmed against manuals
      + a meter (currently all `TBD` by design — see `AGENTS.md` rule 1).
- [ ] Record the PiKVM image version/checksum in `docs/pikvm-setup.md` once
      Phase 0 flashing happens.

## Nice-to-Have

- [ ] OLED status display, environmental monitoring, plugin architecture,
      AI personality layer — see `ROADMAP.md` post-1.0 list for the full,
      deliberately-ordered set.
