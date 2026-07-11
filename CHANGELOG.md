# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/) once
a `v0.1.0` tag is cut — see `docs/versioning-and-releases.md`.

## [Unreleased]

### Added

- `CLAUDE.md` and `.goosehints` now carry real, verified install
  instructions for gstack (`garrytan/gstack`) and goose/goosetown
  (`aaif-goose` org) instead of only naming the tools, matching the fix
  landed upstream in `constitution/` v1.31.0 (tagged and pushed). Bun,
  gstack (including the `/browse` Playwright workaround for this
  machine's Ubuntu 26.04), goose CLI, and goosetown (cloned to
  `~/Repos/goosetown`) are all installed and verified on this machine.
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

### Fixed

### Removed

### Security

### Notes

- No hardware has been wired into the host PC yet. Nothing before `v0.1.0`
  should be treated as validated against real hardware.
