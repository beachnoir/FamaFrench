# Empirical Asset Pricing: From Statistics to Factor ETFs

Why do two diversified equity funds earn different returns? Is one holding different risks, selecting different kinds of companies, or simply experiencing a favourable period? And how much evidence would we need before calling the difference persistent?

This book develops the mathematics needed to ask those questions carefully. We start with sampling uncertainty, derive regression and robust standard errors, and then apply them to Fama–French factor models. The final chapter connects that research to **Avantis UCITS ETFs**: how a manager can use valuation and profitability information to construct a diversified portfolio, and what return data reveal about the resulting exposures.

## The question that connects the chapters

A factor regression writes a fund's excess return as

$$R_{i,t}-R_{f,t}=\alpha_i+\boldsymbol\beta_i^\top\mathbf f_t+\epsilon_{i,t}.$$

Here, $\mathbf f_t$ contains observed factor returns, $\boldsymbol\beta_i$ measures the fund's sensitivities, $\alpha_i$ is its average return beyond this specification, and $\epsilon_{i,t}$ is the remaining variation. Every part raises a question: how are factors constructed, how are coefficients estimated, what uncertainty surrounds them, and how do these statistical objects relate to an investable fund?

By the end, you should be able to derive the estimator, read its uncertainty, explain why a fund might tilt toward particular companies, and judge what evidence supports its investment thesis.

## A path through the material

| Step | Question | What you will learn to do |
|---|---|---|
| [1. Statistical foundations](01_Statistical_Foundations.ipynb) | How much can we infer from a noisy sample? | Derive OLS and its covariance, calculate confidence intervals, and understand HC and HAC estimators. |
| [2. Financial time series](02_Time_Series_Foundations.ipynb) | What changes when observations arrive through time? | Work with returns, investigate serial dependence and volatility clustering, and distinguish diagnostics from assumptions. |
| [3. The three-factor model](03_Fama_French_3Factor.ipynb) | What do market, size and value explain? | Construct the factors conceptually, estimate ETF exposures, and distinguish fit, alpha and a priced premium. |
| [4. Beyond three factors](04_Advanced_Factor_Models.ipynb) | Why consider profitability, investment and momentum? | Connect valuation theory to empirical models, compare specifications, and assess replication and implementation evidence. |
| [5. From factor research to Avantis ETFs](05_Practical_Factor_Investing.ipynb) | How does research become a portfolio? | Translate characteristics into portfolio choices, investigate actual fund exposures, and understand diversification and estimation risk. |

The [solution manual](06_Solution_Manual.ipynb) is a companion to the exercises, best consulted after an attempt. [Data and methods](data-and-methods.md) explains sample coverage, return conventions and sources.

## How to study the book

The intended background is introductory probability and statistics, elementary linear algebra, and some familiarity with Python. The early derivations use small datasets you can check by hand. Later examples use the same ideas on market data; the saved outputs let you read without installing anything.

For a first pass through Chapter 1, focus on the classical CLT, OLS and the sandwich covariance formula. The more general CLTs explain the assumptions needed for dependent observations and are useful on a second pass alongside Chapter 2. Readers already comfortable with econometrics can begin with Chapter 3 and return to the derivations when needed.

## What makes the ETF examples useful?

A company's **characteristics**, a research **factor portfolio**, a fund's estimated **loading**, and its expected **premium** are related but distinct. A lower valuation is a characteristic; HML is a particular long–short return series; an HML loading is a coefficient estimated from returns. None is itself a guarantee of future outperformance.

Avantis is a useful case study because its stated approach combines prices and company financial information with portfolio and trading decisions. That lets us trace a concrete path from valuation arguments to implementation and then back to evidence. We study that path rather than treating a provider's name as evidence that a strategy works. [Avantis investment approach](https://www.avantisinvestors.com/avantis-about-us/en-us/how-we-invest/).

**Data edition: 31 October 2026.** Factor regressions end in September 2026, the latest released factor month in this edition; price histories extend through 30 October. The mathematical lessons do not depend on a particular market outcome, and each empirical conclusion is tied to its stated sample.

[Begin Chapter 1 →](01_Statistical_Foundations.ipynb)
