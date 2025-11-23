"""Minimal Hacker News scraper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List
import datetime as dt
import requests
from bs4 import BeautifulSoup

HN_URL = "https://news.ycombinator.com/"


@dataclass
class HNPost:
    rank: int
    title: str
    url: str


class HackerNewsClient:
    """Scrapes the Hacker News front page and returns structured posts."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def fetch_top_posts(self, limit: int) -> list[HNPost]:
        response = self._session.get(HN_URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("tr.athing")
        posts: List[HNPost] = []
        for row in rows[:limit]:
            rank_text = row.select_one(".rank").get_text(strip=True).rstrip(".")
            title_el = row.select_one(".titleline > a")
            posts.append(
                HNPost(
                    rank=int(rank_text),
                    title=title_el.get_text(strip=True),
                    url=title_el["href"],
                )
            )
        return posts

    @staticmethod
    def format_markdown(posts: list[HNPost]) -> str:
        captured = [f"# Hacker News Top {len(posts)} — {dt.date.today():%Y-%m-%d}", ""]
        for post in posts:
            captured.append(f"{post.rank}. [{post.title}]({post.url})")
        captured.append("")
        return "\n".join(captured)

