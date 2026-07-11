# Murderbot Service Core (MSC)

An embedded, Raspberry Pi–based service processor that lives inside a desktop
PC ("Murderbot": MSI Z490-A PRO / Intel Core i7-10700 / RTX 4080) and provides
enterprise-style out-of-band management — in the spirit of Dell iDRAC, HP
iLO, or Lenovo XClarity — plus custom "personality" features: startup audio,
addressable RGB, and (eventually) host telemetry, a plugin architecture, and
a web dashboard.

> **Status: pre-hardware, documentation and software-scaffolding phase.**
> No board has been wired into the host PC yet. Nothing in this repository
> should be treated as a validated schematic, pinout, or power budget until
> the corresponding `TBD` markers in `docs/` are resolved and the relevant
> ADR / test evidence is linked. See [`docs/decisions/`](docs/decisions/).

## Safety warning

This project connects a Raspberry Pi to a live desktop PC's ATX power
supply, front-panel switches, and (later) low-voltage accessory power. Done
wrong, this can damage a motherboard, a PSU, or the Pi, or create a fire or
shock hazard. Read [`docs/power-design.md`](docs/power-design.md) and
[`docs/wiring.md`](docs/wiring.md) before energizing anything, and do not
skip the bench-proof phase described below. PiKVM (remote BIOS-level
control) is the one subsystem that must always remain reliable and
isolated from failures in every other subsystem — see
[`docs/architecture.md`](docs/architecture.md) for the failure-domain rules
this repository enforces.

## What this is (and isn't) today

MSC's long-term mission is broad — see [`ROADMAP.md`](ROADMAP.md) — but
Phase 1 is deliberately narrow:

- Raspberry Pi platform selection and bench bring-up
- PiKVM integration (BIOS-level remote video/keyboard/mouse)
- Remote power/reset via an isolated ATX interface
- A hardware-independent internal service architecture (state machine,
  event bus, config-driven profiles)
- Startup audio playback
- Boot/host-state detection
- Documentation and a CI-backed testing framework

RGB animations, an OLED status display, environmental monitoring, Home
Assistant integration, an AI voice/personality layer, a plugin architecture,
a REST API, a web dashboard, and OTA updates are explicitly **future
phases** (see `ROADMAP.md`) and are not implemented here yet. Section 12 of
the original engineering report and [`AGENTS.md`](AGENTS.md) both prohibit
inventing hardware facts or wiring anything live ahead of that plan — this
README makes the same promise to human contributors.

## Repository layout

```
murderbot-service-core/
├── docs/            Architecture, requirements, power/wiring design, ADRs, testing, security
├── services/         Python source (murderbot_core) — state machine, event bus, service interfaces
├── tests/            Hardware-independent unit tests for services/
├── hardware/         Bill of materials, harness notes, datasheets
├── electronics/       Schematics and PCB design (KiCad), currently placeholders
├── cad/              3D-printable brackets/enclosures, currently placeholders
├── firmware/         Reserved for any future microcontroller firmware (not currently used — MSC runs on Pi/Linux)
├── configs/examples/ Example (non-secret) YAML configuration
├── scripts/          Repo/dev automation (env setup, linting helpers)
├── tools/            One-off engineering tools (e.g. BOM cost rollups)
├── examples/         Usage examples once services/ is runnable end-to-end
├── host-agents/      Optional Windows/Linux telemetry agents (future)
├── assets/           Media (audio clips, images) — see assets/README.md before adding anything
└── .github/          CI, issue/PR/discussion templates
```

## Engineering philosophy

Reliability > Maintainability > Simplicity > Expandability > Performance >
Cost. Every subsystem is modular, independently testable, and expected to
survive several years of incremental extension. See
[`AGENTS.md`](AGENTS.md) for the working rules this applies to both human
and AI contributors, and [`docs/architecture.md`](docs/architecture.md) for
how failure domains are kept separate (a crashed RGB service must never be
able to take PiKVM or ATX control down with it).

## Getting started

There is no hardware bring-up procedure yet — start with the
hardware-independent software:

```bash
cd services
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

See [`docs/testing.md`](docs/testing.md) for the full test matrix
(including the bench/integration/fault-injection tests that require real
hardware and are not part of `pytest` today).

## Where to go next

| I want to... | Read |
|---|---|
| Understand the overall system design | [`docs/architecture.md`](docs/architecture.md) |
| See what "done" means for v1.0 | [`docs/requirements.md`](docs/requirements.md) |
| Understand power budget / ATX wiring | [`docs/power-design.md`](docs/power-design.md), [`docs/wiring.md`](docs/wiring.md) |
| Set up PiKVM | [`docs/pikvm-setup.md`](docs/pikvm-setup.md) |
| Understand the software services | [`docs/software.md`](docs/software.md) |
| See the current backlog / priorities | [`docs/backlog.md`](docs/backlog.md) |
| See the longer-term roadmap | [`ROADMAP.md`](ROADMAP.md) |
| Contribute | [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) |
| Report a security issue | [`SECURITY.md`](SECURITY.md) |
| Get help | [`SUPPORT.md`](SUPPORT.md) |

## License

MIT — see [`LICENSE`](LICENSE). Audio and other media assets are **not**
covered by this license; see [`assets/README.md`](assets/README.md).
