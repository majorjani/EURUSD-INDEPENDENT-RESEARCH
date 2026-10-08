#!/usr/bin/env python3
"""Read-only quality audit of a locally downloaded HistData EURUSD ASCII tick ZIP.

No network access, no data redistribution: the output JSON contains only
hashes and aggregate statistics, which data/DATA_SOURCES.json allows publishing.
Fixes from the earlier script: weekly sessions are classified as
Friday close -> Sunday open (UTC), gaps are split into weekend vs. in-session,
and spread quantiles are exact (0.1-pip histogram over all rows).

Usage: python -I tools/audit_local_month.py PATH/TO/HISTDATA_COM_ASCII_EURUSD_T202501.zip [--out audit.json]
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

EST_NO_DST = timezone(timedelta(hours=-5))  # HistData: EST all year, no DST
STAMP_RE = re.compile(rb"^(\d{8}) (\d{9}),(\d+\.\d+),(\d+\.\d+),(\d+)\s*$")
PIP = 1e-4
WEEKEND_MIN_SECONDS = 24 * 3600


def quantiles(hist, total, qs=(0.5, 0.9, 0.95, 0.99, 0.999)):
    out, acc, keys = {}, 0, sorted(hist)
    targets = list(qs)
    for k in keys:
        acc += hist[k]
        while targets and acc >= targets[0] * total:
            out[str(targets.pop(0))] = round(k / 10, 1)
    return out


def audit(zip_path):
    blob = zip_path.read_bytes()
    report = {"file_name": zip_path.name, "size_bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest(),
              "timezone_assumption": "EST (UTC-5) without DST, converted to UTC"}
    counts, spread_hist = Counter(), Counter()
    weekend_gaps, session_gaps = [], []
    daily = Counter()
    prev_t = prev_raw = None
    first = last = None
    with zipfile.ZipFile(zip_path) as z:
        report["zip_integrity"] = z.testzip() or "PASS"
        report["archive_members"] = z.namelist()
        members = [m for m in z.namelist() if m.lower().endswith(".csv")]
        if not members:
            raise SystemExit("No CSV member in archive")
        for member in members:
            with z.open(member) as f:
                for raw in f:
                    m = STAMP_RE.match(raw)
                    if not m:
                        counts["invalid_rows"] += 1
                        continue
                    t = datetime.strptime((m[1] + m[2]).decode(), "%Y%m%d%H%M%S%f").replace(
                        tzinfo=EST_NO_DST).astimezone(timezone.utc)
                    bid, ask = float(m[3]), float(m[4])
                    if not 0 < bid <= ask:
                        counts["bid_ask_invariant_violations"] += 1
                        continue
                    counts["valid_rows"] += 1
                    daily[t.date().isoformat()] += 1
                    spread_hist[round((ask - bid) / PIP * 10)] += 1
                    if raw == prev_raw:
                        counts["adjacent_exact_duplicates"] += 1
                    if prev_t is not None:
                        d = (t - prev_t).total_seconds()
                        if d < 0:
                            counts["out_of_order"] += 1
                        elif d == 0:
                            counts["same_timestamp"] += 1
                        elif d > 60:
                            gap = {"start_utc": prev_t.isoformat(), "end_utc": t.isoformat(), "seconds": round(d, 3),
                                   "start_weekday_utc": prev_t.strftime("%a"), "end_weekday_utc": t.strftime("%a")}
                            if d >= WEEKEND_MIN_SECONDS:
                                gap["classification"] = ("weekend_fri_to_sun" if prev_t.weekday() == 4 and t.weekday() == 6
                                                         else "holiday_or_outage")
                                weekend_gaps.append(gap)
                            else:
                                counts["session_gaps_over_60s"] += 1
                                if d > 300:
                                    counts["session_gaps_over_5min"] += 1
                                session_gaps.append(gap)
                    prev_t, prev_raw = t, raw
                    first = first or t
                    last = t
    total = counts["valid_rows"]
    session_gaps.sort(key=lambda g: -g["seconds"])
    report.update(
        first_utc=first.isoformat() if first else None,
        last_utc=last.isoformat() if last else None,
        row_counts=dict(counts),
        spread_pips_min=round(min(spread_hist) / 10, 1) if spread_hist else None,
        spread_pips_max=round(max(spread_hist) / 10, 1) if spread_hist else None,
        spread_pips_quantiles=quantiles(spread_hist, total) if total else {},
        spread_over_3pips=sum(v for k, v in spread_hist.items() if k > 30),
        spread_over_10pips=sum(v for k, v in spread_hist.items() if k > 100),
        weekly_closures=weekend_gaps,
        longest_session_gaps=session_gaps[:20],
        daily_utc_rows=dict(sorted(daily.items())),
        limitations=["Non-adjacent duplicates are not detected.",
                     "Rows are quote updates at millisecond precision, not independent trades.",
                     "Liquidity-provider composition of the HistData feed is unknown."],
    )
    flagged = counts["invalid_rows"] or counts["out_of_order"] or counts["bid_ask_invariant_violations"] \
        or report["zip_integrity"] != "PASS"
    report["status"] = "AUDIT_COMPLETED_WITH_FLAGS" if flagged else "AUDIT_COMPLETED"
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("zip", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    report = audit(args.zip)
    text = json.dumps(report, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"{report['status']}: {report['row_counts'].get('valid_rows', 0):,} rows -> {args.out}")
    else:
        print(text)
    return 0 if report["status"] == "AUDIT_COMPLETED" else 2


if __name__ == "__main__":
    sys.exit(main())
