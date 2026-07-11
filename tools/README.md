# tools/

One-off engineering tools, distinct from `../scripts/` (repo/dev
environment automation) and `../services/` (runtime services).

- `bom_report.py` — stdlib-only script that summarizes
  `../hardware/bom.csv` target-cost totals by phase and counts rows by
  status. Run with `python3 tools/bom_report.py` from the repo root (or
  pass an explicit path). Its total may not exactly match the phased
  cumulative-cost table in the original engineering report/`ROADMAP.md`
  — it's an independent line-item sum for sanity-checking the BOM as it
  evolves, not a source of truth for the budget narrative.
