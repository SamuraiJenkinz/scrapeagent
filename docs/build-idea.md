Daily cron -> scrapes HN front page -> saves top 10 posts to hn_<week>,md Review weekly.
Weekly review -> curate -> save to hn_<week>.md.

Support files live under:
- src/scrape_agent/... core logic
- scripts/... local entrypoints
- data/raw + data/weekly_reviews
- infra/azure/... timer-trigger function app