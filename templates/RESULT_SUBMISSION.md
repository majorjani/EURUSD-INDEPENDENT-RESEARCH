# Result Submission — `<study_id>`

Place this file as `submissions/<study_id>/README.md`, together with
`manifest.json`, `preregistration.md`, `trades.csv`, `trials.csv`,
`metrics.json` and your code.

## 1. Summary
- **Author:**
- **Hypothesis (one sentence):**
- **Horizon / timeframe(s):**
- **Label claimed:** EXPLORATORY / PRE_REGISTERED / VALIDATED_OOS / REPLICATED / REJECTED
- **Replicates study:** (id, or "none")

## 2. Data
- Provider and files (names + SHA-256 are in the manifest):
- Period per role (exploration / validation / holdout):
- Timezone handling:
- Gap / duplicate / weekend handling:

## 3. Signal and execution
- Signal definition, and the exact time it becomes observable:
- Entry / exit / stop / sizing:
- Bid/Ask usage:
- Commission, slippage scenarios, swap:

## 4. Search process
- Number of trials N (from `trials.csv`):
- How the final parameters were selected:
- Link to the pre-registration commit:

## 5. Results (fill one row per period role and cost scenario)

| Period role | Slippage | Trades | Net exp. (pips) | PF | Hit % | Sharpe (daily, ann.) | DSR | Max DD | 95% CI exp. (block bootstrap) |
|---|---|---|---|---|---|---|---|---|---|
| exploration | 0.0 | | | | | | | | |
| exploration | 0.2 | | | | | | | | |
| validation | 0.2 | | | | | | | | |
| holdout | 0.2 | | | | | | | | |

Per-year and per-session breakdown:

## 6. Limitations and failure modes

## 7. Reproduction
```
# exact command(s)
```
Environment:

## 8. Checklist
- [ ] `python tools/prepublish_check.py submissions/<study_id>` passes
- [ ] No raw tick/OHLC data included
- [ ] `trials.csv` includes failed configurations
- [ ] Reproducibility checklist completed
