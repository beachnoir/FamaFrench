# Empirical Asset Pricing: From Statistics to Factor ETFs

An open educational book about the mathematics and statistics behind empirical asset pricing, with worked Fama–French regressions and a case study of Avantis UCITS ETFs.

**[Read the book](https://beachnoir.github.io/FamaFrench/)** or start with the [introduction](index.md) in this repository.

The course develops sampling uncertainty and OLS, studies financial time series, constructs and estimates factor models, and then connects valuation and profitability research to the design and analysis of real ETFs. Python notebooks include executed examples; a separate solution manual covers the 18 exercises in Chapters 1–4.

| Part | Chapters |
|---|---|
| Statistical foundations | [1. Inference and regression](01_Statistical_Foundations.ipynb), [2. Financial time series](02_Time_Series_Foundations.ipynb) |
| Empirical asset-pricing models | [3. Fama–French three-factor model](03_Fama_French_3Factor.ipynb), [4. Profitability, investment and other factors](04_Advanced_Factor_Models.ipynb) |
| Research in practice | [5. From factor research to Avantis ETFs](05_Practical_Factor_Investing.ipynb) |
| Reference | [Worked solutions](06_Solution_Manual.ipynb), [Data and methods](data-and-methods.md) |

The displayed market-data edition is dated **31 October 2026**, with released factors through September 2026 and adjusted prices through 30 October 2026. Samples and limitations are explained where results are used.

For installation, execution, tests and deployment, see [DEVELOPMENT.md](DEVELOPMENT.md). The website renders executed notebook outputs. Publishing to `main` runs validation, builds the book, and deploys only if those steps succeed.
