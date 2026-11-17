# Backlog

Working backlog for Phase 0–5 (`ROADMAP.md`). This is the project-board
equivalent until/unless a GitHub Projects board is stood up — if one is
added later, this table should link to it rather than duplicate it.

| Priority | Task | Completion evidence |
|---|---|---|
| P0 | Identify exact PSU model and documented 5VSB rating | Photo/manual citation and recorded rating in `docs/power-design.md` |
| P0 | Acquire or select Raspberry Pi 4 and compatible capture bridge | `hardware/bom.csv` rows marked selected with source |
| P0 | Identify host PC GPU model and its POST output behavior across HDMI/DisplayPort | Test matrix results + photos, `docs/testing.md` |
| P0 | Choose safe PiKVM power/data cable topology | Diagram reviewed against official DIY guide, `docs/pikvm-setup.md` |
| P1 | Measure Pi/capture idle and peak current | Logged measurements + instrument details, `docs/power-design.md` |
| P1 | Prototype optoisolated PWR/RESET circuit | Schematic, bench test, default-open fault test, `docs/testing.md` |
| P1 | Implement and test software state machine | CI results and transition coverage — **done**, see `tests/test_state_machine.py` |
| P2 | Prototype I²S audio and printed enclosure | Playback test and mounted-fit photos |
| P2 | Prototype level-shifted 10-pixel RGB output | Scope/meter check, current measurement, thermal check |
| P3 | Design integrated carrier PCB after pinout freeze | Reviewed schematic and fabrication files, `electronics/pcb/` |
| P3 | Add Windows and Linux host agents | Authenticated heartbeat and telemetry tests, `host-agents/` |

## Repository/tooling backlog (not from the original hardware report)

| Priority | Task | Notes |
|---|---|---|
| P1 | Wire up `.github/workflows/ci.yml` against a real `services/` package (done — verify it stays green as code lands) | See `.github/workflows/ci.yml` |
| P2 | Implement `murderbot_core.core_service` entrypoint so `services/systemd/murderbot-core.service` is installable | Done — config load + event bus + state machine + transition logging, covered by `tests/test_core_service.py`. The process has no transport event loop yet (sets up, logs, exits 0), so the unit is still an example, not something to enable. Audio/RGB/telemetry/health entrypoints still pending their phases. |
| P2 | Decide on docs-site generation (mkdocs vs. plain GitHub rendering) | Currently plain markdown; revisit once `docs/` grows large enough to need navigation/search |
| P2 | Formal secrets-scanning in CI beyond pre-commit's `detect-private-key` | Done — `secrets-scan` job in `.github/workflows/ci.yml` runs `constitution/scripts/check_secrets.sh` on every PR and push |
| P3 | LAN-boundary threat model for post-1.0 REST API/dashboard | `docs/security.md` known gap; only relevant once `ROADMAP.md` post-1.0 items start |
| P3 | Wire `logging_setup.py` to read `configs/examples/logging.example.yaml`'s schema instead of a hardcoded level argument | Done — `load_logging_config` + `configure_logging(path=...)`, covered by `tests/test_logging.py` |

## How to use this file

- New P0/P1 items block the current `ROADMAP.md` phase; P2/P3 do not.
- When an item completes, move it (with its evidence link) into the
  relevant `docs/*.md` "Status" table rather than just deleting the row —
  this file tracks *open* work, not history (that's `CHANGELOG.md`'s job).
