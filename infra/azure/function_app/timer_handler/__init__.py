"""Azure Function timer trigger entrypoint."""

from __future__ import annotations

import datetime as dt
import logging
import sys
from pathlib import Path

import azure.functions as func

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from scrape_agent import run_daily_scrape  # noqa: E402


def main(mytimer: func.TimerRequest) -> None:
    utc_now = dt.datetime.utcnow().isoformat()
    logging.info("Timer triggered at %s", utc_now)

    if mytimer.past_due:
        logging.warning("Timer is running late!")

    run_daily_scrape()
    logging.info("Scrape complete.")

