from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
STARTING_WEALTH = 100_000
RISK_FREE_DAILY = 0.0001
COLAB_URL = "https://colab.research.google.com/drive/1Jc1ZjkHwNA_sHCkSf6gUSaJnZ2IuZp2w#scrollTo=part0_header"
REPO_URL = "https://github.com/areebirfan62/stockportfolioanalysis"

COLORS = {
    "background": "#08111f",
    "panel": "#111b2e",
    "panel_2": "#17243a",
    "border": "#2d3b55",
    "text": "#edf4ff",
    "muted": "#9fb0c8",
    "cyan": "#2dd4ff",
    "green": "#6ee7a8",
    "red": "#ff6b7a",
    "gold": "#ffd166",
    "purple": "#b794f4",
}

SECTOR_COLORS = {
    "Technology": "#2dd4ff",
    "Energy": "#ffd166",
    "ConsumerStaples": "#6ee7a8",
    "Financials": "#b794f4",
    "Healthcare": "#ff8fab",
}


def money(value: float) -> str:
    return f"${value:,.2f}"


def pct(value: float) -> str:
    return f"{value:.2%}"


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = pd.read_csv(DATA_DIR / "portfolio_daily_summary.csv", parse_dates=["Date"])
    latest = pd.read_csv(DATA_DIR / "latest_portfolio_holdings.csv", parse_dates=["Date"])
    forward = pd.read_csv(DATA_DIR / "portfolio_forward_log.csv", parse_dates=["Date"])

    summary = summary.sort_values("Date").reset_index(drop=True)
    latest = latest.sort_values("Weight", ascending=False).reset_index(drop=True)
    forward = forward.sort_values(["Date", "Weight"], ascending=[True, False]).reset_index(drop=True)
    return summary, latest, forward


def plotly_layout(fig: go.Figure, title: str, height: int = 420) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        height=height,
        paper_bgcolor=COLORS["panel"],
        plot_bgcolor=COLORS["panel"],
        font={"color": COLORS["text"], "family": "Inter, Segoe UI, Arial, sans-serif"},
        margin={"l": 55, "r": 30, "t": 70, "b": 55},
        legend={"orientation": "h", "y": 1.08, "x": 0.02},
        hovermode="x unified",
    )
    fig.update_xaxes(gridcolor="#26344e", zerolinecolor="#26344e")
    fig.update_yaxes(gridcolor="#26344e", zerolinecolor="#26344e")
    return fig


def build_value_chart(summary: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=summary["Date"],
            y=summary["Portfolio_Value"],
            mode="lines+markers",
            name="Portfolio value",
            line={"color": COLORS["cyan"], "width": 3},
            marker={"size": 7},
            fill="tozeroy",
            fillcolor="rgba(45, 212, 255, 0.10)",
            hovertemplate="%{x|%b %d, %Y}<br>Value: $%{y:,.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=summary["Date"],
            y=[STARTING_WEALTH] * len(summary),
            mode="lines",
            name="Starting capital",
            line={"color": COLORS["muted"], "dash": "dash", "width": 2},
            hovertemplate="Starting capital: $%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    return plotly_layout(fig, "Forward-Test Portfolio Value", 430)


def build_return_chart(summary: pd.DataFrame) -> go.Figure:
    colors = [COLORS["green"] if r >= 0 else COLORS["red"] for r in summary["Portfolio_Return"]]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=summary["Date"],
            y=summary["Portfolio_Return"],
            marker_color=colors,
            name="Daily return",
            hovertemplate="%{x|%b %d, %Y}<br>Return: %{y:.2%}<extra></extra>",
        )
    )
    fig.add_hline(y=0, line_color=COLORS["muted"], line_width=1)
    fig.update_yaxes(tickformat=".1%")
    return plotly_layout(fig, "Daily Portfolio Return", 360)


