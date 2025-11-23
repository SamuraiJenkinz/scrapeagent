"""Manual troubleshooting helper for the OpenRouter insights call."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from scrape_agent.config import load_settings  # noqa: E402
from scrape_agent.hn_client import HackerNewsClient  # noqa: E402
from scrape_agent.insights import OPENROUTER_URL  # noqa: E402


def main() -> None:
    settings = load_settings()
    if not settings.openrouter_api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment.")

    client = HackerNewsClient()
    posts = client.fetch_top_posts(settings.hn_top_n)
    story_list = "\n".join(f"- {p.title} ({p.url})" for p in posts)

    payload = {
        "model": settings.openrouter_model,
        "max_tokens": settings.openrouter_max_tokens,
        "messages": [
            {
                "role": "system",
                "content": "You are an elite AI analyst focused on extracting actionable AI/ML trends from Hacker News.",
            },
            {
                "role": "user",
                "content": (
                    "Review these Hacker News stories and return concise, actionable insights about AI trends, "
                    "breakthroughs, and market signals:\n\n"
                    f"{story_list}"
                ),
            },
        ],
    }
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": settings.openrouter_referer,
        "X-Title": settings.openrouter_title,
    }

    print("[debug_ai_insights] Sending payload to OpenRouter...")
    response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
    print(f"[debug_ai_insights] Status: {response.status_code}")
    print("[debug_ai_insights] Raw response:")
    try:
        parsed = response.json()
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print(response.text)


if __name__ == "__main__":
    main()

