# Known Issues in the Maintainer's Prior Work

Disclosed so that contributors do not repeat them.

| # | Area | Issue | Status |
|---|---|---|---|
| 1 | Strategy | The H4 breakout/retest variant was chosen after many hypotheses were explored. The trial count was not fully logged. | Treated as exploratory only. |
| 2 | Strategy | The event definition allowed an entry on the bar that produced the signal, before the signal was observable. | The definition needs a fix (Protocol §4.1). |
| 3 | Validation | No untouched period. All of 2024–2025 has been seen. | The 2026+ holdout is defined in Protocol §2. |
| 4 | Data audit | The monthly audit script labels Friday→Monday transitions. The actual session open is Sunday ~22:00 UTC, so those transitions are mislabelled. | Fixed in `tools/audit_local_month.py`. |
| 5 | Data audit | Only adjacent duplicate rows are detected. Non-adjacent duplicates are not checked. | Open. |
| 6 | Data audit | Timestamp precision is milliseconds. Rows are quote updates, not necessarily independent ticks. Quote source representativeness (which LPs) is unknown. | Open, documented. |
| 7 | Data licence | HistData redistribution rights are unverified. | Publication blocked (see the data licence policy). |
| 8 | Data audit | 2025-10 has 1 out-of-order timestamp (`AUDIT_COMPLETED_WITH_FLAGS`). All other months have 0. | Open. Locate the row and define a sort/drop rule. |
