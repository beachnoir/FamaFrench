"""Shared, auditable data handling for the factor-investing notebooks.

Returns are decimals unless ``percent=True`` is requested. French monthly
observations use month-start labels; prices always retain their trading dates.
The as-of cutoff limits observations, not the vintage of revised source data.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent
AS_OF = pd.Timestamp(os.environ.get("ANALYSIS_AS_OF", datetime.now(ZoneInfo("Europe/Amsterdam")).date().isoformat())).normalize()
END_EXCLUSIVE = (AS_OF + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
CACHE = ROOT / "data" / "cache" / AS_OF.strftime("%Y-%m-%d")
FRENCH_BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"


def _cache_paths(key, suffix):
    CACHE.mkdir(parents=True, exist_ok=True)
    stem = hashlib.sha256(key.encode()).hexdigest()[:20]
    return CACHE / (stem + suffix), CACHE / (stem + ".json")


def _record(path, meta_path, source, frame, **extra):
    metadata = dict(source=source, as_of=str(AS_OF.date()),
                    retrieved_at=datetime.now(ZoneInfo("UTC")).isoformat(),
                    first_observation=str(frame.index.min().date()),
                    last_observation=str(frame.index.max().date()), rows=len(frame),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(), **extra)
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n")


def _verify_cache(path, meta_path):
    if not meta_path.exists():
        raise ValueError(f"Snapshot metadata missing for {path.name}")
    metadata = json.loads(meta_path.read_text())
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != metadata.get("sha256"):
        raise ValueError(f"Snapshot checksum mismatch for {path.name}")


def parse_french_zip(payload, frequency="monthly"):
    """Read only the first monthly/daily table, never mix VW/EW/annual tables.

    Locate date rows rather than hard-coded header offsets. Missing-value
    sentinels are masked before percent-to-decimal conversion by the caller.
    """
    if frequency not in {"monthly", "daily"}:
        raise ValueError("frequency must be monthly or daily")
    pattern = re.compile(r"^\d{" + ("6" if frequency == "monthly" else "8") + r"}$")
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith(".csv")]
        if len(names) != 1:
            raise ValueError(f"Expected one CSV, found {names}")
        rows = list(csv.reader(io.StringIO(archive.read(names[0]).decode("utf-8-sig"))))
    start = next((i for i, row in enumerate(rows) if row and pattern.fullmatch(row[0].strip())), None)
    if start is None:
        raise ValueError(f"No {frequency} observations in French archive")
    header = next((r for r in reversed(rows[:start]) if len(r) == len(rows[start]) and not r[0].strip()), None)
    if header is None:
        raise ValueError("Missing return-table header")
    block = []
    for row in rows[start:]:
        if not row or not pattern.fullmatch(row[0].strip()):
            break
        if len(row) != len(header):
            raise ValueError("Unexpected number of columns in French table")
        block.append(row)
    frame = pd.DataFrame(block, columns=[h.strip() for h in header])
    dates = pd.to_datetime(frame.pop(frame.columns[0]).str.strip(), format="%Y%m" if frequency == "monthly" else "%Y%m%d")
    frame.index = pd.DatetimeIndex(dates, name="Date")
    frame = frame.apply(pd.to_numeric, errors="raise").replace([-99.99, -999.0], np.nan)
    if frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        raise ValueError("French dates must be unique and increasing")
    if frequency == "monthly" and len(frame) > 1:
        if not np.all(np.diff(frame.index.to_period("M").asi8) == 1):
            raise ValueError("Missing month in French table")
    return frame


def load_french(filename, *, frequency="monthly", percent=False, start=None):
    url = filename if filename.startswith("https://") else FRENCH_BASE + filename
    path, meta = _cache_paths(url + frequency, ".zip")
    if not path.exists():
        if os.environ.get("ANALYSIS_OFFLINE") == "1":
            raise FileNotFoundError(f"Offline snapshot missing: {url}")
        request = urllib.request.Request(url, headers={"User-Agent": "FactorInvestingTutorial/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        frame = parse_french_zip(payload, frequency)
        path.write_bytes(payload)
        _record(path, meta, url, frame, frequency=frequency, raw_units="percent")
    _verify_cache(path, meta)
    frame = parse_french_zip(path.read_bytes(), frequency)
    # Exclude unfinished monthly observations even if a provider supplies one.
    limit = AS_OF if frequency == "daily" else last_complete_month().to_timestamp()
    frame = frame.loc[start:limit].copy()
    if frame.empty:
        raise ValueError(f"No usable observations for {filename}")
    return frame if percent else frame / 100


def last_complete_month():
    month = AS_OF.to_period("M")
    return month if AS_OF.is_month_end else month - 1


def load_prices(ticker, start="1999-12-01"):
    """Explicit adjusted Close; cache the exact observations used for this run."""
    key = f"yfinance:{ticker}:{start}:{END_EXCLUSIVE}:auto_adjust=True:repair=False"
    path, meta = _cache_paths(key, ".csv")
    if path.exists():
        _verify_cache(path, meta)
        series = pd.read_csv(path, index_col=0, parse_dates=True)["Close"]
    else:
        if os.environ.get("ANALYSIS_OFFLINE") == "1":
            raise FileNotFoundError(f"Offline snapshot missing: {ticker}")
        import yfinance as yf
        raw = yf.download(ticker, start=start, end=END_EXCLUSIVE, auto_adjust=True,
                          repair=False, progress=False, threads=False, timeout=45)
        if raw.empty:
            raise RuntimeError(f"No Yahoo prices for {ticker}; refusing to substitute or reuse stale results")
        close = raw["Close"]
        series = close[ticker] if isinstance(close, pd.DataFrame) else close
        series.index = pd.DatetimeIndex(series.index).tz_localize(None).normalize()
        series = series.dropna().sort_index().rename("Close")
        series = series.loc[:AS_OF]
        if series.empty or series.index.has_duplicates or not np.isfinite(series).all() or (series <= 0).any():
            raise ValueError(f"Invalid adjusted prices: {ticker}")
        series.to_csv(path, index_label="Date")
        _record(path, meta, key, series, ticker=ticker, adjusted=True, repair=False)
    if series.empty or series.index.has_duplicates or not series.index.is_monotonic_increasing or not np.isfinite(series).all() or (series <= 0).any() or (series.index > AS_OF).any():
        raise ValueError(f"Invalid cached prices: {ticker}")
    return series.rename(ticker)


def monthly_returns(prices):
    """Calendar-month total returns from consecutive adjusted month-end closes.

    Requires a prior month's close (so launch months are excluded). No filling
    across missing months. A final price more than four calendar days before
    month-end is treated as an incomplete month, allowing ordinary holidays.
    This is a boundary check, not a full exchange-calendar completeness audit.
    """
    prices = prices.sort_index()
    if prices.index.has_duplicates:
        raise ValueError("Duplicate price dates")
    closes = prices.resample("ME").last()
    last_dates = pd.Series(prices.index, index=prices.index).resample("ME").max()
    stale = (pd.Series(closes.index, index=closes.index) - last_dates).dt.days > 4
    closes = closes.mask(stale)
    returns = closes.pct_change(fill_method=None)
    returns.index = returns.index.to_period("M").to_timestamp()
    return returns.loc[:last_complete_month().to_timestamp()].dropna()


def usd_prices(prices_eur, eurusd):
    """Convert price levels before returns, preserving the first return interval."""
    fx = eurusd.reindex(prices_eur.index, method="ffill", tolerance=pd.Timedelta(days=4))
    if fx.isna().any():
        raise ValueError("FX data missing or more than four days stale")
    return prices_eur * fx


def nw_lags(n):
    """Common sample-size bandwidth heuristic; not Andrews' plug-in selector."""
    return min(n - 1, int(np.floor(4 * (n / 100) ** (2 / 9))))


