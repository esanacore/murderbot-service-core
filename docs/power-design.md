# Power Design

**Status: parameterized, pending measurement.** Per `AGENTS.md` rule 1, no
value below is asserted as final until it has a citation (datasheet/manual)
or a measurement (instrument + method) recorded next to it. Anything marked
`TBD` blocks Phase 2 (`ROADMAP.md`) and has a matching row in
`docs/backlog.md`.

## Two branches, two guarantees

| Branch | Powered when | Loads | Design notes |
|---|---|---|---|
| Standby | PSU connected and rear switch on | Pi 4, capture bridge, network, ATX logic | Protected, fused, sized from measured load and PSU 5VSB rating. |
| Host-on | Motherboard commands PSU on | NeoPixels, amplifier, display, decorative devices | Separate fuse; sensed by Pi; no backfeeding into standby branch. |

Rationale for the split: see `docs/architecture.md` § Power topology and
ADR 0001.

## Standby branch budget

The Raspberry Pi 4 requires a stable 5 V supply with adequate current
margin. Per the Raspberry Pi 4 Model B datasheet (see
`docs/pikvm-setup.md` / `docs/decisions/` reference list), Raspberry Pi
documentation calls for a 5 V, 3 A supply under general use, with 2.5 A
potentially acceptable when downstream USB loads remain low.

| Quantity | Value | Source |
|---|---|---|
| Pi 4 recommended supply | 5V, 3A (2.5A acceptable, low USB load) | Raspberry Pi 4 datasheet |
| PSU 5VSB rated current | `TBD` | Read from the exact PSU's label/manual — do not assume from wattage class |
| Measured idle draw (Pi + capture bridge, PiKVM running) | `TBD` | Bench measurement, Phase 1 |
| Measured peak draw (capture active + network + USB HID) | `TBD` | Bench measurement, Phase 1 |
| Standby-branch fuse rating | `TBD` — derive from measured peak + margin, not guessed | Phase 2 |

**Rule:** the 5VSB rail must be checked against the exact PSU's
documented rating and all standby loads *before* it is used. A fused
DC-DC or protected distribution stage is used instead of wiring the Pi
directly to an unknown standby connector (FR-07 relatedly bans powering
high-current accessories from Pi GPIO pins — this is the standby-side
analogue: don't power the Pi from an unqualified rail either).

## Host-on branch budget

| Quantity | Value | Source |
|---|---|---|
| I²S amplifier (MAX98357A-class) peak output | ~3 W class | Adafruit MAX98357A product page (see `docs/decisions/`/reference list) |
| NeoPixel strip current (per LED, full white) | ~60 mA/LED (WS2812B datasheet nominal) | Datasheet; actual draw is capped in software — see brightness cap below |
| Initial strip length | ≤10 LEDs (Phase 4 bring-up), ≤30 LEDs (initial installed target) | `ROADMAP.md` Phase 4, engineering report BOM |
| Host-on branch fuse rating | `TBD` — derive from (amplifier peak) + (LED count × per-LED draw × brightness cap), not guessed | Phase 4 |

**Brightness cap:** RGB firmware/software enforces a conservative
software brightness ceiling (see `services/src/murderbot_core/rgb/`) so
the *installed* current draw stays well under the strip's theoretical
maximum. The cap value itself is `TBD` pending Phase 4 current
measurements at several brightness settings (`docs/testing.md`).

## What must never happen (FR-07 and general safety)

- The Pi's own GPIO 3.3V/5V pins must not power NeoPixels, the amplifier,
  or any other accessory directly — those pins are not current-rated for
  it and doing so risks browning out the Pi itself (taking PiKVM down
  with it, violating the failure-domain rule in `docs/architecture.md`).
- No connection from the host-on branch back into the standby branch
  (no backfeeding) — this would defeat the entire point of the split.
- No wiring change is made "live" — power is disconnected before any
  branch is modified, and the change is documented (`docs/wiring.md`)
  before re-energizing (`docs/decisions/` repository rule, from the
  original engineering report §11.1).

## Open items (see `docs/backlog.md` for tracked, prioritized versions)

- [ ] Identify exact PSU model and read documented 5VSB rating (P0).
- [ ] Measure Pi + capture bridge idle/peak current (P1).
- [ ] Derive and implement standby-branch fuse rating from measurement.
- [ ] Measure NeoPixel current at candidate brightness caps (P2).
- [ ] Derive and implement host-on branch fuse rating from measurement.
