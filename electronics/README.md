# electronics/

Schematics and PCB design (KiCad). **Currently placeholder** — per
`AGENTS.md` non-goals, no custom production PCB is designed before the
bench prototype and pin allocation are proven (`ROADMAP.md` Phase 5).

- `schematics/` — KiCad schematic project, once bench wiring is stable
  enough to formalize. Will capture the ATX optoisolation circuit, the
  level-shifter/NeoPixel data path, and the I²S amplifier wiring — the
  three circuits currently described only narratively in
  `../docs/wiring.md` and `../docs/power-design.md`.
- `pcb/` — carrier PCB layout, blocked on schematic freeze (see
  `../docs/backlog.md` P3 item "Design integrated carrier PCB after
  pinout freeze").

## Licensing note

Once this directory contains original design files, they will be
licensed under CERN-OHL-S v2 in addition to this repository's MIT
license for software — see
`../docs/decisions/0002-repository-structure-and-license.md`.
