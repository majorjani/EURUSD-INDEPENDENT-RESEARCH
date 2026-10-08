# Audit Protocol

Every submission is audited before it enters the comparison table. The auditor
must be someone other than the author. Findings are recorded in
`submissions/<id>/AUDIT.md`.

## A. Admissibility (automatic)

Run `python tools/prepublish_check.py submissions/<id>`. It must pass:

- [ ] `manifest.json` is present and valid against
      [templates/manifest.schema.json](../templates/manifest.schema.json).
- [ ] Every file listed in the manifest exists, and its SHA-256 matches.
- [ ] There are no raw market-data files (tick or OHLC) in the submission.
- [ ] Every data source in the manifest is registered in
      [data/DATA_SOURCES.json](../data/DATA_SOURCES.json).

## B. Data integrity

- [ ] The data source, period and timezone conversion are stated.
- [ ] Input file hashes are recorded, so another researcher with the same
      provider files can confirm identical inputs.
- [ ] Weekend and holiday gaps are handled explicitly. The Sunday ~22:00 UTC
      open is not mislabelled as Monday.
- [ ] Duplicate and out-of-order quotes are handled, with the rule stated.

## C. Causality

- [ ] The signal timestamp is earlier than the fill timestamp for every trade.
      Check this on `trades.csv`: `signal_time_utc < entry_time_utc`.
- [ ] No higher-timeframe bar is used before it closes.
- [ ] Indicator warm-up periods are excluded from evaluation.
- [ ] Level and pivot confirmation lag is implemented.
- [ ] Spot-check: the auditor recomputes the signals for 20 random trades by hand
      or with independent code.

## D. Execution realism

- [ ] Bid/Ask is used correctly for entry and exit.
- [ ] Commission, slippage scenarios and swap are applied as in Research
      Protocol §5.
- [ ] The stop/target ambiguity inside a bar is resolved conservatively or with
      ticks.
- [ ] No fills happen inside data gaps longer than 60 s without a stated rule.

## E. Selection and statistics

- [ ] `trials.csv` exists, and the total trial count N is reported.
- [ ] The Deflated Sharpe Ratio is computed with that N.
- [ ] Confidence intervals account for serial dependence.
- [ ] The holdout was evaluated once. If more than once, the result is labelled
      `AUDIT_FLAGGED`.
- [ ] The pre-registration commit predates the first validation/holdout run.

## F. Reproducibility

- [ ] Environment pinned (`requirements.txt` / `environment.yml` / platform
      version).
- [ ] A single command regenerates `metrics.json` and `trades.csv` from the
      provider data.
- [ ] The auditor re-ran it, and the metrics match within tolerance
      (expectancy ±1%, trade count exact).

## G. Cross-study independence

Similar results from several researchers are **not** automatic confirmation.
Before a study is counted in `replicated_by`, the auditor records:

- [ ] **Shared data:** same provider and same files (compare hashes)? If yes, it
      confirms the code, not the edge. Credit as cross-data replication only
      with a different vendor or feed.
- [ ] **Shared method:** was code, rule text or parameters copied from the
      original study? If yes, label it `REPLICATED (code)`, not independent.
- [ ] **Shared selection:** did the replicator pick this hypothesis *because*
      it looked good in the table? If yes, add the original study's N to the
      replicator's N for the DSR.
- [ ] **Project-wide multiple testing:** report the total N across all studies
      of the same hypothesis family; the comparison table's best row is itself
      a selected result.
- [ ] **Correlated P&L:** if two studies trade the same hours, compute the
      correlation of their daily P&L. Above 0.7, treat them as one result.

## Verdict

| Verdict | Condition |
|---|---|
| `PASS` | All sections are satisfied. |
| `PASS_WITH_NOTES` | Only minor documentation gaps. |
| `AUDIT_FLAGGED` | A violation in C, D or E. The result stays visible with a flag. |
| `REJECTED_ADMISSION` | Fails section A (for example, raw data included). Not merged. |