def fit_hac(y, x, lags=None):
    """OLS with Bartlett HAC, n/(n-k) correction and explicit normal inference."""
    if isinstance(y, (pd.Series, pd.DataFrame)) and isinstance(x, (pd.Series, pd.DataFrame)):
        if not y.index.equals(x.index):
            raise ValueError("Response and factors must have identical date indexes")
    y, x = np.asarray(y, dtype=float), np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    design = sm.add_constant(x, has_constant="add")
    if len(y) != len(design) or not np.isfinite(y).all() or not np.isfinite(design).all():
        raise ValueError("Regression inputs must be finite and aligned")
    if len(y) <= design.shape[1] or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("Insufficient observations or rank-deficient design")
    lag = nw_lags(len(y)) if lags is None else lags
    if not isinstance(lag, (int, np.integer)) or not 0 <= lag < len(y):
        raise ValueError("HAC lags must be an integer between 0 and n-1")
    return sm.OLS(y, design).fit(cov_type="HAC", cov_kwds={"maxlags": lag, "use_correction": True}, use_t=False)


def mean_hac(series):
    values = np.asarray(series, dtype=float)
    return sm.OLS(values, np.ones((len(values), 1))).fit(
        cov_type="HAC", cov_kwds={"maxlags": nw_lags(len(values)), "use_correction": True}, use_t=False)


def load_beta_portfolios():
    frame = load_french("Portfolios_Formed_on_BETA_CSV.zip")
    # French supplies quintiles and deciles in the same VW table.
    lo, hi = frame.columns.get_loc("Lo 10"), frame.columns.get_loc("Hi 10")
    deciles = frame.iloc[:, lo:hi + 1].copy()
    if deciles.shape[1] != 10:
        raise ValueError("Expected ten value-weighted beta deciles")
    deciles.columns = [f"D{i}" for i in range(1, 11)]
    return deciles.dropna()


def coverage(label, data):
    print(f"{label}: {len(data):,} observations, {data.index.min():%Y-%m-%d} to {data.index.max():%Y-%m-%d}; as of {AS_OF:%Y-%m-%d}")


def write_manifest(destination):
    records = [json.loads(p.read_text()) for p in sorted(CACHE.glob("*.json"))]
    Path(destination).write_text(json.dumps({"as_of": str(AS_OF.date()), "sources": records}, indent=2) + "\n")
