# Roadmap

MSC's mission is broad and multi-year: grow from a bench-proven PiKVM +
ATX controller into an iDRAC/iLO-style management processor with
personality, telemetry, and a plugin ecosystem. This roadmap sequences that
so each phase ships something reliable before the next is layered on top —
see `AGENTS.md` rule 9 (phased scope discipline) and
`docs/architecture.md` (failure-domain isolation) for why order matters
here: PiKVM must stay solid while everything else is still being proven.

Phase numbering matches `docs/requirements.md` and the phased BOM in the
original engineering report.

## Phase 0 — Repository & bench setup (current)

- Repository scaffold, documentation set, CI, issue/PR templates.
- Hardware-independent `murderbot_core` package: event types, state
  machine, config parsing, mock hardware/audio/RGB/telemetry interfaces.
- Inventory/acquire Pi, microSD, capture bridge; flash PiKVM image.

**Exit criteria:** CI green on `main`; state machine unit-tested; PiKVM
image flashed and reachable on the bench network.

## Phase 1 — PiKVM core proof

- Validate BIOS/POST visibility, HID emulation, virtual media, and
  reconnect behavior against the RTX 4080's video outputs.
- Extended stability + undervoltage/thermal check.

## Phase 2 — Standby power and ATX integration

- Characterize PSU 5VSB capability and Pi/capture current draw.
- Build and validate the optoisolated PWR/RESET interface (fail-open).
- Host-state sensing (main rail on/off) feeding the state machine.

## Phase 3 — Startup audio ("personality" begins)

- I²S amplifier + speaker, printed enclosure.
- Audio triggers only on a genuine host power-up event, with a cooldown.

## Phase 4 — Addressable RGB

- Level-shifted NeoPixel output, starting at ≤10 LEDs.
- Boot/idle/load/fault/shutdown lighting profiles, brightness-capped.

## Phase 5 — Integration & enclosure, v1.0

- Keyed harnesses, CAD-designed mounts, as-built wiring diagrams.
- 24-hour stability test and recovery drill.
- Tag `v1.0.0` once `docs/requirements.md` acceptance criteria are met.

## Post-1.0 — Enterprise-management feature set

These are explicitly **not** in scope until v1.0's PiKVM/ATX/audio/RGB core
is proven stable, per `AGENTS.md` rule 9. Rough, non-committal order based
on dependency (an API needs the state machine event bus; a dashboard needs
the API; OTA needs a release/versioning story already defined in
`docs/versioning-and-releases.md`):

1. **OLED status display** — small local status readout (host state,
   IP, temps); mostly a new `hardware/` service consumer of the existing
   event bus.
2. **Environmental monitoring** — case temperature/humidity sensors feeding
   `murderbot-telemetry`.
3. **Hardware telemetry expansion** — richer host-agent metrics
   (`host-agents/`), still optional and authenticated per FR-line in
   `docs/requirements.md`.
4. **REST API** — read-only first (state, telemetry, logs), then
   authenticated control endpoints (power/reset, RGB profile) reusing the
   existing event bus rather than bypassing it.
5. **Web dashboard** — thin client over the REST API; no direct
   hardware access from the dashboard process.
6. **Home Assistant integration** — via the REST API/MQTT bridge, not a
   bespoke integration that duplicates state-machine logic.
7. **Plugin architecture** — formalizes the `Protocol`-based interfaces
   already used for hardware/audio/RGB/telemetry into a documented
   extension point once at least two real plugins (RGB + telemetry) exist
   to design against.
8. **AI voice/personality** — the highest-risk, most speculative item;
   requires the plugin architecture and REST API to exist first so it can
   be sandboxed like any other plugin, not wired into the core state
   machine.
9. **OTA update capability** — deliberately last: needs a stable
   versioning/release process (`docs/versioning-and-releases.md`) and a
   proven rollback story before anything auto-updates a device with
   physical control over the host PC.

## Explicit non-goals (see `AGENTS.md`)

- Public-internet exposure of PiKVM without VPN or equivalent, at any
  phase.
- Native 4K capture/streaming of the RTX 4080's gaming output.
- A custom production PCB before Phase 5's pin allocation is proven on
  perfboard/bench wiring.
