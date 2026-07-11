# Testing

Testing splits into what CI can run today (hardware-independent) and what
requires the physical bench setup (tracked here as a matrix, run manually
and recorded, until/unless a hardware-in-the-loop CI runner exists).

## CI-covered (runs on every PR)

| Check | Tool | Scope |
|---|---|---|
| Lint | `ruff` | `services/` |
| Format check | `ruff format --check` | `services/` |
| Type check | `mypy` | `services/src` |
| Unit tests | `pytest` | `services/tests` (state machine, events, config parsing, mock hardware/audio/RGB/telemetry) |
| Markdown/link check | `.github/workflows/ci.yml` (`docs-link-check` job) | `docs/`, root `*.md` |

Satisfies FR-10 and v1.0 acceptance criterion coverage for anything
software-only.

## Bench / integration matrix (manual, hardware required)

| Phase | Test | Pass criteria | Evidence to record |
|---|---|---|---|
| 1 | POST/BIOS visibility across RTX 4080 outputs + local-display combinations | BIOS visible remotely for the chosen output combination | Photo/recording, output combination used |
| 1 | Keyboard/mouse emulation, virtual media, reboot recovery, network reconnect | All functions work; PiKVM reconnects after host reboot without manual intervention | Test log |
| 1 | Extended stability test | No PiKVM crash/undervoltage/thermal warning over test duration (duration `TBD`) | `vcgencmd get_throttled` output, uptime log |
| 2 | Current draw at idle, capture load, peak startup | Values recorded, feed `docs/power-design.md` | Instrument + method noted |
| 2 | Momentary pulse timing and physical-button pass-through | Remote and local buttons both work; timing matches motherboard spec | Scope capture or timed test log |
| 2 | Failure cases: Pi reboot, GPIO daemon crash, disconnected optocoupler, host lockup | ATX output fails open in every case (FR-03, `AGENTS.md` rule 5) | Test log per failure case |
| 3 | I²S output on bench power | Audio plays cleanly at target volume | Recording or listening test log |
| 3 | Trigger discipline | Plays once per genuine host power-up; cooldown prevents repeat-trigger loop after service restart | Test log |
| 4 | Level-shifted data at first pixel | Logic levels correct per `docs/wiring.md` FR-06 | Scope capture |
| 4 | Current at several brightness settings | Feed brightness cap decision in `docs/power-design.md` | Meter readings |
| 4 | GPU load interference check | No thermal/electrical side effects on RGB/audio during GPU load | Test log |
| 5 | 24-hour stability test | No undervoltage/thermal warning; state machine remains coherent | Log excerpt |
| 5 | Recovery drill | Full config recreated from fresh PiKVM image using only documented steps | Recovery log, timing |

## Fault-injection tests (subset of the above, called out explicitly)

Per FR-05 and the failure-domain rules in `docs/architecture.md`, each of
these must be tested independently, not just implied by the others:

- Kill `murderbot-audio.service` mid-playback → PiKVM session unaffected.
- Kill `murderbot-rgb.service` mid-animation → PiKVM session unaffected,
  LEDs default off.
- Kill `murderbot-core.service` → ATX interface fails open (no stuck
  pulse), PiKVM unaffected.
- Disconnect the ATX optocoupler board → system reports `FAULT` or
  degraded state, does not silently pretend control still works.

## Undervoltage / thermal

Checked via `vcgencmd get_throttled` (or PiKVM's own reporting where
available) at the end of every bench/integration test above, not just the
dedicated stability tests — a transient undervoltage event during a
different test is still a finding.

## Recording results

Bench/integration results are not currently automated into this repo.
Until a structured format is adopted, record results as dated entries
under `docs/images/` (photos/scope captures) referenced from the relevant
`docs/*.md` "Status" table row (e.g. `docs/power-design.md`,
`docs/wiring.md`), and close the corresponding `docs/backlog.md` item.
