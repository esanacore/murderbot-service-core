# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/) once
a `v0.1.0` tag is cut — see `docs/versioning-and-releases.md`.

## [Unreleased]

### Added

- `services/src/murderbot_core/core_service.py`: the entrypoint module
  referenced by `services/systemd/murderbot-core.service`. Loads
  `hardware.yaml`/`profiles.yaml`/`logging.yaml` from a config directory
  (default `/etc/murderbot`, overridable as the first CLI argument),
  builds the event bus and state machine, and subscribes one handler per
  event type the machine consumes (derived from the new
  `HostStateMachine.consumed_event_types`) that logs the event and feeds
  the machine. Performs no hardware I/O, so the safety invariant (a
  restart must never assert a pulse, play audio, or illuminate LEDs)
  holds by construction; `tests/test_core_service.py` proves it by
  running the entrypoint in a fresh interpreter and asserting that no
  hardware/audio/RGB/telemetry package was loaded. No transport event
  loop exists yet, so the process currently sets up, logs, and exits 0
  (`docs/software.md`).
- `services/src/murderbot_core/logging_setup.py` now reads
  `configs/examples/logging.example.yaml`'s schema (`level`,
  `destinations`) via `load_logging_config()`, instead of taking only a
  hardcoded numeric level. `configure_logging()` accepts a parsed
  `LoggingConfig`, an explicit `level`, or a config `path`; rejects an
  unknown level or destination with `LoggingConfigError` before touching
  the root logger; and on reconfiguration replaces only the handlers it
  installed itself. A missing, unreadable, or malformed `logging.yaml`
  raises `LoggingConfigError`, which `core_service` handles by falling
  back to the defaults (INFO, stdout) rather than refusing to start.
  Covered by `tests/test_logging.py`.
- `secrets-scan` job in `.github/workflows/ci.yml`, running
  `constitution/scripts/check_secrets.sh` on every push and PR. This
  closes the P2 backlog item for formal secrets-scanning beyond
  pre-commit's `detect-private-key` hook (`docs/security.md`).
- `tests/conftest.py`: an autouse fixture that restores the root
  logger's handlers and level after every test, so logging tests cannot
  leak state into each other.
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
  The RTX 4080 has been moved back to the user's gaming PC and out of
  Murderbot. The host PC's GPU is a GTX 1060 6 GB, named in `README.md`,
  `AGENTS.md`, and `wiki/Home.md`; the other files refer to the host
  PC's video output generically. A Quadro P2000 may be added later. The
  corresponding P0 backlog item ("Test RTX 4080 POST output behavior
  across HDMI/DisplayPort") now names the GTX 1060 and asks for a repeat
  if the Quadro P2000 is installed.
- `tools/bom_report.py` lists phases in numeric order (`0`, `0-1`, `1`,
  `1-4`, `2`, ...) instead of every single phase before every range.

### Fixed

### Removed

### Security

### Notes

- No hardware has been wired into the host PC yet. Nothing before `v0.1.0`
  should be treated as validated against real hardware.
