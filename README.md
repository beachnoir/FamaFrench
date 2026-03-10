# Factor Investing: From Statistical Foundations to Fama-French Models

A self-contained tutorial series on factor investing for anyone with an undergraduate-level background in probability and statistics. Key results are derived and demonstrated on data small enough to verify by hand, then applied to real market data.

## Notebooks

Work through these in order — each builds on the previous one.

| # | Notebook | Topics |
|---|----------|--------|
| 1 | [Statistical Foundations](01_Statistical_Foundations.ipynb) | Descriptive stats, CLT, hypothesis testing, OLS by hand, HC sandwich estimator, Newey-West HAC derivation — all on hand-checkable datasets (5–8 observations) |
| 2 | [Time-Series Foundations](02_Time_Series_Foundations.ipynb) | Prices vs returns, stationarity & ADF tests, ACF/PACF, Ljung-Box, volatility clustering & ARCH, ergodicity & mixing, full assumption stack for FF regressions |
| 3 | [Fama-French 3-Factor Model](03_Fama_French_3Factor.ipynb) | FF3 theory, real data (Ken French + Yahoo Finance ETFs: SPY, IWN, VTV), OLS normal equations, statsmodels, R²/F-tests, diagnostics (JB, BP, DW, VIF), robust SEs, Newey-West, interpretation & predictions, multi-ETF comparison |
| 4 | [Advanced Factor Models](04_Advanced_Factor_Models.ipynb) | FF5, Carhart 4-factor, Novy-Marx profitability, reversals, beta anomaly & BAB, meta-research (replication, out-of-sample decay, Adaptive Markets Hypothesis), the practitioner debate (DFA, Avantis, premium timing), rolling-window analysis |
| 5 | [Practical Factor Investing](05_Practical_Factor_Investing.ipynb) | Real ETF data (AVWS, AVWC, AVEM, IWMO), monthly FF5+Momentum regressions with regional factor matching, portfolio construction (50/40/10), constrained optimisation, factor profiles, limitations of short samples |
| 6 | [Solution Manual](06_Solution_Manual.ipynb) | Complete worked solutions to all 18 exercises from notebooks 01–04, with code, output interpretation, and explanations |

## Read Online

**[View the book on GitHub Pages &rarr;](https://beachnoir.github.io/FamaFrench/)**

## Quick Start

```bash
git clone https://github.com/beachnoir/FamaFrench.git && cd FamaFrench
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

Requires Python 3.9+.

### Preview the book locally

```bash
pip install -r requirements-book.txt
jupyter-book build --execute --html
jupyter-book start                     # opens at http://localhost:3000
```

## Project Structure

```
FamaFrench/
├── 01_Statistical_Foundations.ipynb
├── 02_Time_Series_Foundations.ipynb
├── 03_Fama_French_3Factor.ipynb
├── 04_Advanced_Factor_Models.ipynb
├── 05_Practical_Factor_Investing.ipynb
├── 06_Solution_Manual.ipynb
├── custom.css               ← Styling for the Jupyter Book
├── myst.yml                 ← Jupyter Book v2 / MyST config + TOC
├── runtime.txt              ← Python version pin for hosted runtimes
├── .github/workflows/
│   └── deploy-book.yml      ← GitHub Actions: build + deploy to Pages
├── requirements.txt         ← Runtime deps (numpy, pandas, statsmodels, …)
├── requirements-book.txt    ← Book build deps (jupyter-book v2)
├── .gitignore
└── README.md
```

## Data Sources

- **Fama-French factors** (US and international): Downloaded at runtime from [Kenneth French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
- **ETF prices**: Downloaded at runtime via [yfinance](https://github.com/ranaroussi/yfinance)
  - *Notebook 3*: SPY, IWN, VTV (US large-cap, small-cap value, large-cap value)
  - *Notebook 5*: AVWS, AVWC, AVEM, IWMO (Avantis UCITS + iShares Momentum, Xetra-listed)

No data files are committed to the repo — everything is fetched when the notebooks execute.

## License

This educational material is provided as-is for learning purposes.
