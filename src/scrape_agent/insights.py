"""LLM-powered insight generation via OpenRouter."""

from __future__ import annotations

import logging
from typing import Sequence

import requests

from .hn_client import HNPost

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def summarize_ai_insights(
    posts: Sequence[HNPost],
    *,
    api_key: str,
    model: str,
    referer: str,
    title: str,
    max_tokens: int,
) -> str:
    if not posts:
        return ""

    story_list = "\n".join(f"- {p.title} ({p.url})" for p in posts)
    payload = {
        "model": model,
        "max_tokens": max_tokens,
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
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": referer,
        "X-Title": title,
    }
    try:
        response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.HTTPError as exc:  # pragma: no cover
        detail = exc.response.text if exc.response is not None else "no response body"
        logging.error("OpenRouter insights failed (%s): %s", exc.response.status_code if exc.response else "HTTPError", detail)
        return ""
    except Exception as exc:  # pragma: no cover
        logging.error("OpenRouter insights failed: %s", exc)
        return ""

