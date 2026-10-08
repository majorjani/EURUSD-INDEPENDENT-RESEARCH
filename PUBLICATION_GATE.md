# Publication Gate (maintainer only)

Nothing leaves this machine without **explicit, per-item approval by the
maintainer**. Approval for one item does not carry over to the next.

## Before creating or pushing the GitHub repository
- [ ] `python tools/prepublish_check.py` → `PREPUBLISH: PASS`
- [ ] `git status` / `git ls-files` reviewed. No `*.zip`, no `DAT_ASCII_*`, no CSV under `data/`.
- [ ] `Contact via GitHub Issues` placeholder in README replaced (or removed).
- [ ] Licence choice confirmed (MIT code / CC BY 4.0 docs, or changed).
- [ ] Repository visibility decided (start **private**, then switch to public after review).
- [ ] The maintainer approved: "push repo" ☐ (date: ____ )

## Before each forum post
- [ ] Forum rules re-read on the day of posting (self-promotion, links, new-account limits).
- [ ] No attempt to bypass rate limits, CAPTCHAs, karma/age thresholds or moderation queues.
      If a forum blocks the post, stop and report back.
- [ ] The post links only to the repo (once it is public). No data, no sample files.
- [ ] Logged in the maintainer's private outreach log (not in this repository).
- [ ] The maintainer approved this specific post ☐ (forum: ____ date: ____ )

## Hard rules
- Never publish HistData tick or OHLC data, including samples, until written permission is recorded in `data/DATA_SOURCES.json`.
- Never resubmit the MQL5 thread (already live: https://www.mql5.com/en/forum/517909).
- No paid services (GitHub paid plans, promoted posts, paid data) without approval.
- No trading orders, broker connections or EA deployment. The maintainer's other systems and any live trading are out of scope and must not be touched.
