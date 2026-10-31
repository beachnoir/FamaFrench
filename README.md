# Factor Investing: From Statistical Foundations to Fama–French Models

A tutorial series that derives statistical results on hand-checkable examples, then applies them to current factor and ETF data. Read the notebooks in order; the solution manual covers all 18 exercises from notebooks 01–04.

**Reviewed and executed as of 31 October 2026.** Factor regressions use released data through **September 2026**. Adjusted prices extend through **30 October 2026**. October prices do not imply October factors are available. See the [review report](REVIEW.md) for corrections, findings, checks and limitations.

| Notebook | Contents |
|---|---|
| [01 — Statistical Foundations](01_Statistical_Foundations.ipynb) | CLTs and their assumptions, OLS by hand, HC covariance, Newey–West derivation, simulation calibration |
| [02 — Time-Series Foundations](02_Time_Series_Foundations.ipynb) | Prices and returns, ADF, ACF/PACF, ARCH, dependence diagnostics and their limits |
| [03 — Fama–French 3-Factor Model](03_Fama_French_3Factor.ipynb) | SPY/IWN/VTV, calendar-month returns, original FF3 factors, diagnostics, classical and robust inference |
| [04 — Advanced Factor Models](04_Advanced_Factor_Models.ipynb) | FF5, Carhart, reversals, beta-decile proxies, rolling estimates, research and explicit return scenarios |
| [05 — Practical Factor Investing](05_Practical_Factor_Investing.ipynb) | UCITS ETFs, USD conversion, regional factors, monthly portfolios, short-sample uncertainty and allocation sensitivity |
| [06 — Solution Manual](06_Solution_Manual.ipynb) | Worked calculations and discussion answers tied to the exercises and actual results |

The [online book](https://beachnoir.github.io/FamaFrench/) reflects the last deployed revision; local changes appear there only after deployment.

## Setup and execution

Use Python **3.12 or later**. The reviewed run used Python 3.14.2; exact analysis package versions are recorded in the [execution report](reports/execution_2026-10-31.json).

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v

# Fetch the dated snapshot, then execute all six notebooks in fresh kernels.
ANALYSIS_AS_OF=2026-10-31 python scripts/refresh_data.py
python scripts/run_notebooks.py --as-of 2026-10-31 --offline
jupyter notebook
```

Run from the repository root. In PowerShell set `$env:ANALYSIS_AS_OF="2026-10-31"` before running the refresh script. For a later refresh, replace the date in **both** commands. When opening notebooks interactively, set `ANALYSIS_AS_OF` in the environment before launching Jupyter; otherwise it defaults to today's Amsterdam date. Set `ANALYSIS_OFFLINE=1` to require the matching cache.

Downloads require internet access. Data are cached under `data/cache/YYYY-MM-DD/` with source, observation dates, retrieval time, settings and SHA-256 checksums. Corrupted caches fail explicitly. `--offline` refuses missing snapshots instead of silently substituting stale data. The runner saves each notebook only after all its cells succeed, and records failures in the execution report. To execute a subset, add `--notebooks 05_Practical_Factor_Investing.ipynb`.

**A date cutoff is not a historical data vintage.** French and Yahoo can revise prior observations. Re-downloading today's source with an earlier cutoff cannot recreate what was known then. Preserve the local cache separately if you need byte-identical input data; raw price and factor files are not committed. The [source manifest](reports/data_manifest_2026-10-31.json) records the reviewed snapshot's hashes, while notebook outputs are retained in Git.

## Conventions

- Returns are decimals in code unless explicitly labelled percent. French monthly labels identify the return month.
- ETF returns use consecutive adjusted **month-end** closes. A prior month-end is required, so partial launch months are excluded. Missing months are not filled. A four-calendar-day month-end boundary check excludes clearly incomplete observations; it is not a complete exchange-calendar audit.
- EUR listings are converted to USD price levels before returns, with at most four calendar days of FX carry-forward. Exchange and FX closes are not synchronised.
- Published FF3 and FF5 use different SMB series. Model comparisons preserve that distinction; they are not exactly nested.
- Applied HAC uses Bartlett weights, the stated lag rule, `n/(n-k)` correction and normal inference. Hand calculations explicitly omit that correction when deriving HC0/HAC. Lag choice and short-sample sensitivity matter.
- Monthly target-weight portfolios compound total returns; Sharpe uses excess returns. Academic long–short factor indices are illustrative and exclude implementation costs.

## Preview the book

Install Node.js 22 and the book dependency, then render the saved, executed outputs:

```bash
pip install -r requirements-book.txt
jupyter-book build --html
jupyter-book start
```

The book build does not run notebooks or refresh data. GitHub Pages deployment renders the committed results. Run the refresh and execution commands first when updating the analysis.

## Project layout

`analysis_utils.py` centralises parsing, caching, currency conversion and regression conventions. `scripts/refresh_data.py` builds a snapshot; `scripts/run_notebooks.py` executes notebooks. `tests/` checks alignment, missing observations, factor-table selection and covariance conventions. `reports/` contains data provenance and execution records. `myst.yml`, `custom.css` and `.github/workflows/deploy-book.yml` configure the book.

Legacy holdings CSVs and exported figures in an existing local checkout are not inputs to this analysis. No holdings-based conclusions are made from them.

## Sources and limitations

Factor definitions and data come from [Kenneth French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html); adjusted market prices come through [yfinance](https://ranaroussi.github.io/yfinance/). Primary research is linked beside the relevant discussion. French's US files switched from CRSP FIZ to CIZ processing in January 2025, which affects historical comparability; the notebooks use the current published vintage.

The practical portfolio has only **18 matched months**. Several early IWMO price jumps remain unverified, are disclosed and retained, and are accompanied by a post-2018 sensitivity analysis. Neither asymptotic p-values nor an in-sample optimum establish a persistent premium. This is educational analysis; all material is provided as-is for learning purposes.
