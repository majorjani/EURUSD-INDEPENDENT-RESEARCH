# Research Protocol

Version 0.1 (draft, 2026-10-08)

This protocol applies to every study submitted to the project. It aims to keep
false discoveries from being reported as edges.

## 1. Scope

- Instrument: EUR/USD spot.
- Horizons: swing (H4–D1), intraday (M15–H1) and scalping (tick–M5).
- Data: Bid/Ask quotes. Studies that use mid prices only must say so and are
  flagged as `COST_MODEL_WEAK`.

## 2. Data periods

| Role | Period | Rule |
|---|---|---|
| Exploration | 2024-01-01 – 2025-06-30 | Anything goes, but every trial is logged. |
| Validation | 2025-07-01 – 2025-12-31 | Used only for final model selection. Logged. |
| Holdout | 2026-01-01 onward (untouched) | Evaluated **once** for pre-registered models. |

- **2024–2025 results alone can never be labelled "validated".**
  The maintainer has already explored this whole period.
- All timestamps must be converted to UTC. HistData timestamps are
  EST (UTC−5) **without** daylight-saving adjustment.

## 3. Pre-registration

Before any validation or holdout data is touched, record the following in the
submission folder (`preregistration.md`, committed with a timestamp):

- Hypothesis in one sentence, plus the economic or microstructural rationale.
- Exact signal definition, including the moment the signal becomes observable.
- Entry, exit, stop and position-sizing rules.
- The full parameter grid, and how the final parameters will be chosen.
- Cost model (see §5).
- Primary metric and pass/fail threshold.

## 4. Causality rules (no lookahead)

1. A signal computed from a bar can act only **after that bar closes**. The
   earliest fill is the first quote after the close timestamp.
2. Multi-timeframe features may use only higher-timeframe bars that have
   **closed** at decision time. Partially formed bars are not allowed.
3. Support/resistance levels, swing points and pivots must be confirmed with
   their confirmation lag included (for example, a fractal needs N bars on the
   right side).
4. Normalisation statistics (volatility, z-scores, quantiles) use trailing
   windows only.
5. Within-bar ordering of high and low is unknown in OHLC data. Stop/target
   resolution must use tick data or a conservative rule (stop first).

## 5. Execution and cost model

- Longs fill at **Ask** and exit at **Bid**; shorts fill at Bid and exit at Ask.
- Add commission. The default is USD 7 per 100k round-turn (state your value).
- Slippage: run at least two scenarios, 0 pips and 0.2 pips per side. A result
  must survive the stressed scenario.
- Swap/rollover is required for positions held over 22:00 UTC (state the source
  or assumption).
- Quotes during illiquid windows (around 21:00–23:00 UTC and weekend opens) need
  a stated handling rule.

## 6. Logging every trial

- Every configuration run, including failures, goes into `trials.csv`
  (`trial_id, timestamp, hypothesis_id, params_json, period, n_trades, metric`).
- The total number of trials (N) is reported and used in the multiple-testing
  adjustment.

## 7. Statistical evaluation

Report all of the following:

- Net expectancy per trade (pips and R), profit factor, hit rate, n trades.
- Annualised Sharpe on **daily** P&L, not per trade.
- Max drawdown and the longest time to recover from a drawdown.
- **Deflated Sharpe Ratio** (Bailey & López de Prado, 2014) using N from §6.
- Block or stationary bootstrap confidence intervals, to handle serial
  dependence and overlapping trades.
- Per-year and per-session breakdowns, to check stability.
- For walk-forward studies: the in-sample/out-of-sample split schedule, and
  out-of-sample results only.
- Optional: Probability of Backtest Overfitting (CSCV), White's Reality Check or
  Hansen's SPA when many variants are compared.

## 8. Second engine / portability

A result is promoted to `REPLICATED` only when a different researcher reproduces
it with an independent implementation (a different codebase or platform). The
replicator works from the pre-registration document, not from the original code.

## 9. Result labels

| Label | Meaning |
|---|---|
| `EXPLORATORY` | Exploration period only. No claims allowed. |
| `PRE_REGISTERED` | Plan committed before validation or holdout data was touched. |
| `VALIDATED_OOS` | Passed validation **and** a single holdout evaluation. |
| `REPLICATED` | `VALIDATED_OOS` and independently reproduced. |
| `REJECTED` | Failed a pre-registered test. Kept in the table; negative results count. |
| `AUDIT_FLAGGED` | The audit found a protocol violation. See the audit notes. |

## 10. References

- Bailey, D. H., & López de Prado, M. (2014). *The Deflated Sharpe Ratio.*
- Bailey, Borwein, López de Prado & Zhu (2017). *The Probability of Backtest Overfitting.*
- White, H. (2000). *A Reality Check for Data Snooping.*
- Hansen, P. R. (2005). *A Test for Superior Predictive Ability.*
- Harvey, Liu & Zhu (2016). *…and the Cross-Section of Expected Returns.*
- Politis & Romano (1994). *The Stationary Bootstrap.*
