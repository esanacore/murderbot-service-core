# hardware/

Bill of materials and physical-build reference data — not design files
(those live in `../electronics/` and `../cad/`, see ADR 0002).

- `bom.csv` — the authoritative parts list. Columns: `category, item,
  manufacturer, part_number, quantity, target_price, actual_price,
  source, status, already_owned, phase, notes`. Update this file, not
  just the narrative in `../docs/`, whenever a part is selected,
  purchased, or substituted (`AGENTS.md` rule 6).
- `harnesses/` — physical harness build notes (connector-to-connector
  wiring as actually built, photos, keying scheme) once bench wiring
  moves to keyed harnesses (`ROADMAP.md` Phase 5).
- `datasheets/` — local copies or links for parts where the manufacturer
  page might disappear; prefer linking in `docs/` first and only mirror
  a datasheet here if it's small and clearly licensed for redistribution.

## Budget control rule

Per the original engineering report: the BOM must track target price,
actual price, source, purchase date/status, and "already owned" —
shipping and tax should be tracked rather than silently excluded once
real purchases start. Do not purchase the RGB or audio phase parts until
the KVM power and capture paths are stable (`ROADMAP.md` Phase 1-2 before
Phase 3-4).
