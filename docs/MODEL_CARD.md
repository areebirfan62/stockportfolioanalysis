# Model Card

## Objective

Build a daily portfolio allocation model that selects 10 stocks and allocates capital to maximize return per unit of risk while obeying realistic trading constraints.

## Data

- Source: Yahoo Finance daily adjusted close prices
- Universe: 100 large-cap stocks across 5 sectors
- Selection pool: top 4 stocks per sector by historical Sharpe ratio, giving 20 candidates
- Forward-test start: 2026-04-21

## Decision Variables

- `X[k]`: continuous allocation weight for stock `k`
- `Y[k]`: binary selection variable for stock `k`

## Hard Constraints

- Budget: all selected weights sum to 1
- Stock count: exactly 10 selected stocks
- Minimum allocation: 5% for any selected stock
- Maximum allocation: 50% for any selected stock
- Sector balance: exactly 2 selected stocks from each of the 5 sectors

## Models

### Model 1: Integer MPT Optimizer

Uses historical mean returns and covariance over a sliding lookback window. The model traces the efficient frontier by sweeping target returns and automatically chooses the portfolio with the highest Sharpe ratio.

### Model 2: XGBoost + Moving-Average Overlay

Uses engineered technical features to predict next-day returns. Moving-average signals are used as a momentum screen, but the model relaxes the screen when needed to preserve the required 2-stocks-per-sector rule.

## Validation

The notebook validates every allocation window for:

- total weight equals 1
- exactly 10 stocks selected
- no selected stock below 5%
- no selected stock above 50%
- exactly 2 stocks from each sector

Both Model 1 and Model 2 passed these hard constraints in the latest run.

## Reporting

The repository publishes an interactive dashboard from `docs/index.html`. The dashboard is generated from the latest CSV outputs and summarizes portfolio value, daily returns, sector allocation, stock-level weights, return contribution, and allocation history.

## Known Limitations

- Yahoo Finance ticker availability can change over time.
- Transaction costs and taxes are not yet included.
- The current forward-test window is short, so annualized metrics can look exaggerated.
- XGBoost predictions should be interpreted as an experimental alpha overlay, not a trading guarantee.

## Recommended Extensions

- Add transaction costs and turnover controls.
- Add rolling out-of-sample walk-forward validation over a longer history.
- Add unit tests for allocation constraints and data pipeline validation.
