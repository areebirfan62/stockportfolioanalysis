from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
README = ROOT / "README.md"
REPORTS.mkdir(exist_ok=True)

latest = pd.read_csv(DATA / "latest_portfolio_holdings.csv")
daily = pd.read_csv(DATA / "portfolio_daily_summary.csv")

latest_date = str(latest["Date"].max())
last_daily = daily.sort_values("Date").iloc[-1]

portfolio_value = float(last_daily["Portfolio_Value"])
cumulative_return = float(last_daily["Cumulative_Return"])
wealth_gain = float(last_daily["Wealth_Gain_$"])
avg_daily_return = float(daily["Portfolio_Return"].mean())

holdings_table = latest[["Stock", "Sector", "Weight", "Holding_Value"]].copy()
holdings_table["Weight"] = holdings_table["Weight"].astype(float).map(lambda x: f"{x:.2%}")
holdings_table["Holding_Value"] = holdings_table["Holding_Value"].astype(float).map(lambda x: f"${x:,.2f}")
holdings_table = holdings_table.rename(columns={"Holding_Value": "Holding Value"})


def markdown_table(df: pd.DataFrame) -> str:
    header = "| " + " | ".join(df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(df.columns)) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in df.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *rows])


holdings_markdown = markdown_table(holdings_table)

summary = f"""# Latest Portfolio Summary

Latest refresh date: **{latest_date}**

| Metric | Value |
|---|---:|
| Portfolio value | ${portfolio_value:,.2f} |
| Wealth gain | ${wealth_gain:,.2f} |
| Cumulative return | {cumulative_return:.2%} |
| Average daily return | {avg_daily_return:.2%} |
| Holdings | {len(latest)} |
| Sector rule | 2 stocks from each of 5 sectors |
| Weight bounds | 5% minimum, 50% maximum |

## Latest Holdings

{holdings_markdown}

## Dashboard

![Final Dashboard](final_dashboard.png)
"""

(REPORTS / "latest_summary.md").write_text(summary, encoding="utf-8")
print("Rendered reports/latest_summary.md")

readme_snapshot = f"""## Current Forward-Test Snapshot

Latest generated date: **{latest_date}**

| Metric | Value |
|---|---:|
| Starting wealth | $100,000 |
| Latest portfolio value | ${portfolio_value:,.2f} |
| Wealth gain | ${wealth_gain:,.2f} |
| Cumulative return | {cumulative_return:.2%} |
| Average daily return | {avg_daily_return:.2%} |
| Holdings | {len(latest)} stocks |
| Sector rule | 2 stocks from each of 5 sectors |
| Weight bounds | 5% minimum, 50% maximum per selected stock |

## Latest Portfolio Allocation

{holdings_markdown}
"""

if README.exists():
    readme_text = README.read_text(encoding="utf-8")
    updated_readme = re.sub(
        r"## Current Forward-Test Snapshot\n.*?(?=\n## Interactive Dashboard)",
        readme_snapshot.rstrip() + "\n",
        readme_text,
        flags=re.S,
    )
    if updated_readme == readme_text:
        raise RuntimeError("Could not find README snapshot section to update.")
    README.write_text(updated_readme, encoding="utf-8")
    print("Updated README.md current snapshot")
