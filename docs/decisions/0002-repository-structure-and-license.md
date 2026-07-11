# ADR 0002: Repository structure and licensing approach

Status: Accepted

## Context

Two documents proposed slightly different repository layouts:

- The original engineering report (§11) proposed a layout centered on
  `software/src/murderbot_core/` with `hardware/{schematics,pcb,cad,harnesses}`
  as one combined directory, sized for a Phase 0–5 hobby build.
- The later `agent_instructions.md` bootstrap prompt asked for a broader,
  "professional embedded systems project" layout with `firmware/`,
  `services/`, `hardware/`, `cad/`, `electronics/`, `docs/`, `scripts/`,
  `tests/`, `assets/`, `configs/`, `examples/`, `tools/`, and `.github/`
  kept separate, sized for the multi-year iDRAC/iLO-style vision in
  `ROADMAP.md`.

These need to be reconciled into one actual directory tree, and the
project also needs a license decision that the original report didn't
address (`agent_instructions.md` asked for a "License" file but not a
specific choice).

## Decision

Adopt the broader `agent_instructions.md` top-level structure, since it
scales better to the multi-year roadmap, and map the report's more
detailed content into it as follows:

- `services/` — the report's `software/src/murderbot_core/` content
  (Python package, systemd unit examples under `services/systemd/`).
- `hardware/` — bill of materials (`bom.csv`), harness notes, datasheet
  references. Data and physical-build notes, not design files.
- `electronics/` — schematics and PCB design (KiCad), split out from the
  report's combined `hardware/schematics|pcb`. Currently placeholder —
  see `AGENTS.md` non-goals (no production PCB before bench proof).
- `cad/` — 3D-printable brackets/enclosures, split out similarly.
  Currently placeholder.
- `firmware/` — reserved, currently unused. MSC runs entirely as Linux
  services on the Pi in Phase 0–5; this directory exists for a possible
  future microcontroller (e.g. a dedicated OLED/sensor co-processor,
  `ROADMAP.md` post-1.0 item 1–2) rather than being deleted and
  potentially re-argued-over later.
- `host-agents/` — kept from the report as a top-level directory (not
  explicitly named in `agent_instructions.md`, but a real, approved
  subsystem — see `docs/architecture.md` "Host agent" row).

**License:** MIT for all software and documentation in this repository
(`LICENSE`). Media assets are explicitly excluded (`assets/README.md`) —
MIT is inappropriate for third-party or user-supplied audio. Once
`electronics/` and `cad/` contain original design files (not just
placeholders/references), those directories will additionally be
licensed under CERN-OHL-S v2 (a copyleft-ish hardware license that keeps
manufacturability requirements attached to derivatives), tracked as a
follow-up to this ADR rather than decided speculatively now — see
`docs/backlog.md` if this hasn't happened yet by the time `electronics/`
gets its first real schematic.

## Alternatives considered

- **Keep the report's flatter `hardware/` structure:** Simpler today, but
  would need restructuring later once electronics/CAD content actually
  exists and needs different licensing/tooling (KiCad vs. STL/STEP
  files) — better to pay that cost once, now, while the repo is empty.
- **Apache-2.0 for software:** Considered for the explicit patent grant;
  not chosen because this is a hobbyist project with no patent portfolio
  concerns, and MIT is simpler for casual contributors to reason about.
- **GPL-3.0 for software:** Considered to prevent proprietary forks;
  not chosen — there's no commercial-fork threat model here, and GPL's
  copyleft would complicate reusing MSC's `Protocol`-based hardware
  interfaces (`docs/software.md`) in unrelated personal projects, which
  is a plausible and desirable outcome for this kind of hobby code.

## Consequences

- Contributors need to know the split between `hardware/` (data/BOM),
  `electronics/` (schematics/PCB), and `cad/` (enclosures/brackets) isn't
  the same as the original report's single `hardware/` directory — this
  ADR is the canonical explanation if that's ever confusing.
- A second, hardware-specific license (CERN-OHL-S v2) will need to be
  added to `electronics/` and `cad/` once they have real content; this is
  tracked, not forgotten, but is explicitly not decided today per
  `AGENTS.md` rule 1's spirit (don't assert things ahead of when they're
  actually needed/known).
