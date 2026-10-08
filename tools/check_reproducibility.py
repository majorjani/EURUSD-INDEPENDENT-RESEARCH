#!/usr/bin/env python3
"""Check a submission folder for the files and metadata needed to reproduce it.

Usage:
  python tools/check_reproducibility.py submissions/<study_id>
  python tools/check_reproducibility.py submissions/<study_id> --update-hashes
Exit code 0 = pass, 1 = fail.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = ["README.md", "manifest.json", "preregistration.md", "trades.csv", "trials.csv", "metrics.json"]
REQUIRED_KEYS = ["study_id", "author", "label", "horizon", "data_inputs", "periods", "cost_model",
                 "n_trials", "files", "environment", "reproduce_command"]
LABELS = {"EXPLORATORY", "PRE_REGISTERED", "VALIDATED_OOS", "REPLICATED", "REJECTED"}
HORIZONS = {"swing", "intraday", "scalping"}
TRADE_COLS = ["trade_id", "signal_time_utc", "entry_time_utc", "exit_time_utc", "side",
              "entry_px", "exit_px", "pnl_pips", "cost_pips", "period_role"]
TRIAL_COLS = ["trial_id", "timestamp", "hypothesis_id", "params_json", "period", "n_trades", "metric"]
METRIC_KEYS = ["n_trades", "net_exp_pips", "profit_factor", "hit_rate", "sharpe_daily_ann", "dsr", "max_dd_pips"]
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
HASHED_SUFFIXES = {".py", ".r", ".mq5", ".mqh", ".cs", ".ipynb", ".csv", ".json", ".md", ".txt", ".yml", ".yaml", ".toml"}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_header(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return next(csv.reader(f), []), sum(1 for _ in f)


def update_hashes(folder, manifest_path, manifest):
    files = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.name != "manifest.json" and p.suffix.lower() in HASHED_SUFFIXES:
            files.append({"path": p.relative_to(folder).as_posix(), "sha256": sha256(p)})
    manifest["files"] = files
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {len(files)} file hash(es) in {manifest_path}")


def check(folder, update):
    errors, warnings = [], []
    for name in REQUIRED_FILES:
        if not (folder / name).is_file():
            errors.append(f"missing {name}")
    mpath = folder / "manifest.json"
    manifest = {}
    if mpath.is_file():
        try:
            manifest = json.loads(mpath.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            errors.append(f"manifest.json invalid JSON: {exc}")
    if manifest and update:
        update_hashes(folder, mpath, manifest)
    if manifest:
        for k in REQUIRED_KEYS:
            if k not in manifest:
                errors.append(f"manifest missing '{k}'")
        if manifest.get("study_id") and manifest["study_id"] != folder.name and folder.name != "_example":
            errors.append(f"study_id '{manifest['study_id']}' does not match folder '{folder.name}'")
        if manifest.get("label") not in LABELS:
            errors.append(f"label must be one of {sorted(LABELS)}")
        if manifest.get("horizon") not in HORIZONS:
            errors.append(f"horizon must be one of {sorted(HORIZONS)}")
        if not isinstance(manifest.get("n_trials"), int) or manifest.get("n_trials", 0) < 1:
            errors.append("n_trials must be a positive integer")
        for inp in manifest.get("data_inputs", []):
            if not SHA_RE.match(str(inp.get("sha256", ""))):
                errors.append(f"data input {inp.get('file_name')}: missing/invalid sha256")
        cm = manifest.get("cost_model", {})
        if cm and not cm.get("bid_ask"):
            warnings.append("cost_model.bid_ask is false - result will be flagged COST_MODEL_WEAK")
        if cm and len(cm.get("slippage_pips_per_side", [])) < 2:
            warnings.append("fewer than two slippage scenarios (protocol requires >= 2)")
        for entry in manifest.get("files", []):
            p = folder / entry.get("path", "")
            if not p.is_file():
                errors.append(f"manifest file not found: {entry.get('path')}")
            elif sha256(p) != entry.get("sha256"):
                errors.append(f"hash mismatch: {entry.get('path')} (run with --update-hashes if intended)")
        if manifest.get("label") in {"VALIDATED_OOS", "REPLICATED"} and not manifest.get("periods", {}).get("holdout"):
            errors.append("VALIDATED_OOS/REPLICATED requires a holdout period")
    tp = folder / "trades.csv"
    if tp.is_file():
        header, n = read_header(tp)
        missing = [c for c in TRADE_COLS if c not in header]
        if missing:
            errors.append(f"trades.csv missing columns {missing}")
        else:
            with tp.open(newline="", encoding="utf-8-sig") as f:
                bad = [r["trade_id"] for r in csv.DictReader(f) if r["signal_time_utc"] >= r["entry_time_utc"]]
            if bad:
                errors.append(f"causality: {len(bad)} trade(s) with signal_time_utc >= entry_time_utc (e.g. {bad[:5]})")
        extra = [c for c in header if c.lower() in {"open", "high", "low", "close", "bid", "ask"}]
        if extra:
            errors.append(f"trades.csv contains price-series columns {extra} (not allowed)")
    trp = folder / "trials.csv"
    if trp.is_file():
        header, n = read_header(trp)
        missing = [c for c in TRIAL_COLS if c not in header]
        if missing:
            errors.append(f"trials.csv missing columns {missing}")
        if manifest.get("n_trials") and n < manifest["n_trials"]:
            errors.append(f"trials.csv has {n} rows but manifest.n_trials = {manifest['n_trials']}")
    mp = folder / "metrics.json"
    if mp.is_file():
        try:
            metrics = json.loads(mp.read_text(encoding="utf-8-sig"))
            rows = metrics if isinstance(metrics, list) else [metrics]
            for r in rows:
                miss = [k for k in METRIC_KEYS if k not in r]
                if miss:
                    errors.append(f"metrics.json entry missing {miss}")
                    break
        except json.JSONDecodeError as exc:
            errors.append(f"metrics.json invalid JSON: {exc}")
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder", type=Path)
    ap.add_argument("--update-hashes", action="store_true")
    args = ap.parse_args(argv)
    folder = args.folder.resolve()
    if not folder.is_dir():
        print(f"REPRODUCIBILITY CHECK: FAIL - {folder} is not a directory")
        return 1
    errors, warnings = check(folder, args.update_hashes)
    for w in warnings:
        print("  warning:", w)
    if errors:
        print(f"REPRODUCIBILITY CHECK: FAIL ({len(errors)} issue(s)) - {folder.name}")
        for e in errors:
            print("  -", e)
        return 1
    print(f"REPRODUCIBILITY CHECK: PASS - {folder.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
