# Data Licence Policy

## Rule

**No market data is published in this repository** unless the provider's terms
explicitly permit redistribution and that permission is documented in
[data/DATA_SOURCES.json](../data/DATA_SOURCES.json) with evidence.

This applies to raw ticks, resampled OHLC bars, derived per-bar series that
could reconstruct prices, and "small samples".

## What may be published

- Code that reads provider files from the researcher's own local copy.
- File names, sizes and SHA-256 hashes of provider files. These let others
  confirm they have identical inputs.
- Aggregate statistics: row counts, spread quantiles, gap counts, monthly
  summaries.
- Strategy outputs: trade lists (timestamps, side, P&L in pips) and metrics.
  Trade lists must **not** include full price series.

## HistData.com (current primary source)

| Item | Status (checked 2026-10-08) |
|---|---|
| Explicit licence / redistribution terms on the FAQ page | **None found** |
| FAQ wording | "Use the data at your own will and risk." No warranty. |
| Paid tiers | FTP/SFTP and automatic updates are sold separately. |
| Timezone | EST without daylight-saving adjustment |
| **Redistribution status** | **UNVERIFIED → NOT PERMITTED** |

Free access does not imply a right to redistribute. Until HistData gives
written permission:

- Researchers download the data themselves from histdata.com.
- The project publishes only hashes and aggregate audit statistics.
- The "small permitted sample" offered in early outreach drafts is **on hold**.

To unblock: contact HistData, ask for written permission covering (a) a sample
and (b) full months, and record the reply (date, scope, contact) in
`DATA_SOURCES.json`.

## Enforcement

- `.gitignore` blocks `*.zip`, `*.csv` under `data/`, and common tick/bar file
  patterns.
- `tools/check_data_license.py` scans for HistData file names, tick-format rows
  (`YYYYMMDD HHMMSSfff,bid,ask,vol`), OHLC-like rows and large CSVs. It fails if
  it finds any of them.
- The maintainer runs `tools/prepublish_check.py .` before every push.
