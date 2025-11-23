"""Helpers for curating the weekly markdown summary."""

from __future__ import annotations

import datetime as dt
from pathlib import Path


def build_weekly_filename(week: dt.date | None = None) -> str:
    week = week or dt.date.today()
    return f"hn_{week.isocalendar().week:02d}.md"


def render_weekly_summary(notes: list[str]) -> str:
    today = dt.date.today()
    header = f"# Weekly Hacker News Notes — Week {today.isocalendar().week}"
    body = "\n".join(f"- {note}" for note in notes) or "- TODO: add notes"
    return f"{header}\n\n{body}\n"


def persist_weekly_summary(target_dir: Path, notes: list[str]) -> Path:
    file_path = target_dir / build_weekly_filename()
    file_path.write_text(render_weekly_summary(notes), encoding="utf-8")
    return file_path

