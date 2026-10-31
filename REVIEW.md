---
downloads:
  - file: reports/execution_2026-10-31.json
    title: Notebook execution report
  - file: reports/data_manifest_2026-10-31.json
    title: Data provenance manifest
---

# Project review — 31 October 2026

All six notebooks were reviewed, corrected and executed from fresh kernels against a dated public-data snapshot. The changes cover calculations, mathematical explanations, exercise solutions, research claims, plots, reproducibility and the book workflow.

## Data coverage

| Analysis | First observation used | Latest available observation |
|---|---|---|
| US factor-only examples | January 2000 | September 2026 |
| Introductory US ETF regressions | January 2010 | September 2026 |
| Advanced common SPY/IWN/VTV regressions | February 2004 | September 2026 |
| AVWS / AVWC regional regressions | November 2024 | September 2026 — 23 months |
| AVEM regional regression | April 2025 | September 2026 — 18 months |
| IWMO regional regression | November 2014 | September 2026 — 143 months |
| Common UCITS portfolio comparisons | April 2025 | September 2026 — 18 months |
| Raw adjusted-price histories | Varies by ticker | 30 October 2026 |

October complete-month price returns are available for descriptive displays, but October factor returns were not in the downloaded releases. All regressions stop at the latest overlapping published month. AVEM's observed Yahoo/Xetra history starts on 24 March 2025; that is not its fund inception date.

The [data manifest](reports/data_manifest_2026-10-31.json) contains 19 input-source records with retrieval times, coverage, settings and SHA-256 checksums. The cache is kept locally under `data/cache/2026-10-31/`. Source revisions mean an as-of cutoff alone cannot reconstruct a historical data vintage.

## Material corrections

| Area | Correction and consequence |
|---|---|
| Return alignment | Replaced first-trading-day returns shifted backwards with consecutive adjusted month-end returns. Removed partial launch months and prohibited filling missing monthly returns. Factor and asset returns now cover the same calendar intervals. |
| Currency | Convert EUR adjusted-price levels to USD before calculating returns, preserving the first valid interval. Explicitly limit FX carry-forward and disclose asynchronous closes. |
| Source parsing | Parse only the first value-weighted/monthly table, stop before annual or equal-weighted sections, mask source sentinels and validate dates. Select beta **deciles by name**, fixing a solution that mixed quintiles with deciles. |
| Model definitions | Keep original FF3 SMB separate from FF5 SMB. Published FF3 and FF5 are not exactly nested; a higher R² is not mechanically guaranteed. Define the advanced regression helper before its first use. |
| Inference | State covariance corrections and normal/t reference distributions explicitly; distinguish HC0 from corrected lag-zero HAC/HC1; add robust joint inference, lag sensitivity and short-sample sensitivity. Correct attribution of the lag heuristic. |
| Theory | Correct CLT moment/dependence conditions, score versus residual dependence, exogeneity, GARCH/ADF interpretation, covariance summability versus mixing, and Berry–Esseen's absolute third moment. Diagnostics supply evidence, not proofs of assumptions. |
| Time series | Compound multi-month simple returns; distinguish a fixed-window loss from drawdown; include starting wealth in drawdown calculations; fix rolling-window endpoints. |
| Beta strategy | Remove full-sample beta look-ahead from the leveraged proxy. Use lagged 60-month estimates and a common comparison window; distinguish decile proxies from published BAB. |
| Simulations | Compare tilted and benchmark wealth using the **same market shocks**. Replace unsupported manager-return forecasts and arbitrary cost waterfalls with labelled scenarios, including zero and negative premia. Check simulated probabilities against the analytical result. |
| Portfolio analysis | Use monthly rebalancing, a common sample, total-return wealth and excess-return Sharpe consistently. Verify weighted constituent coefficients equal portfolio coefficients under a common benchmark. Include optimisation endpoints and leave-one-month-out sensitivity. |
| Data quality | Remove mechanical deletion of >10% moves and following days. Flag and retain extremes, disclose unresolved early IWMO observations, and add a fixed post-2018 sensitivity. |
| Solutions | Align all 18 answers with their exercises, fix the hand-calculation dataset, derive comparisons from actual outputs, correct the 36-basis-point economic-significance discussion and avoid double-counting fund expenses. |
| Research | Verify primary sources; correct Chen–Velikov's journal and published results, distinguish working papers from publications, and remove unsubstantiated claims about manager-specific expected returns or guaranteed factor survival. |
| Maintenance | Centralise data handling, cache and checksum inputs, provide refresh/execution scripts and regression tests, bound dependencies, retain notebook results and render those results in the book. |

