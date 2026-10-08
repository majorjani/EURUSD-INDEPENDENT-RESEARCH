# Comparison Table — Column Definitions

`comparison_table.csv` is the source of truth. `COMPARISON_TABLE.md` is a
rendered view of it. Each row is one study × period role × slippage scenario.

| Column | Definition |
|---|---|
| `study_id` | Folder name under `submissions/` |
| `author` | Credited handle |
| `hypothesis` | One-line description |
| `horizon` | swing / intraday / scalping |
| `timeframe` | Signal timeframe (e.g. H4, M5, tick) |
| `data_source` | `source_id` from `data/DATA_SOURCES.json` |
| `period_role` | exploration / validation / holdout |
| `period_start`, `period_end` | ISO dates (UTC) |
| `slippage_pips` | Per-side slippage scenario |
| `commission_usd_rt` | Per 100k round-turn |
| `n_trials` | Total configurations tried (whole study) |
| `n_trades` | Trades in this period |
| `net_exp_pips` | Mean net P&L per trade after all costs |
| `profit_factor` | Gross win / gross loss after costs |
| `hit_rate` | Fraction of winning trades |
| `sharpe_daily_ann` | Annualised Sharpe of daily net P&L (√252) |
| `dsr` | Deflated Sharpe Ratio, computed with `n_trials` |
| `max_dd_pips` | Peak-to-trough drawdown of cumulative net P&L |
| `ci95_low`, `ci95_high` | Block-bootstrap 95% CI of `net_exp_pips` |
| `label` | Research Protocol §9 label |
| `audit_verdict` | PASS / PASS_WITH_NOTES / AUDIT_FLAGGED / PENDING |
| `replicated_by` | study_id(s) of independent replications |
| `notes` | Short free text |

Rows are never deleted. Rejected and flagged studies stay in the table, because
negative results are part of the record.
