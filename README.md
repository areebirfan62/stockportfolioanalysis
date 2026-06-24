# S&P 500 Portfolio Optimizer

[![Daily Portfolio Refresh](https://github.com/areebirfan62/stockportfolioanalysis/actions/workflows/daily_portfolio_refresh.yml/badge.svg)](https://github.com/areebirfan62/stockportfolioanalysis/actions/workflows/daily_portfolio_refresh.yml)

This project builds a daily active portfolio allocation system for OPIM 5641 Business Decision Modeling. The model uses Modern Portfolio Theory, integer selection variables, sector diversification rules, moving-average signals, and an XGBoost overlay to decide which 10 stocks to hold and how much capital to allocate to each position.

[Interactive Dashboard](https://areebirfan62.github.io/stockportfolioanalysis/) | [Powered by Colab](https://colab.research.google.com/drive/1Jc1ZjkHwNA_sHCkSf6gUSaJnZ2IuZp2w#scrollTo=part0_header) | [Summary Statistics](reports/latest_summary.md) | [Model Card](docs/MODEL_CARD.md)

## View Results

The main results are published in the interactive dashboard, not in the repository file list. Use the dashboard link above to review the latest portfolio value, summary statistics, daily returns, sector allocation, and current holdings. If GitHub Pages is still being configured, the same dashboard source is stored in `docs/index.html`.

## Executive Summary

The portfolio is evaluated as a forward test beginning on April 21, 2026. Each trading day, the workbook refreshes market data, retrains the allocation logic using only prior data, selects a constrained 10-stock portfolio, and records the next-day performance. The result is an iterative trading model rather than a one-time static backtest.

The modeling workflow is powered by Google Colab for transparent notebook execution and GitHub Actions for daily publication. Colab remains the primary workbook environment, while this repository publishes the refreshed data files, validation outputs, and interactive dashboard.

## Current Forward-Test Snapshot

Latest generated date: **2026-06-24**

| Metric | Value |
|---|---:|
| Starting wealth | $100,000 |
| Latest portfolio value | $122,338.29 |
| Wealth gain | $22,338.29 |
| Cumulative return | 22.40% |
| Average daily return | 0.46% |
| Holdings | 10 stocks |
| Sector rule | 2 stocks from each of 5 sectors |
| Weight bounds | 5% minimum, 50% maximum per selected stock |

## Latest Portfolio Allocation

| Stock | Sector | Weight | Holding Value |
| --- | --- | --- | --- |
| MS | Financials | 20.93% | $25,606.91 |
| KO | ConsumerStaples | 20.24% | $24,763.96 |
| MO | ConsumerStaples | 15.98% | $19,543.73 |
| CVS | Healthcare | 11.94% | $14,609.09 |
| MU | Technology | 5.91% | $7,230.02 |
| INTC | Technology | 5.00% | $6,116.91 |
| LLY | Healthcare | 5.00% | $6,116.91 |
| GS | Financials | 5.00% | $6,116.91 |
| WMB | Energy | 5.00% | $6,116.91 |
| TRGP | Energy | 5.00% | $6,116.91 |

## Interactive Dashboard

The project dashboard is published from `docs/index.html` through GitHub Pages. It refreshes from the same CSV outputs produced by the workbook and includes:

- Summary statistics button for the latest forward-test metrics
- Forward-test portfolio value
- Daily portfolio returns
- Latest 10-stock allocation
- Sector mix pie chart
- Stock-level return contribution
- Allocation history by stock
- Current holdings table

Static notebook figures are retained in `reports/` as supporting evidence from the modeling workflow.

## Modeling Approach

The optimizer combines continuous allocation decisions with binary stock-selection decisions:

| Component | Role |
|---|---|
| `X[k]` | Portfolio weight assigned to stock `k` |
| `Y[k]` | Binary decision for whether stock `k` is selected |
| Budget constraint | All portfolio weights sum to 100% |
| Linking constraints | Selected stocks must receive at least 5% and no more than 50% |
| Cardinality constraint | Exactly 10 stocks are selected each day |
| Sector constraint | Exactly 2 stocks are selected from each of 5 sectors |
| Objective | Select the maximum Sharpe allocation along the efficient frontier |

The forward-test loop uses a sliding historical window so that each allocation is trained only on information available before the tested trading day.

## Model Comparison

The notebook includes three complementary modeling layers:

| Model | Purpose |
|---|---|
| Integer MPT optimizer | Core constrained allocation engine |
| Moving-average signal screen | Technical momentum comparison and signal validation |
| XGBoost return overlay | Experimental machine-learning estimate of next-day returns |

The final dashboard emphasizes the daily forward-test portfolio because it is the most direct evidence of how the trading process behaves over time.

## Automation

GitHub Actions runs the refresh workflow Monday through Friday at **3:45 PM Eastern during daylight saving time**.

Workflow steps:

1. Execute the portfolio notebook.
2. Refresh Yahoo Finance data.
3. Rebuild the forward-test allocations.
4. Validate the hard portfolio constraints.
5. Regenerate summary tables, charts, and the interactive dashboard.
6. Commit the updated outputs back to the repository.
7. Deploy the `docs/` dashboard through GitHub Pages.

GitHub cron uses UTC. The current schedule is `45 19 * * 1-5`, which equals 3:45 PM Eastern during daylight saving time. When daylight saving time ends, the workflow should be changed to `45 20 * * 1-5` to keep the same Eastern time.

<details>
<summary><strong>Repository Contents</strong></summary>

```text
.
+-- data/
|   +-- latest_portfolio_holdings.csv
|   +-- portfolio_daily_summary.csv
|   +-- portfolio_forward_log.csv
+-- docs/
|   +-- index.html
|   +-- MODEL_CARD.md
|   +-- PROJECT_GUIDE.md
+-- reports/
|   +-- final_dashboard.png
|   +-- latest_summary.md
|   +-- ma_signals.png
|   +-- model1_results.png
|   +-- womack_frontier.png
|   +-- xgboost_analysis.png
+-- notebooks/
|   +-- BDM_final_portfolio_notebook.ipynb
|   +-- BDM_final_portfolio_notebook_executed.ipynb
+-- scripts/
|   +-- build_dashboard.py
|   +-- collect_outputs.py
|   +-- render_latest_summary.py
|   +-- validate_outputs.py
+-- .github/workflows/daily_portfolio_refresh.yml
+-- requirements.txt
+-- README.md
```

</details>

## Reproducing the Project

To refresh the project in Colab, open the workbook and run from the real-data pipeline section through the final reporting section. To run the repository automation locally:

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/BDM_final_portfolio_notebook.ipynb --output BDM_final_portfolio_notebook_executed.ipynb --output-dir notebooks
python scripts/collect_outputs.py
python scripts/validate_outputs.py
python scripts/render_latest_summary.py
python scripts/build_dashboard.py
```

## Disclaimer

This project is for academic modeling and presentation purposes only. It is not financial advice, and historical or forward-tested performance does not guarantee future results.
