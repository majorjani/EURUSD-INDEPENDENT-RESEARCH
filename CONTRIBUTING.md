# Contributing

1. Open a **Researcher application** issue.
2. Fork the repository and create `submissions/<study_id>/` by copying `submissions/_example/`.
3. Commit `preregistration.md` **before** running validation or holdout tests.
4. Add code, `trades.csv`, `trials.csv`, `metrics.json` and a README based on
   `templates/RESULT_SUBMISSION.md`.
5. Run:
   ```
   python tools/check_reproducibility.py submissions/<study_id> --update-hashes
   python tools/prepublish_check.py submissions/<study_id>
   ```
6. Open a pull request. An auditor (not the author) applies
   [docs/AUDIT_PROTOCOL.md](docs/AUDIT_PROTOCOL.md). The maintainer then adds
   rows to `comparison/comparison_table.csv` and runs `python tools/render_comparison.py`.

**Never commit market data.** Pull requests that contain tick or OHLC files are
closed, and their history must be purged.

## Code of conduct
Be precise and respectful. Critique the methods, not the people. Do not sell
signals, courses or EAs, and do not use this project for referrals.