## Findings from the updated run

- In the introductory 2010–September 2026 common sample, SPY has the highest FF3 R², approximately **0.9963**, versus **0.9824** for IWN and **0.9370** for VTV. The earlier solution's assertion that IWN had the highest fit was incorrect. Fit is not investment performance.
- The statistical-foundations simulation rejects a true null **18.35%** of the time using classical inference and **7.40%** using HAC, against a 5% nominal level. HAC improves this design but does not achieve exact calibration; its Monte Carlo standard error is approximately 0.59 percentage points.
- AVWS's regional six-factor annualised arithmetic alpha is approximately **−9.12%** in only 23 months. Its p-value changes from about **0.021** under the default asymptotic HAC method to **0.101** under the HC3/approximate-t sensitivity. These methods have different assumptions; the contrast illustrates fragile short-sample inference, not a definitive performance verdict.
- On the shared 18-month sample, the monthly rebalanced 50/40/10 base portfolio has an excess Sharpe of approximately **1.786**, versus **1.737** with a 20% IWMO allocation. The historical optimiser selects a weight very close to zero, while leave-one-month-out fits range from **0% to 30%**. These are in-sample descriptions, not allocation recommendations.
- The early IWMO series contains **15 flagged daily moves above 10% in magnitude**, including offsetting jumps. They remain unverified and are not silently edited. Its full-history FF5-plus-momentum R² is approximately **0.775**, versus **0.902** from 2018 onward. Different samples reflect both possible data problems and different market conditions; this comparison cannot isolate the cause. The recent common portfolio window contains none of these flagged early moves.

## Validation

- All **six notebooks**, **92 code cells**, executed in order with fresh kernels and no execution errors. See the [execution report](reports/execution_2026-10-31.json) for exact package versions, runtimes and notebook hashes.
- **13 regression tests** cover first-table parsing, missing-value sentinels, date validation, month-end alignment, partial periods, missing months, stale closes, FX conversion, true-decile selection, cache corruption, HAC/HC1 equivalence, portfolio coefficient linearity and invalid regression inputs.
- Notebook structure, Python syntax, execution order and saved outputs are checked by `scripts/check_notebooks.py`. CI runs these checks without relying on live market-data downloads.
- Figures were inspected for readable labels, missing series and misleading conclusions. Rolling exposures now include pointwise uncertainty intervals and separate figures by ETF.
- The book renders saved outputs; its strict HTML build is validated locally. The official Avantis product page is search-indexed but returns 403/404 to automated requests in this environment; that exact URL remains a visible link-check warning rather than a build-blocking error. Raw data are not fetched during deployment. A local `nbstripout` rule that would remove results at commit time was disabled for notebooks, and `.gitattributes` records the output-preservation policy.

## Remaining limitations

This is a current-vintage educational analysis, not an independently audited market-data product or a point-in-time backtest. Yahoo prices were checked for structural problems and extreme moves, but not reconciled with every exchange close or fund NAV. FX timing, vendor adjustments and source revisions remain potential errors. The four-day month-end boundary check is deliberately explicit and is not a full holiday-calendar audit.

Short histories, model mismatch, multiple comparisons and asymptotic covariance estimates limit inference. Regional fund regressions and common-developed-benchmark portfolio regressions answer different questions. Portfolio wealth omits investor trading costs and taxes; factor-spread indices omit financing and implementation frictions. No live trading strategy, future premium or causal explanation is established.

See [README](README.md) for the exact refresh, execution, testing and build commands. Existing ignored holdings CSVs and legacy figure exports are not used as analysis inputs. Deployment requires passing analysis validation and a successful strict book build.
