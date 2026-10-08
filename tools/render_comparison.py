#!/usr/bin/env python3
"""Render comparison/comparison_table.csv to comparison/COMPARISON_TABLE.md."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "comparison" / "comparison_table.csv"
DST = ROOT / "comparison" / "COMPARISON_TABLE.md"
SHOWN = ["study_id", "horizon", "timeframe", "period_role", "slippage_pips", "n_trials", "n_trades",
         "net_exp_pips", "profit_factor", "sharpe_daily_ann", "dsr", "max_dd_pips", "label", "audit_verdict", "notes"]


def main():
    with SRC.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = ["# Comparison Table", "",
           "Generated from `comparison_table.csv` by `tools/render_comparison.py`. Do not edit by hand.",
           "Column definitions: [COLUMNS.md](COLUMNS.md). Empty metric = withheld or not yet computed.", "",
           "| " + " | ".join(SHOWN) + " |", "|" + "---|" * len(SHOWN)]
    for r in rows:
        out.append("| " + " | ".join((r.get(c) or "").replace("|", "/") for c in SHOWN) + " |")
    out.append("")
    DST.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {DST} ({len(rows)} row(s))")


if __name__ == "__main__":
    main()
