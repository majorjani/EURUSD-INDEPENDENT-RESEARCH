#!/usr/bin/env python3
"""Fail if a path contains market data that this project may not redistribute.

Scans file names, archive members and file contents for HistData artefacts,
tick rows, OHLC rows and oversized tabular files. Stdlib only.

Usage: python tools/check_data_license.py [PATH ...]   (default: repo root)
Exit code 0 = clean, 1 = violations found.
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "DATA_SOURCES.json"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
NAME_PATTERNS = [
    (re.compile(r"^HISTDATA_COM_", re.I), "HistData download archive"),
    (re.compile(r"^DAT_(ASCII|MT|NT|XLSX)_", re.I), "HistData data file"),
    (re.compile(r"\.(bi5|hst|fxt|parquet|feather|h5|hdf5)$", re.I), "binary market-data format"),
]
ARCHIVE_EXT = {".zip", ".7z", ".gz", ".rar", ".tar"}
TEXT_EXT = {".csv", ".txt", ".tsv", ".json", ".md", ".dat", ""}

# HistData tick format: YYYYMMDD HHMMSSfff,bid,ask,volume (e.g. 20000101 000000000,1.000000,1.000100,0 - synthetic)
TICK_RE = re.compile(r"^\d{8}[ T]?\d{6,9}[,;]\s*\d+\.\d+[,;]\s*\d+\.\d+")
# Generic OHLC: timestamp followed by >=4 prices
OHLC_RE = re.compile(r"^[\d.\-/: T]{8,26}[,;\t]\s*\d+\.\d{3,}([,;\t]\s*\d+\.\d{3,}){3}")
PRICE_ROWS_LIMIT = 50          # rows matching price patterns tolerated in one file
LARGE_TABLE_BYTES = 5_000_000  # CSV/TXT above this is flagged for manual review
# Files in which price-like rows are expected and acceptable (trade fills only)
ALLOWED_PRICE_FILES = {"trades.csv"}


def load_registry():
    try:
        return {s["source_id"]: s for s in json.loads(REGISTRY.read_text(encoding="utf-8"))["sources"]}
    except Exception as exc:
        print(f"WARNING: cannot read registry {REGISTRY}: {exc}")
        return {}


def scan_text(path):
    hits = {"tick": 0, "ohlc": 0}
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i > 200_000:
                    break
                if TICK_RE.match(line):
                    hits["tick"] += 1
                elif OHLC_RE.match(line):
                    hits["ohlc"] += 1
    except OSError:
        pass
    return hits


def check_file(path, problems):
    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    for rx, why in NAME_PATTERNS:
        if rx.search(path.name):
            problems.append(f"{rel}: {why}")
            return
    suffix = path.suffix.lower()
    if suffix in ARCHIVE_EXT:
        if suffix == ".zip" and zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as z:
                members = [m for m in z.namelist() if any(rx.search(Path(m).name) for rx, _ in NAME_PATTERNS)
                           or m.lower().endswith((".csv", ".txt"))]
            problems.append(f"{rel}: archive (members: {members[:5]}) - archives are not allowed")
        else:
            problems.append(f"{rel}: archive file - archives are not allowed")
        return
    if suffix in TEXT_EXT:
        size = path.stat().st_size
        if suffix in {".csv", ".txt", ".tsv", ".dat"} and size > LARGE_TABLE_BYTES:
            problems.append(f"{rel}: large table ({size:,} bytes) - manual licence review required")
        hits = scan_text(path)
        if hits["tick"] > 0 and path.name not in ALLOWED_PRICE_FILES:
            problems.append(f"{rel}: {hits['tick']} tick-format quote rows")
        if hits["ohlc"] > PRICE_ROWS_LIMIT and path.name not in ALLOWED_PRICE_FILES:
            problems.append(f"{rel}: {hits['ohlc']} OHLC-like rows")


def check_manifest_sources(path, registry, problems):
    for manifest in path.rglob("manifest.json") if path.is_dir() else []:
        try:
            m = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as exc:
            problems.append(f"{manifest}: unreadable manifest ({exc})")
            continue
        for inp in m.get("data_inputs", []):
            sid = inp.get("source_id")
            if sid not in registry:
                problems.append(f"{manifest}: data source '{sid}' not registered in data/DATA_SOURCES.json")


def walk(path):
    if path.is_file():
        yield path
        return
    for p in path.rglob("*"):
        if p.is_file() and not (SKIP_DIRS & set(p.parts)):
            yield p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", type=Path, default=[ROOT])
    args = ap.parse_args(argv)
    registry = load_registry()
    problems = []
    for target in args.paths:
        target = target.resolve()
        if not target.exists():
            problems.append(f"{target}: does not exist")
            continue
        for f in walk(target):
            check_file(f, problems)
        check_manifest_sources(target, registry, problems)
    blocked = [s for s, v in registry.items() if v.get("redistribution") != "PERMITTED"]
    print(f"Registry: {len(registry)} source(s); redistribution NOT permitted for: {', '.join(blocked) or 'none'}")
    if problems:
        print(f"DATA LICENCE CHECK: FAIL ({len(problems)} issue(s))")
        for p in problems:
            print("  -", p)
        return 1
    print("DATA LICENCE CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
