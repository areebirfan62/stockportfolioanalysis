from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
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
    dest = target_dir / filename
    candidates = [
        ROOT / filename,
        NOTEBOOKS / filename,
    ]

    for src in candidates:
        if src.exists():
            if src.resolve() == dest.resolve():
                print(f"Already present: {dest.relative_to(ROOT)}")
                return
            shutil.move(str(src), str(dest))
            print(f"Moved {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
            return

    raise FileNotFoundError(
        f"Expected fresh notebook output file not found: {filename}. "
        f"Checked: {', '.join(str(p.relative_to(ROOT)) for p in candidates)}"
    )


for name in REPORT_FILES:
    move_if_exists(name, REPORTS)

for name in DATA_FILES:
    move_if_exists(name, DATA)

print("All notebook outputs collected.")
