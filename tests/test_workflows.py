from scrape_agent import run_daily_scrape, run_weekly_review


def test_daily_returns_markdown(monkeypatch):
    def fake_fetch(*_args, **_kwargs):
        return []

    monkeypatch.setattr(
        "scrape_agent.workflows.HackerNewsClient.fetch_top_posts",
        lambda self, limit: [],
    )
    result = run_daily_scrape()
    assert isinstance(result, str)


def test_weekly_returns_summary():
    result = run_weekly_review(["item"])
    assert "item" in result

