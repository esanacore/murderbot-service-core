# Software Architecture

## Layout

```
services/
├── pyproject.toml
└── src/murderbot_core/
    ├── events.py        # Event types (dataclasses/enums), the event bus
    ├── state_machine.py # STANDBY/HOST_STARTING/HOST_RUNNING/HOST_SHUTTING_DOWN/FAULT
    ├── config.py         # YAML config loading/validation (configs/examples/)
    ├── logging_setup.py  # Structured logging setup shared by all services
    ├── core_service.py   # Entrypoint for murderbot-core.service (config load + bus + state machine + transition logging)
    ├── hardware/          # ATX/GPIO Protocol interfaces + mock implementation
    ├── audio/             # Audio-service Protocol interface + mock implementation
    ├── rgb/               # RGB-service Protocol interface + mock implementation
    └── telemetry/         # Telemetry Protocol interface + mock implementation
```

## Services (systemd units, `services/systemd/`)

| Service | Purpose | Dependencies |
|---|---|---|
| `murderbot-core.service` | Owns the state machine, events, and profile selection | GPIO abstraction only; no direct PiKVM modification. |
| `murderbot-audio.service` | Receives events and plays approved local clips | ALSA/I²S, host-on state. |
| `murderbot-rgb.service` | Runs animations with current and brightness limits | GPIO/SPI backend, level shifter, host-on state. |
| `murderbot-telemetry.service` | Consumes optional host-agent metrics | Network or serial transport; optional. |
| `murderbot-health.timer` | Periodic self-test and status summary | Systemd and local logging. |

Each service is a separate systemd unit with its own restart policy so a
crash in one (audio, RGB, telemetry) cannot take down `murderbot-core` or
PiKVM — see `docs/architecture.md` failure-domain table and `AGENTS.md`
rule 4. Unit files are examples under `services/systemd/`; they are
**not** installed or enabled automatically (`AGENTS.md` rule 3).

## Design rules

- **Use Python wherever practical.** Type-hinted, formatted/linted with
  `ruff`, type-checked with `mypy`.
- **Independent services over a monolith.** Each systemd unit above is a
  separate process communicating only through the event bus
  (`events.py`) — no direct imports between `audio/`, `rgb/`,
  `telemetry/`, and PiKVM internals.
- **No global mutable state.** State lives in the state machine instance
  (`state_machine.py`) or in explicit configuration objects passed into
  constructors — not in module-level globals.
- **Configuration over hardcoding.** Runtime behavior (profiles, GPIO pin
  assignments once frozen, brightness caps, audio cooldown) is read from
  YAML config (`config.py` + `configs/examples/`), never hardcoded in
  service logic.
- **Hardware behind interfaces.** Every hardware-facing capability (GPIO
  ATX pulses, I²S playback, NeoPixel output, telemetry transport) is
  defined as a `typing.Protocol` (or ABC) in the relevant subpackage, with
  a mock implementation used by `tests/`. This is what makes `pytest`
  runnable with no Raspberry Pi attached (`AGENTS.md` rule 8), and is the
  same seam the future plugin architecture (`ROADMAP.md`) will formalize.

## State model

See `docs/architecture.md` § State model for the diagram. Implementation
lives in `state_machine.py`; transition rules are unit-tested in
`tests/test_state_machine.py`. Profiles (FR-08: separate behavior for
Windows/Linux/booting/idle/fault) are configuration-driven, selected by
the state machine's current state plus telemetry-reported host OS where
available, and default to a conservative "unknown host" profile when
telemetry is absent.

## What's implemented today vs. planned

| Component | Status |
|---|---|
| Event types, state enum, transitions | Implemented, unit-tested |
| Config parsing | Implemented (schema for `hardware.yaml`/`profiles.yaml`/`logging.yaml`) |
| GPIO/audio/RGB/telemetry interfaces + mocks | Implemented as `Protocol`s with mock backends |
| `core_service` entrypoint (config load + bus + state machine + transition logging) | Implemented, unit-tested (`tests/test_core_service.py`); performs no hardware I/O. No transport event loop yet — see the note below |
| Logging config (`logging.yaml`: `level`, `destinations`) | Implemented, unit-tested (`tests/test_logging.py`); `stdout`/`stderr` destinations only |
| Real GPIO/audio/RGB/telemetry backends | Not implemented — blocked on hardware bring-up (`ROADMAP.md` Phases 2–4) |
| REST API, web dashboard, plugin loader, OTA | Not implemented — post-1.0 (`ROADMAP.md`) |

**Note for this phase:** `hardware.yaml`'s `atx_enabled` / `audio_enabled` /
`rgb_enabled` / `telemetry_enabled` flags are parsed and validated, but no
code path consumes them yet — the core service has no hardware wiring to
gate. That is correct for Phase 0 (no backends exist), but it means the
"safe defaults" guard in `config.py` is not yet *enforced* anywhere; a
future phase must read these flags before enabling the corresponding
backend, and should be reviewed as part of that phase's ADR.

**`core_service` does not stay running yet.** `python -m
murderbot_core.core_service [config-dir]` reads `hardware.yaml`,
`profiles.yaml`, and `logging.yaml` from `config-dir` (default
`/etc/murderbot`), builds the bus and state machine, logs the starting
state, and exits 0 — nothing publishes events to the bus until a real
transport (PiKVM GPIO daemon, host-agent socket) exists in Phase 2+. A
missing or invalid `hardware.yaml`/`profiles.yaml` is a startup error; a
missing or invalid `logging.yaml` only produces a warning and the default
logging setup (INFO, stdout). `services/systemd/murderbot-core.service`
therefore remains an example unit, not one to enable on a device.

## Testing

See `docs/testing.md` for the full matrix. `pytest` in `services/` covers
only the hardware-independent pieces listed above; bench/integration/
fault-injection/thermal tests require real hardware and are tracked
separately.
