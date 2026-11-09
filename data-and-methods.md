# Data and Methods

This reference explains how the book moves from prices and research data to comparable returns. The code prints the actual dates and observation counts used in each analysis.

## Coverage of this edition

The market-data cutoff is **31 October 2026**. Kenneth French's downloaded monthly factors run through **September 2026**; adjusted prices run through **30 October 2026**. Price-only displays can therefore include October, while factor regressions cannot.

| Example | Matched return months |
|---|---|
| US factor-history examples | January 2000–September 2026 |
| Introductory SPY/IWN/VTV regressions | January 2010–September 2026 |
| Advanced common ETF comparison | February 2004–September 2026 |
| AVWS and AVWC regional regressions | November 2024–September 2026: 23 months |
| AVEM regional regression | April 2025–September 2026: 18 months |
| Common UCITS portfolio comparison | April 2025–September 2026: 18 months |

The available exchange-price history need not begin on a fund's inception date. In particular, AVEM's vendor history starts in March 2025; the first complete monthly return is April. No synthetic earlier fund returns are added.

## Returns, currencies and dates

All model inputs use decimal simple returns: `0.01` means 1%. A monthly factor observation labelled `2026-09-01` describes September's return, not a price sampled on September 1.

ETF returns are calculated from consecutive adjusted month-end closes. We require a prior month's close, exclude partial launch months, and do not fill missing months. A last price more than four calendar days before month-end is treated as incomplete; this boundary check allows common holidays but is not a full exchange-calendar audit.

For EUR listings, we first multiply the adjusted price by EUR/USD, expressed as dollars per euro. This retains both local-price and currency movements:

$$(1+R_{USD})=(1+R_{EUR})(1+R_{FX}).$$

FX can be carried forward for at most four calendar days. FX and exchange closes are not synchronised, so some measurement noise remains. A fund's trading currency alone does not identify the currency risk of its underlying holdings.

## Factors and inference

Factor data come from [Kenneth French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). Its published FF3 and FF5 SMB series have different constructions; comparisons preserve this difference. US research returns switched from CRSP FIZ to CIZ processing in January 2025. Current downloads can revise older observations, so a date cutoff does not recreate what investors knew at that date.

Adjusted market prices are retrieved through [yfinance](https://ranaroussi.github.io/yfinance/). They approximate distribution-reinvested market-price returns, not independently reconciled fund-NAV returns. Large moves are flagged and retained. Chapter 5 compares the three Avantis funds on shared dates in the price charts and portfolio analysis, while regional regressions retain each fund’s available matched history.

Applied regressions use Bartlett Newey–West covariance with the reported lag length, an $n/(n-k)$ correction and normal reference inference. The hand derivations explicitly identify uncorrected HC0/HAC calculations. Robust covariance does not remove model error, and the UCITS samples are too short for precise conclusions about persistent alpha.

## Portfolio conventions

Portfolio examples use fixed target weights rebalanced monthly, before the month's return. Wealth compounds total returns; Sharpe uses returns in excess of the matching risk-free rate. Alpha is annualised as twelve times the monthly intercept; this differs from the realised compound annual growth rate.

Fund expenses are already reflected in observed returns. Investor commissions, bid–ask spreads, taxes and portfolio rebalancing costs are additional. Academic long–short factor indices are hypothetical return constructions and omit investability constraints and financing costs.

The learning objective is to make these conventions explicit enough to reproduce and challenge. To run the notebooks, use the installation and execution instructions in the [source repository](https://github.com/beachnoir/FamaFrench).
