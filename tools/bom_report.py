#!/usr/bin/env python3
"""Summarize hardware/bom.csv: target-cost totals by phase and status.

Standalone stdlib-only script (deliberately not part of the
murderbot_core package - this is a one-off engineering tool, not a
runtime service, per tools/README.md).

Usage:
    python3 tools/bom_report.py [path/to/bom.csv]
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_BOM_PATH = Path(__file__).resolve().parent.parent / "hardware" / "bom.csv"


def _parse_price_range(raw: str) -> tuple[float, float] | None:
    """Parse a target_price cell like '$35-70 used/new' into (35.0, 70.0).

    Returns None for cells that don't contain a parseable numeric range
    (e.g. blank actual_price cells) rather than raising, since this is a
    reporting tool over a hand-maintained CSV that may have gaps.
    """
    numbers = re.findall(r"\d+(?:\.\d+)?", raw)
    if not numbers:
        return None
    values = [float(n) for n in numbers]
    return (min(values), max(values))


def summarize(bom_path: Path) -> None:
    if not bom_path.exists():
        print(f"BOM file not found: {bom_path}", file=sys.stderr)
        sys.exit(1)

    by_phase_low: dict[str, float] = defaultdict(float)
    by_phase_high: dict[str, float] = defaultdict(float)
    by_status: dict[str, int] = defaultdict(int)
    total_low = total_high = 0.0

    with bom_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            phase = row.get("phase", "unknown") or "unknown"
            status = row.get("status", "unknown") or "unknown"
            qty_raw = row.get("quantity", "1") or "1"
            qty_match = re.match(r"\d+", qty_raw)
            qty = int(qty_match.group()) if qty_match else 1

            by_status[status] += 1

            price_range = _parse_price_range(row.get("target_price", ""))
            if price_range is None:
                continue
            low, high = price_range
            by_phase_low[phase] += low * qty
            by_phase_high[phase] += high * qty
            total_low += low * qty
            total_high += high * qty

    print("BOM target-cost summary (approximate - see hardware/bom.csv for exact rows)\n")
    print(f"{'Phase':<12}{'Low':>10}{'High':>10}")
    for phase in sorted(by_phase_low, key=lambda p: (len(p), p)):
        print(f"{phase:<12}${by_phase_low[phase]:>8.2f} ${by_phase_high[phase]:>8.2f}")
    print(f"\n{'TOTAL':<12}${total_low:>8.2f} ${total_high:>8.2f}")

    print("\nStatus counts:")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BOM_PATH
    summarize(path)
