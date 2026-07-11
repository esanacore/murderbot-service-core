# Wiring

**Status: connector inventory only — no pin numbers are asserted here.**
Per `AGENTS.md` rule 1 and the original engineering report's repository
rule ("never assume a connector pinout from wire color alone; cite the PSU,
motherboard, or board reference and verify with a meter"), every pinout
below is `TBD` until it is confirmed against a manufacturer reference and a
meter, and the confirming source is cited inline.

## Connector inventory

| Connector | Purpose | Pin count | Pinout source | Status |
|---|---|---|---|---|
| ATX front-panel header (motherboard) | PWR SW / RESET SW / power LED / HDD LED | `TBD` | MSI Z490-A PRO manual (front panel header section) | Not yet verified against board silkscreen + meter |
| ATX 24-pin main power | 5VSB identification | 24 | MSI Z490-A PRO manual / ATX spec | 5VSB pin location known from ATX spec convention; PSU-specific rating still `TBD` (see `docs/power-design.md`) |
| Raspberry Pi 40-pin GPIO | ATX opto outputs, NeoPixel data, I²S, sensing | 40 | Raspberry Pi 4 datasheet | Pin *assignment* (which of the 40 pins is used for what) is a project decision, not yet made — track in `docs/decisions/` when frozen |
| HDMI-to-CSI bridge | Video capture from RTX 4080 | per bridge datasheet | Bridge manufacturer datasheet (bridge model not yet selected — see `hardware/bom.csv`) | Blocked on bridge selection |
| I²S amplifier breakout (MAX98357A-class) | Audio out | per breakout datasheet | Adafruit MAX98357A product page | Not yet wired |
| NeoPixel strip connector | RGB data/power/ground | 3 (5V, GND, DIN) | WS2812B datasheet | Not yet wired |

## Rules for this document

1. Do not fill in a pin number without a citation next to it (datasheet
   page/section, manual page, or "measured with meter, see photo in
   `docs/images/`").
2. Front-panel and ATX headers are especially failure-prone to guess —
   wire color conventions vary by motherboard vendor and are not a
   substitute for the manual.
3. Any connector that will carry the isolated PWR/RESET signals must be
   keyed or clearly labeled (FR-09) before it's considered done — a
   generic unkeyed header is a bench-only state, not a final one.
4. When a pinout is confirmed, move its row from "Not yet verified" to a
   dated, cited value, and cross-reference the ADR or backlog item that
   closed it.

## As-built diagram

Not yet created — v1.0 acceptance criterion #9 (`docs/requirements.md`)
requires this document to match the as-built system before release. It
will be added here (or linked from `docs/images/`) once Phase 5
(`ROADMAP.md`) converts bench wiring into keyed harnesses.

## See also

- `docs/power-design.md` — current/fusing budgets for the branches these
  connectors carry.
- `hardware/harnesses/` — physical harness build notes once bench wiring
  is finalized.
- `docs/decisions/` — any ADR that fixes a pin assignment.
