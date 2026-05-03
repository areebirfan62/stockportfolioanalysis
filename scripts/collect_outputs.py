from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DATA = ROOT / "data"

REPORTS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

REPORT_FILES = [
    "womack_frontier.png",
    "model1_results.png",
    "ma_signals.png",
    "xgboost_analysis.png",
    "final_dashboard.png",
]

DATA_FILES = [
    "portfolio_forward_log.csv",
    "portfolio_daily_summary.csv",
    "latest_portfolio_holdings.csv",
]


def move_if_exists(filename: str, target_dir: Path) -> None:
    src = ROOT / filename
    dest = target_dir / filename
    if src.exists():
        shutil.move(str(src), str(dest))
        print(f"Moved {filename} -> {target_dir.relative_to(ROOT)}")
    elif dest.exists():
        print(f"Already present: {dest.relative_to(ROOT)}")
    else:
        raise FileNotFoundError(f"Expected output file not found: {filename}")


for name in REPORT_FILES:
    move_if_exists(name, REPORTS)

for name in DATA_FILES:
    move_if_exists(name, DATA)

print("All notebook outputs collected.")
