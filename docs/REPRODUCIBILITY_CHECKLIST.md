# Reproducibility Checklist

Copy this into your submission's `README.md` and tick each item.

## Inputs
- [ ] The data provider and exact files are listed in `manifest.json` → `data_inputs`.
- [ ] The SHA-256 of each input file is recorded.
- [ ] The timezone conversion is stated (HistData: fixed UTC−5 → UTC).

## Environment
- [ ] Language and version (for example, Python 3.12.4, MQL5 build, LEAN version).
- [ ] Dependency lock file is committed.
- [ ] Random seeds are fixed and listed.

## Execution
- [ ] One command reproduces all outputs (`make`, `python run.py --config ...`).
- [ ] Configuration lives in a file, not hard-coded.
- [ ] Runtime and hardware are noted.

## Outputs (committed)
- [ ] `trades.csv`: `trade_id, signal_time_utc, entry_time_utc, exit_time_utc, side, entry_px, exit_px, pnl_pips, cost_pips, period_role`
- [ ] `metrics.json`: see the metric names in [comparison/COLUMNS.md](../comparison/COLUMNS.md)
- [ ] `trials.csv`: every configuration tried
- [ ] `preregistration.md`: committed before validation/holdout runs

## Verification
- [ ] `python tools/prepublish_check.py submissions/<id>` passes.
- [ ] A second person re-ran the study, and the outputs matched.

> `entry_px` and `exit_px` are individual fill prices at trade times. This is
> considered non-reconstructive and is allowed. Do not add OHLC columns or
> per-bar series to `trades.csv`.
