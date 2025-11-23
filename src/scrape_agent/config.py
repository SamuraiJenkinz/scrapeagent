"""Centralized configuration helpers for ScrapeAgent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    """Runtime configuration pulled from environment variables."""

    hn_top_n: int = int(os.getenv("HN_TOP_N", "10"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "data/raw"))
    weekly_dir: Path = Path(os.getenv("WEEKLY_DIR", "data/weekly_reviews"))
    blob_conn_str: str | None = os.getenv("BLOB_CONN_STR")
    output_container: str | None = os.getenv("OUTPUT_CONTAINER")
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/gpt-5.1-thinking")
    openrouter_referer: str = os.getenv("OPENROUTER_REFERER", "https://scrapeagent.local")
    openrouter_title: str = os.getenv("OPENROUTER_TITLE", "ScrapeAgent")
    openrouter_max_tokens: int = int(os.getenv("OPENROUTER_MAX_TOKENS", "600"))

    @property
    def is_cloud_mode(self) -> bool:
        return bool(self.blob_conn_str and self.output_container)


def load_settings() -> Settings:
    """Factory so downstream modules can import lazily."""
    settings = Settings()
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    settings.weekly_dir.mkdir(parents=True, exist_ok=True)
    return settings

