# Data Audit Summary — HistData EUR/USD tick, 2024-01 to 2025-12

Aggregate statistics only. **No price data is included** (see [DATA_LICENSE_POLICY.md](DATA_LICENSE_POLICY.md)).
Researchers who download the same months from histdata.com can compare SHA-256 hashes to confirm they have identical inputs.

- Months audited: 24/24 (ZIP integrity PASS; 23 `AUDIT_COMPLETED`, 1 `AUDIT_COMPLETED_WITH_FLAGS`)
- Total valid quote rows: **44,134,016**
- Format: Generic ASCII tick, Bid/Ask; timestamps EST (UTC−5) without DST, converted to UTC
- Invalid rows and Bid>Ask violations: 0 in every month. Out-of-order timestamps: **1 row in 2025-10** (open item, see KNOWN_ISSUES.md #8)

| Month | Valid rows | Gaps >60 s (incl. weekends) | First UTC | Last UTC | ZIP SHA-256 | Flags |
|---|---:|---:|---|---|---|---|
| 2024-01 | 2,176,113 | 265 | 2024-01-01T22:00:12 | 2024-02-01T04:59:57 | `9a4ae15d87abff93311cc60adf7fe83de9078664c6baaf2984fcc70f160b3da9` | — |
| 2024-02 | 1,702,058 | 287 | 2024-02-01T05:00:00 | 2024-03-01T04:59:37 | `bf38a79ae8032429adef649c35005100ba60eb88d247ac0432b48590db133517` | — |
| 2024-03 | 1,476,727 | 427 | 2024-03-01T05:00:00 | 2024-04-01T04:59:56 | `b70fcaf5ee82ca6dc847f8a6c0f4354ecb456ae8579faed8563b53ac2ac324df` | — |
| 2024-04 | 1,560,509 | 445 | 2024-04-01T05:00:00 | 2024-05-01T04:59:55 | `cb9b219aa3c557f8f4c3e5bddcdd3fc75a7f5113590329153fc17fce34ad17f2` | — |
| 2024-05 | 1,240,628 | 652 | 2024-05-01T05:00:07 | 2024-05-31T21:59:59 | `c81fd7c2c94829664e523dd18e54e985c07f7b7be6f4fa5998cbe7a15569360c` | — |
| 2024-06 | 1,344,506 | 599 | 2024-06-02T22:00:07 | 2024-07-01T04:59:57 | `162e85bb8da67b35852b2950f1aa2e6d2eff7f2fef738849bc1327e4f5392d12` | — |
| 2024-07 | 1,463,751 | 623 | 2024-07-01T05:00:00 | 2024-08-01T04:59:55 | `d46ff671cd5fd65c605d7c03496217dcbca3ed39086dc3afe202f193f518442c` | — |
| 2024-08 | 1,840,228 | 336 | 2024-08-01T05:00:01 | 2024-08-30T21:59:59 | `89d4922aab8b3e83f10d8c9635f4e247652e8c0c1f7dcda306cbf83fc4b2751a` | — |
| 2024-09 | 1,805,004 | 480 | 2024-09-01T22:00:05 | 2024-10-01T04:59:59 | `00ab61749d1d70081c18f9dfe4a175e160c54de29edb779a713432fcbae10059` | — |
| 2024-10 | 1,772,075 | 369 | 2024-10-01T05:00:00 | 2024-11-01T04:59:59 | `5041948a91b7c3ab6036c08c5adfbe2438c7c3d21ff7ccdaafbc8d61f18d039d` | — |
| 2024-11 | 2,312,773 | 171 | 2024-11-01T05:00:00 | 2024-11-29T21:59:59 | `2ca378fffe3fcaee698ef2486e6407d72afd8f292002983463c338f329838f17` | — |
| 2024-12 | 1,979,900 | 355 | 2024-12-01T22:00:48 | 2024-12-31T21:59:58 | `a4dd430ed823a7671dd012faff1eda56f46a7cc54dd7bdb5cd5dc19db3eda3c5` | — |
| 2025-01 | 2,283,239 | 201 | 2025-01-01T22:00:14 | 2025-01-31T21:59:57 | `159f906f8055f6ee835d95806cf7fdf4023b6e3ef098aa308d2ab6ce53ac964a` | — |
| 2025-02 | 2,053,257 | 204 | 2025-02-02T22:00:07 | 2025-02-28T21:59:58 | `63c3b2717c024f7aada8642b38e7a944646dbe2440303632918e5c594db2313e` | — |
| 2025-03 | 2,353,340 | 245 | 2025-03-02T22:00:00 | 2025-04-01T04:59:59 | `0746c04af3a4aba26a559d0bbd665bbeda8e237c624b51625e63bf10066cc096` | — |
| 2025-04 | 3,916,978 | 164 | 2025-04-01T05:00:00 | 2025-05-01T04:59:58 | `613aa42d654e66853ec35d233a372adf66d818614a2ebe9f92be4add59f7970e` | — |
| 2025-05 | 2,412,228 | 163 | 2025-05-01T05:00:01 | 2025-05-30T21:59:59 | `3ce49d7b44e8b17c942ad2d5e77e317c023a5884f090c086806b888dae633f77` | — |
| 2025-06 | 2,044,343 | 185 | 2025-06-01T22:03:32 | 2025-07-01T04:59:54 | `a36a057d0afcb38e11cab1bec01c4e6de83f053530e0ea99c88acf99145af77c` | — |
| 2025-07 | 1,555,775 | 233 | 2025-07-01T05:00:00 | 2025-08-01T04:59:56 | `c671c79da3955d7f97dcbe4386165ac059878d29019e7ca6453b286bad2a2a74` | — |
| 2025-08 | 1,338,471 | 260 | 2025-08-01T05:00:00 | 2025-09-01T04:59:59 | `c9b4869da23f24082614b8666159ce4a1f83573f5e687879634d7640f507a229` | — |
| 2025-09 | 1,493,622 | 321 | 2025-09-01T05:00:00 | 2025-10-01T04:59:59 | `d3a6310bd8427b6d9ea2d68c0edf5da2c469511a61b957b0a0d41c45dc9d9310` | — |
| 2025-10 | 1,483,175 | 320 | 2025-10-01T05:00:05 | 2025-10-31T20:59:57 | `80ff5b3bb0e172e30cf6003feb59bbb147629443041555d5e44ab54e40f7de5e` | out_of_order=1 |
| 2025-11 | 1,242,212 | 310 | 2025-11-02T22:00:01 | 2025-12-01T04:59:55 | `3e2b099ea6e94657b27c03ae64f4238d13ece34748289148b3675c250b0e65ae` | — |
| 2025-12 | 1,283,104 | 423 | 2025-12-01T05:00:00 | 2025-12-31T21:58:59 | `05a79fad8637861c997e7ab5e9854aa8a5d6030aee4d6b448f9fa52b915911a5` | — |

## Caveats

- These are first-pass quality audits, not strategy validation.
- HistData month files are cut at EST midnight, so each month's UTC range extends to ~05:00 UTC on the 1st of the next month.
- Earlier scripts mislabelled Friday→Monday transitions. `tools/audit_local_month.py` classifies weekly closures as Friday ~22:00 → Sunday ~22:00 UTC. It was verified on 2025-01: identical row count, hash and spread quantiles to the earlier detailed audit.
- Spread quantiles for 2025-01 (pips): p50 0.3, p90 0.5, p95 0.6, p99 1.3, p99.9 4.3; max 13.3.
- Non-adjacent duplicates and feed representativeness are not certified.
