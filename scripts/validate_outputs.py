from pathlib import Path
import math

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

latest_path = DATA / "latest_portfolio_holdings.csv"
daily_path = DATA / "portfolio_daily_summary.csv"
forward_path = DATA / "portfolio_forward_log.csv"

for path in [latest_path, daily_path, forward_path]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required output: {path}")

latest = pd.read_csv(latest_path)
daily = pd.read_csv(daily_path)
forward = pd.read_csv(forward_path)

if latest.empty:
    raise ValueError("latest_portfolio_holdings.csv is empty")
if daily.empty:
    raise ValueError("portfolio_daily_summary.csv is empty")
if forward.empty:
    raise ValueError("portfolio_forward_log.csv is empty")

required_columns = {"Date", "Stock", "Sector", "Weight"}
missing = required_columns - set(latest.columns)
if missing:
    raise ValueError(f"latest_portfolio_holdings.csv is missing columns: {sorted(missing)}")

if len(latest) != 10:
    raise ValueError(f"Expected exactly 10 latest holdings, found {len(latest)}")

weight_sum = latest["Weight"].astype(float).sum()
if not math.isclose(weight_sum, 1.0, rel_tol=0, abs_tol=1e-5):
    raise ValueError(f"Latest weights must sum to 1.0; got {weight_sum}")

if (latest["Weight"].astype(float) < 0.05 - 1e-5).any():
    raise ValueError("At least one selected stock is below the 5% minimum allocation")

if (latest["Weight"].astype(float) > 0.50 + 1e-5).any():
    raise ValueError("At least one selected stock is above the 50% maximum allocation")

sector_counts = latest["Sector"].value_counts().to_dict()
expected_sectors = {"Technology", "Energy", "Healthcare", "Financials", "ConsumerStaples"}
bad = {sector: sector_counts.get(sector, 0) for sector in expected_sectors if sector_counts.get(sector, 0) != 2}
if bad:
    raise ValueError(f"Sector rule failed. Expected 2 per sector; got {bad}")

print("Portfolio output validation passed.")
print(f"Latest date: {latest['Date'].max()}")
print(f"Latest holdings: {len(latest)}")
print(f"Weight sum: {weight_sum:.6f}")
print("Sector counts:")
print(latest["Sector"].value_counts().sort_index().to_string())