def build_allocation_chart(latest: pd.DataFrame) -> go.Figure:
    latest = latest.sort_values("Weight")
    marker_colors = [SECTOR_COLORS.get(str(sector), COLORS["cyan"]) for sector in latest["Sector"]]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=latest["Weight"],
            y=latest["Stock"],
            orientation="h",
            marker_color=marker_colors,
            customdata=latest[["Sector", "Holding_Value"]],
            hovertemplate=(
                "%{y}<br>Sector: %{customdata[0]}"
                "<br>Weight: %{x:.2%}<br>Holding value: $%{customdata[1]:,.2f}<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(tickformat=".0%")
    return plotly_layout(fig, "Latest 10-Stock Allocation", 430)


def build_sector_chart(latest: pd.DataFrame) -> go.Figure:
    sector_mix = latest.groupby("Sector", as_index=False)["Weight"].sum().sort_values("Weight", ascending=False)
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=sector_mix["Sector"],
            values=sector_mix["Weight"],
            hole=0.55,
            marker={"colors": [SECTOR_COLORS.get(str(s), COLORS["cyan"]) for s in sector_mix["Sector"]]},
            textinfo="label+percent",
            hovertemplate="%{label}<br>Portfolio weight: %{value:.2%}<extra></extra>",
        )
    )
    return plotly_layout(fig, "Sector Mix", 360)


def build_contribution_chart(latest: pd.DataFrame) -> go.Figure:
    latest = latest.sort_values("Weighted_Return")
    colors = [COLORS["green"] if r >= 0 else COLORS["red"] for r in latest["Weighted_Return"]]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=latest["Weighted_Return"],
            y=latest["Stock"],
            orientation="h",
            marker_color=colors,
            customdata=latest[["Weight", "Stock_Return"]],
            hovertemplate=(
                "%{y}<br>Contribution: %{x:.2%}"
                "<br>Weight: %{customdata[0]:.2%}<br>Stock return: %{customdata[1]:.2%}<extra></extra>"
            ),
        )
    )
    fig.add_vline(x=0, line_color=COLORS["muted"], line_width=1)
    fig.update_xaxes(tickformat=".1%")
    return plotly_layout(fig, "Latest Daily Return Contribution", 430)


def build_heatmap(forward: pd.DataFrame) -> go.Figure:
    pivot = forward.pivot_table(index="Stock", columns="Date", values="Weight", aggfunc="sum").fillna(0)
    order = pivot.max(axis=1).sort_values(ascending=False).index
    pivot = pivot.loc[order]
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=[
                [0, "#0b1220"],
                [0.35, "#164e63"],
                [0.7, "#2dd4ff"],
                [1, "#ffd166"],
            ],
            colorbar={"tickformat": ".0%", "title": "Weight"},
            hovertemplate="%{y}<br>%{x|%b %d, %Y}<br>Weight: %{z:.2%}<extra></extra>",
        )
    )
    return plotly_layout(fig, "Allocation History by Stock", 520)


