## ScrapeAgent

Python-only automation that scrapes Hacker News daily and prepares a weekly, human-readable digest stored as `hn_<week>.md`. The long-term goal is to run the bot on Azure (Timer-triggered Azure Function + Blob Storage).

### Project layout
- `build-idea.md` — shorthand problem statement.
- `src/` — application code packaged as `scrape_agent`.
- `scripts/` — thin entrypoints for local execution.
- `data/` — working directory for raw scrapes and curated markdown exports.
- `infra/azure/` — Azure Function scaffolding plus sample settings.
- `tests/` — lightweight sanity checks.

### Getting started
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/run_daily.py
```

### AI insights
- Set `OPENROUTER_API_KEY` (optionally `OPENROUTER_MODEL`, `OPENROUTER_REFERER`, `OPENROUTER_TITLE`) before running.
- Each daily scrape makes a single call to `openrouter/gpt-5.1-thinking` asking for actionable AI/ML trends, then appends the response to the same markdown file.
- Without credentials the LLM step is skipped; the scraper still writes the daily digest.

### Deployment notes
1. Build an Azure Storage Account (Blob) for `data/raw` + `data/weekly_reviews`.
2. Publish the function inside `infra/azure/function_app` via `func azure functionapp publish`.
3. Provide the required env vars (`HN_TOP_N`, `OUTPUT_CONTAINER`, `BLOB_CONN_STR`) either via Azure App Settings or `local.settings.json`.
4. Use Azure Scheduler/Timer trigger CRON expressions to match the daily scrape + weekly summary cadence.

