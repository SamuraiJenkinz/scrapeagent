"""Local helper to run the weekly review workflow."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from scrape_agent import run_weekly_review  # noqa: E402


def main() -> None:
    summary = run_weekly_review()
    print(summary)


if __name__ == "__main__":
    main()