def build_holdings_table(latest: pd.DataFrame) -> str:
    rows = []
    for _, row in latest.sort_values("Weight", ascending=False).iterrows():
        rows.append(
            "<tr>"
            f"<td>{row['Stock']}</td>"
            f"<td>{row['Sector']}</td>"
            f"<td>{pct(safe_float(row['Weight']))}</td>"
            f"<td>{money(safe_float(row['Holding_Value']))}</td>"
            f"<td>{pct(safe_float(row['Stock_Return']))}</td>"
            f"<td>{pct(safe_float(row['Weighted_Return']))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def build_summary_stats_table(stats: dict[str, str]) -> str:
    rows = []
    for label, value in stats.items():
        rows.append(
            "<tr>"
            f"<td>{label}</td>"
            f"<td>{value}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def metric_card(label: str, value: str, detail: str = "") -> str:
    detail_html = f"<span>{detail}</span>" if detail else ""
    return f"""
    <article class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      {detail_html}
    </article>
    """


def render_dashboard(summary: pd.DataFrame, latest: pd.DataFrame, forward: pd.DataFrame) -> str:
    latest_row = summary.iloc[-1]
    latest_date = pd.Timestamp(latest_row["Date"])
    latest_value = safe_float(latest_row["Portfolio_Value"])
    wealth_gain = latest_value - STARTING_WEALTH
    cumulative_return = latest_value / STARTING_WEALTH - 1
    avg_daily_return = safe_float(summary["Portfolio_Return"].mean())
    daily_vol = safe_float(summary["Portfolio_Return"].std(ddof=1))
    sharpe = ((avg_daily_return - RISK_FREE_DAILY) / daily_vol * np.sqrt(252)) if daily_vol > 0 else np.nan
    drawdown = summary["Portfolio_Value"] / summary["Portfolio_Value"].cummax() - 1
    max_drawdown = safe_float(drawdown.min())
    win_rate = safe_float((summary["Portfolio_Return"] > 0).mean())
    sector_count = int(latest["Sector"].nunique())
    rebalance_days = int(summary["Date"].nunique())
    latest_return = safe_float(latest_row["Portfolio_Return"])
    latest_solver = latest["Solver"].mode().iloc[0] if "Solver" in latest and not latest["Solver"].empty else "recorded"
    total_weight = safe_float(latest["Weight"].sum())
    summary_stats = {
        "Latest trade date": latest_date.strftime("%B %d, %Y"),
        "Forward-test sessions": f"{rebalance_days}",
        "Starting wealth": money(STARTING_WEALTH),
        "Portfolio value": money(latest_value),
        "Wealth gain": money(wealth_gain),
        "Cumulative return": pct(cumulative_return),
        "Average daily return": pct(avg_daily_return),
        "Daily volatility": pct(daily_vol),
        "Annualized Sharpe": "N/A" if np.isnan(sharpe) else f"{sharpe:.2f}",
        "Maximum drawdown": pct(max_drawdown),
        "Win rate": pct(win_rate),
        "Current holdings": f"{len(latest)}",
        "Total portfolio weight": pct(total_weight),
        "Sector coverage": f"{sector_count} sectors",
        "Allocation rule": "Exactly 2 stocks from each of 5 sectors",
        "Weight bounds": "5% minimum and 50% maximum per selected stock",
        "Latest solver": str(latest_solver),
    }

    figs = [
        build_value_chart(summary),
        build_return_chart(summary),
        build_allocation_chart(latest),
        build_sector_chart(latest),
        build_contribution_chart(latest),
        build_heatmap(forward),
    ]
    divs = []
    for i, fig in enumerate(figs):
        divs.append(pio.to_html(fig, include_plotlyjs="cdn" if i == 0 else False, full_html=False))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>S&P 500 Portfolio Optimizer</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: {COLORS["background"]};
      --panel: {COLORS["panel"]};
      --panel-2: {COLORS["panel_2"]};
      --border: {COLORS["border"]};
      --text: {COLORS["text"]};
      --muted: {COLORS["muted"]};
      --cyan: {COLORS["cyan"]};
      --green: {COLORS["green"]};
      --red: {COLORS["red"]};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, "Segoe UI", Arial, sans-serif;
    }}
    header {{
      padding: 30px clamp(18px, 4vw, 56px) 18px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, #0b1730 0%, var(--bg) 100%);
    }}
    .eyebrow {{
      color: var(--cyan);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 10px 0 8px;
      font-size: clamp(30px, 4vw, 54px);
      line-height: 1.02;
      letter-spacing: 0;
    }}
    .subtitle {{
      max-width: 980px;
      margin: 0;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.55;
    }}
    nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 22px;
    }}
    nav a {{
      color: var(--text);
      text-decoration: none;
      padding: 10px 14px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,.04);
      border-radius: 6px;
      font-weight: 650;
    }}
    nav a.primary-link {{
      color: #06101f;
      border-color: var(--cyan);
      background: var(--cyan);
    }}
    main {{
      width: min(1460px, 100%);
      margin: 0 auto;
      padding: 24px clamp(14px, 3vw, 36px) 48px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(6, minmax(150px, 1fr));
      gap: 14px;
      margin-bottom: 22px;
    }}
    .metric-card {{
      min-height: 120px;
      padding: 18px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel-2);
    }}
    .metric-label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .06em;
      text-transform: uppercase;
    }}
    .metric-value {{
      margin-top: 12px;
      font-size: clamp(22px, 2.6vw, 34px);
      font-weight: 800;
      line-height: 1.05;
    }}
    .metric-card span {{
      display: block;
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.25fr .75fr;
      gap: 18px;
      align-items: start;
    }}
    .panel {{
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel);
    }}
    .wide {{ grid-column: 1 / -1; }}
    .notes {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin: 22px 0;
    }}
    .note {{
      padding: 18px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: rgba(255,255,255,.035);
      color: var(--muted);
      line-height: 1.5;
    }}
    .note strong {{
      display: block;
      margin-bottom: 7px;
      color: var(--text);
      font-size: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      padding: 13px 14px;
      border-bottom: 1px solid var(--border);
      text-align: right;
    }}
    th:first-child, td:first-child, th:nth-child(2), td:nth-child(2) {{ text-align: left; }}
    th {{
      color: var(--muted);
      font-size: 12px;
      letter-spacing: .05em;
      text-transform: uppercase;
      background: #0e182a;
    }}
    .summary-table td:first-child {{
      color: var(--muted);
      font-weight: 700;
      letter-spacing: .02em;
      text-transform: uppercase;
    }}
    .summary-table td:last-child {{
      color: var(--text);
      font-weight: 750;
    }}
    .section-title {{
      margin: 32px 0 14px;
      font-size: 22px;
    }}
    footer {{
      color: var(--muted);
      border-top: 1px solid var(--border);
      padding-top: 20px;
      margin-top: 24px;
      line-height: 1.5;
    }}
    @media (max-width: 1100px) {{
      .metrics {{ grid-template-columns: repeat(3, 1fr); }}
      .grid {{ grid-template-columns: 1fr; }}
      .notes {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 680px) {{
      .metrics {{ grid-template-columns: 1fr; }}
      th, td {{ padding: 10px 8px; font-size: 12px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="eyebrow">OPIM 5641 Portfolio Optimization Project</div>
    <h1>S&P 500 Portfolio Optimizer</h1>
    <p class="subtitle">
      Daily forward-test dashboard for a constrained active portfolio model. The optimizer selects 10 stocks,
      enforces a 5% minimum and 50% maximum position size, and holds exactly 2 stocks from each of 5 sectors.
    </p>
    <nav>
      <a class="primary-link" href="{COLAB_URL}">Powered by Colab</a>
      <a href="#summary-statistics">Summary Statistics</a>
      <a href="{REPO_URL}/blob/main/reports/latest_summary.md">Latest Summary</a>
      <a href="{REPO_URL}/blob/main/data/latest_portfolio_holdings.csv">Holdings CSV</a>
      <a href="{REPO_URL}/blob/main/data/portfolio_daily_summary.csv">Daily Results CSV</a>
    </nav>
  </header>

  <main>
    <section class="metrics">
      {metric_card("Latest Trade Date", latest_date.strftime("%b %d, %Y"), f"{rebalance_days} forward-test sessions")}
      {metric_card("Portfolio Value", money(latest_value), f"Started at {money(STARTING_WEALTH)}")}
      {metric_card("Wealth Gain", money(wealth_gain), pct(cumulative_return))}
      {metric_card("Latest Daily Return", pct(latest_return), f"Win rate {pct(win_rate)}")}
      {metric_card("Annualized Sharpe", "N/A" if np.isnan(sharpe) else f"{sharpe:.2f}", "Short forward-test window")}
      {metric_card("Max Drawdown", pct(max_drawdown), f"{sector_count} sectors, {len(latest)} holdings")}
    </section>

    <section class="notes">
      <div class="note"><strong>Colab workbook</strong>The project is powered by a Google Colab workbook that refreshes data, runs the optimization models, and writes the daily output files used by this dashboard.</div>
      <div class="note"><strong>Hard constraints</strong>Every daily allocation must sum to 100%, select exactly 10 stocks, keep each selected name between 5% and 50%, and include exactly 2 stocks per sector.</div>
      <div class="note"><strong>Automation</strong>GitHub Actions runs the workbook at 3:45 PM Eastern on market weekdays, refreshes Yahoo Finance data, validates the constraints, and republishes this dashboard.</div>
    </section>

    <h2 id="summary-statistics" class="section-title">Summary Statistics</h2>
    <section class="panel">
      <table class="summary-table">
        <tbody>
          {build_summary_stats_table(summary_stats)}
        </tbody>
      </table>
    </section>

    <section class="grid">
      <div class="panel">{divs[0]}</div>
      <div class="panel">{divs[3]}</div>
      <div class="panel">{divs[1]}</div>
      <div class="panel">{divs[4]}</div>
      <div class="panel wide">{divs[2]}</div>
      <div class="panel wide">{divs[5]}</div>
    </section>

    <h2 class="section-title">Latest Holdings</h2>
    <section class="panel">
      <table>
        <thead>
          <tr>
            <th>Stock</th>
            <th>Sector</th>
            <th>Weight</th>
            <th>Holding Value</th>
            <th>Stock Return</th>
            <th>Return Contribution</th>
          </tr>
        </thead>
        <tbody>
          {build_holdings_table(latest)}
        </tbody>
      </table>
    </section>

    <footer>
      Generated from the project workbook and refreshed data files. The dashboard is for academic modeling and presentation purposes only and is not financial advice.
      Latest solver recorded in the holdings log: {latest_solver}.
    </footer>
  </main>
</body>
</html>
"""


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    summary, latest, forward = load_inputs()
    html = render_dashboard(summary, latest, forward)
    out_path = DOCS_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
