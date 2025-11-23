"""High-level workflows consumed by CLI, schedulers, and Azure Functions."""

from __future__ import annotations

import datetime as dt

from .config import load_settings
from .hn_client import HackerNewsClient
from .insights import summarize_ai_insights
from .storage import upload_blob, write_locally
from .review import persist_weekly_summary, render_weekly_summary


def _week_stamp(date: dt.date | None = None) -> str:
    date = date or dt.date.today()
    return f"{date.isocalendar().week:02d}"


def run_daily_scrape() -> str:
    settings = load_settings()
    client = HackerNewsClient()
    posts = client.fetch_top_posts(settings.hn_top_n)
    markdown = client.format_markdown(posts)

    if settings.openrouter_api_key:
        insights = summarize_ai_insights(
            posts,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            referer=settings.openrouter_referer,
            title=settings.openrouter_title,
            max_tokens=settings.openrouter_max_tokens,
        )
        if insights:
            markdown = f"{markdown}\n## AI Insights\n\n{insights}\n"

    filename = f"hn_{_week_stamp()}_daily.md"
    target = settings.output_dir / filename
    write_locally(target, markdown)
    if settings.is_cloud_mode:
        upload_blob(
            settings.blob_conn_str,  # type: ignore[arg-type]
            settings.output_container,  # type: ignore[arg-type]
            filename,
            markdown,
        )
    return markdown


def run_weekly_review(notes: list[str] | None = None) -> str:
    settings = load_settings()
    notes = notes or ["Review notes go here."]
    rendered = render_weekly_summary(notes)
    target = persist_weekly_summary(settings.weekly_dir, notes)
    if settings.is_cloud_mode:
        upload_blob(
            settings.blob_conn_str,  # type: ignore[arg-type]
            settings.output_container,  # type: ignore[arg-type]
            target.name,
            rendered,
        )
    return rendered

