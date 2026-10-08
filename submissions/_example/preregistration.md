# Pre-registration — `_example` (SYNTHETIC)

- Hypothesis: placeholder.
- Signal observable at: close of the H4 bar (UTC). Earliest fill: first quote after close.
- Entry/exit: placeholder.
- Parameter grid: `lookback ∈ {10, 20}` (2 trials).
- Selection rule: the highest exploration-period DSR, then a single validation run.
- Cost model: Bid/Ask, USD 7 / 100k RT, slippage {0.0, 0.2} pips per side, swap from broker table.
- Primary metric: net expectancy (pips) on validation with 0.2 slippage; pass if 95% CI lower bound > 0.
