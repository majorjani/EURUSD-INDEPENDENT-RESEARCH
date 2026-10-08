#!/usr/bin/env python3
"""Run every pre-publication gate. Must pass before any push or pull request.

Usage:
  python tools/prepublish_check.py              # whole repo: licence scan + all submissions
  python tools/prepublish_check.py submissions/<study_id>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_data_license  # noqa: E402
import check_reproducibility  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main(argv):
    targets = [Path(a).resolve() for a in argv] or [ROOT]
    rc = check_data_license.main([str(t) for t in targets])
    folders = []
    for t in targets:
        if t == ROOT:
            folders += [p for p in (ROOT / "submissions").iterdir() if p.is_dir()]
        elif t.is_dir() and (t / "manifest.json").exists():
            folders.append(t)
    for f in folders:
        rc |= check_reproducibility.main([str(f)])
    print("=" * 60)
    print("PREPUBLISH: PASS" if rc == 0 else "PREPUBLISH: FAIL - do not publish")
    print("Reminder: every public post/push still needs explicit maintainer approval (PUBLICATION_GATE.md).")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
