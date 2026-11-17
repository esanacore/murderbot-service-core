# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/) once
a `v0.1.0` tag is cut — see `docs/versioning-and-releases.md`.

## [Unreleased]

### Added

- `services/src/murderbot_core/core_service.py`: the entrypoint module
  referenced by `services/systemd/murderbot-core.service`. Loads
  `hardware.yaml`/`profiles.yaml`/`logging.yaml`, builds the event bus
  and state machine, and wires a transition logger plus the
  observation->state-machine feed. Performs no hardware I/O, so the
  safety invariant (a restart must never assert a pulse, play audio, or
  illuminate LEDs) holds by construction. Covered by
  `tests/test_core_service.py`, which also asserts the module imports
  no hardware/audio/rgb backend.
- `services/src/murderbot_core/logging_setup.py` now reads
  `configs/examples/logging.example.yaml`'s schema (`level`,
  `destinations`) via `load_logging_config()`, instead of taking only a
  hardcoded numeric level. `configure_logging()` accepts a parsed
  `LoggingConfig`, an explicit `level`, or a config `path`, degrades
  gracefully on a bad logging config, and is idempotent on reconfigure.
  Covered by `tests/test_logging.py` (17 tests).
- `secrets-scan` job in `.github/workflows/ci.yml`, running
  `constitution/scripts/check_secrets.sh` on every push and PR. This
  closes the P2 backlog item for formal secrets-scanning beyond
  pre-commit's `detect-private-key` hook (`docs/security.md`).
- `CLAUDE.md` and `.goosehints` now carry real, verified install
  instructions for gstack (`garrytan/gstack`) and goose/goosetown
  (`aaif-goose` org) instead of only naming the tools, matching the fix
  landed upstream in `constitution/` v1.31.0 (tagged and pushed). Bun,
  gstack (including the `/browse` Playwright workaround for this
  machine's Ubuntu 26.04), goose CLI, and goosetown (cloned to
  `~/Repos/goosetown`) are all installed and verified on this machine.
- `constitution/` submodule bumped to v1.32.0, which adds
  `constitution/scripts/setup-machine.sh` — a one-time, per-machine
  installer for Bun/gstack/goose/goosetown, idempotent, deliberately
  kept separate from `bootstrap.sh`. Ran it here as a sanity check;
  correctly detected everything already installed and skipped cleanly.
- Initial repository scaffold: documentation set (`docs/`), governance
  files, `.github/` templates and CI, hardware-independent `murderbot_core`
  Python package skeleton (event types, state machine, config parsing,
  mock hardware/audio/RGB/telemetry interfaces), and unit tests for the
  state machine.
- ADR 0001: single Raspberry Pi 4 for both PiKVM and personality services.
- ADR 0002: repository structure and licensing approach.
- Adopted [Eric's Engineering Constitution](https://github.com/esanacore/engineering-constitution)
  as the `constitution/` submodule, plus its governance scaffolding
  (`TODO.md`, tool-specific agent instruction files, `docs/PRODUCT_REQUIREMENTS.md`
  + `docs/REQUIREMENTS_TRACEABILITY.md` mapping the existing FR-01..FR-10/NFR-01..NFR-03
  IDs, `docs/TEST_PLAN.md`, `docs/MVP_BACKLOG.md`, `docs/OPERATIONS.md`, and
  CI gates for constitution version/compliance/tests/doc-freshness).

### Changed

- Removed all references to the RTX 4080 GPU across `README.md`,
  `AGENTS.md`, `ROADMAP.md`, `docs/requirements.md`,
  `docs/PRODUCT_REQUIREMENTS.md`, `docs/backlog.md`, `docs/testing.md`,
  `docs/pikvm-setup.md`, `docs/wiring.md`, `docs/troubleshooting.md`,
  `docs/MVP_BACKLOG.md`, `docs/architecture.md`, and `wiki/Home.md`.
  The GPU has been moved back to the user's gaming PC and out of
  Murderbot; the host PC's GPU model is now recorded as `TBD` in those
  files rather than asserted as a specific part. The corresponding P0
  backlog item ("Test RTX 4080 POST output behavior across
  HDMI/DisplayPort") was reworded to be GPU-agnostic.
- `services/src/murderbot_core/core_service.py`'s bus wiring no longer
  registers the transition logger and the state-machine feed as
  separate subscribers for the same six event types (each event was
  handled twice). They are now a single handler per event type, and the
  event set is derived from `HostStateMachine.consumed_event_types`
  rather than re-typed, so it stays in sync with the transition table.
- `services/src/murderbot_core/logging_setup.py`'s `configure_logging`
  installs only handlers tagged `_MurderbotHandler`, so idempotent
  reconfiguration removes its own handlers without stripping test
  frameworks' or application handlers from the root logger.

### Fixed

### Removed

### Security

### Notes

- No hardware has been wired into the host PC yet. Nothing before `v0.1.0`
  should be treated as validated against real hardware.
