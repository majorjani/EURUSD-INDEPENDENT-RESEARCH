# EUR/USD Independent Research Hub

An open, non-commercial project where independent researchers study EUR/USD
trading hypotheses and audit the methods behind them.

> **Status:** methodology phase. **No profitable strategy is claimed.**
> This is research, not investment advice. No signals, no managed accounts,
> no paid services.

## What this project is

- A shared **research protocol** for testing hypotheses causally, without lookahead
  ([docs/RESEARCH_PROTOCOL.md](docs/RESEARCH_PROTOCOL.md)).
- An **audit protocol** that every submitted result goes through
  ([docs/AUDIT_PROTOCOL.md](docs/AUDIT_PROTOCOL.md)).
- A **comparison table** that lists submitted studies side by side with the same
  metrics and cost assumptions ([comparison/](comparison/)).
- **Templates** for joining as a researcher and for submitting results
  ([templates/](templates/), [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/)).
- **Pre-publication checks** for reproducibility and data licensing
  ([tools/](tools/)).

## What this project is not

- It does not distribute market data. See
  [docs/DATA_LICENSE_POLICY.md](docs/DATA_LICENSE_POLICY.md). Each researcher gets
  data from the original provider under that provider's terms.
- It does not ask for, sell or promise profitable strategies.
- It does not place orders, connect to brokers or run live trading.

## Background

The maintainer explored EUR/USD Bid/Ask quotes from 2024-01 to 2025-12
(about 44.1 million quotes). The tests covered support/resistance, breakouts,
retests, volatility regimes, sessions, timeframe alignment and momentum/reversal.
One H4 breakout/retest variant looked positive. The internal audit then found
three problems:

1. **Selection bias.** The variant was picked after many hypotheses had been tried.
2. **Execution timing.** Entries could happen on the same bar as the signal,
   before the signal could be observed.
3. **No untouched out-of-sample period.**

So the result is treated as **unvalidated**. See
[docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) and
[docs/DATA_AUDIT_SUMMARY_2024_2025.md](docs/DATA_AUDIT_SUMMARY_2024_2025.md).

## How to contribute

1. Read the [research protocol](docs/RESEARCH_PROTOCOL.md) and the
   [data licence policy](docs/DATA_LICENSE_POLICY.md).
2. Open a **Researcher application** issue, or fill in
   [templates/RESEARCHER_APPLICATION.md](templates/RESEARCHER_APPLICATION.md).
3. **Pre-register** your hypothesis, parameter grid and test period before you
   look at the test data.
4. Submit results with
   [templates/RESULT_SUBMISSION.md](templates/RESULT_SUBMISSION.md) and a
   `manifest.json` (see [submissions/_example/](submissions/_example/)).
5. Run `python tools/prepublish_check.py submissions/<your-id>` before you open
   a pull request.

Methodological critique on its own is just as welcome as a full study.

## Repository layout

```
docs/          protocol, audit, data licence policy, reproducibility, known issues
templates/     researcher application, result submission, manifest schema
comparison/    unified comparison table (CSV + Markdown) and column definitions
submissions/   one folder per study (code, trades, metrics; never raw market data)
tools/         stdlib-only Python checks (licence scan, reproducibility, local audit)
data/          data-source registry only; market data files are blocked by .gitignore
```

## Licences

- Code (`tools/`): MIT, see [LICENSE](LICENSE).
- Documentation and templates: CC BY 4.0, see [LICENSE-DOCS](LICENSE-DOCS).
- Market data: **not included and not licensed by this project.**

## Contact

Please use [GitHub Issues](../../issues/new/choose) (templates provided) for
anything public.
