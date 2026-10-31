"""Fetch the shared public-data snapshot before executing notebooks."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis_utils import AS_OF, ROOT, coverage, load_french, load_prices, load_beta_portfolios, write_manifest

FILES = [
    "F-F_Research_Data_Factors_CSV.zip", "F-F_Research_Data_5_Factors_2x3_CSV.zip",
    "F-F_Momentum_Factor_CSV.zip", "F-F_ST_Reversal_Factor_CSV.zip",
    "F-F_LT_Reversal_Factor_CSV.zip", "Developed_5_Factors_CSV.zip",
    "Developed_Mom_Factor_CSV.zip", "Emerging_5_Factors_CSV.zip",
]

if __name__ == "__main__":
    for filename in FILES:
        coverage(filename, load_french(filename))
    coverage("Beta deciles (VW)", load_beta_portfolios())
    for ticker in ["SPY", "IWN", "VTV", "IWM", "AAPL"]:
        coverage(ticker, load_prices(ticker))
    for ticker in ["AVWS.DE", "AVWC.DE", "AVEM.DE", "IS3R.DE", "EURUSD=X"]:
        coverage(ticker, load_prices(ticker, start="2014-09-01"))
    (ROOT / "reports").mkdir(exist_ok=True)
    write_manifest(ROOT / "reports" / f"data_manifest_{AS_OF:%Y-%m-%d}.json")
