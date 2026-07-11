# murderbot-core

Hardware-independent core services for the Murderbot Service Core. See
[`../docs/software.md`](../docs/software.md) for the architecture and
[`../docs/architecture.md`](../docs/architecture.md) for how this fits the
overall system.

## Install (dev)

```bash
cd services
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Run tests

```bash
pytest                 # from services/, runs ../tests
ruff check .
ruff format --check .
mypy src
```

## Package layout

```
src/murderbot_core/
├── events.py        # Event dataclasses/enum + in-process event bus
├── state_machine.py # STANDBY/HOST_STARTING/HOST_RUNNING/HOST_SHUTTING_DOWN/FAULT
├── config.py         # YAML config loading/validation
├── logging_setup.py  # Shared structured logging setup
├── hardware/          # ATX/GPIO Protocol + MockAtxInterface
├── audio/             # Audio-service Protocol + MockAudioPlayer
├── rgb/                # RGB-service Protocol + MockRgbController
└── telemetry/          # Telemetry Protocol + MockTelemetrySource
```

Only the state machine, events, and config layers have real logic today.
The `hardware/`, `audio/`, `rgb/`, and `telemetry/` packages currently
contain interface definitions and mock/no-op implementations only — real
backends land in later roadmap phases once hardware exists to test
against (`AGENTS.md` rule 8).
