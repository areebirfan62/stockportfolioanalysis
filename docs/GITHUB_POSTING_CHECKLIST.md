# GitHub Posting Checklist

## Post These

- `README.md`
- `reports/final_dashboard.png`
- `reports/model1_results.png`
- `reports/ma_signals.png`
- `reports/xgboost_analysis.png`
- `data/latest_portfolio_holdings.csv`
- `data/portfolio_daily_summary.csv`
- `data/portfolio_forward_log.csv`
- `docs/MODEL_CARD.md`
- your final cleaned notebook exported from Colab into `notebooks/`

## Optional

- `reports/womack_frontier.png`, as a classroom foundation/model lineage visual
- a short presentation PDF or slide deck
- a live dashboard link if deployed with Streamlit or GitHub Pages

## Do Not Post

- temporary patch scripts
- local cache folders
- API keys, credentials, or private drive paths
- huge raw download files unless needed for reproducibility
- notebook backups with old broken logic

## Best README Order

1. One-sentence project pitch
2. Final dashboard image
3. Latest performance snapshot
4. Latest holdings table
5. Model constraints
6. Methodology
7. Validation results
8. How to refresh/reproduce
9. Limitations/disclaimer

## Highest-Impact Additions

- Use the included `.github/workflows/daily_portfolio_refresh.yml` daily automation workflow.
- Convert notebook code into `src/portfolio_pipeline.py`.
- Add `tests/test_constraints.py`.
- Add a Streamlit dashboard.
- Add transaction costs and turnover statistics.
- Add benchmark comparison against SPY.
- Add drawdown, volatility, Sharpe, and Calmar tables.
