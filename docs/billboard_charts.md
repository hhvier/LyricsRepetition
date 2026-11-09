# Weekly Billboard song charts

The dataset in `data/billboard/` is every public weekly **song** chart on Billboard from the first chart week of 2018 (`2018-01-03`) through the latest week published for that chart. The Hot 100 has 100 positions. Other charts are stored at whatever length Billboard prints on the public page (airplay charts are often 20–50, Hits of the World is usually 25, the Global 200 is 200).

Album charts, artist charts, songwriter/producer charts, and all-time or year-end lists are not in the song files. They are listed as skipped in `data/billboard/catalog.csv`.

## Refresh or resume

From the repository root, with the packages in `requirements.txt` installed:

```bash
python py/billboard_charts.py scrape
```

That command is safe to repeat. Each chart-week is cached under `data/billboard/cache/` (gitignored). A rerun skips weeks already saved, continues a chart that stopped early, and picks up a newer latest week when Billboard has published one. Finished charts cost one request each, to see whether a new week exists.

Useful flags:

```bash
python py/billboard_charts.py scrape --only hot-100,canadian-hot-100
python py/billboard_charts.py scrape --interval 0.7 --workers 2
python py/billboard_charts.py export
```

`--interval` is the minimum gap between HTTP requests across all workers. The default is 0.55 seconds. Do not lower it to hammer the site. If Billboard returns 401, 403, 429, or an anti-bot page, that chart is stopped and recorded. A second block stops the whole run so it can be resumed later. The scraper does not log in, solve captchas, or try to read positions that are not in the public HTML.

`export` rebuilds the CSV files and `data/billboard/VALIDATION.md` from the cache without downloading.

## Files

| Path | Contents |
| --- | --- |
| `data/billboard/weekly/<slug>.csv.gz` | One chart |
| `data/billboard/billboard_weekly_songs.csv.gz` | All charts, if the gzip is small enough for git |
| `data/billboard/catalog.csv` | Included charts, date ranges, row counts, and skipped charts with reasons |
| `data/billboard/VALIDATION.md` | Week counts, gaps, duplicate checks, and spot checks |
| `data/billboard/cache/` | Local resume cache, not committed |

CSV columns: `chart`, `region`, `category`, `chart_name`, `week`, `rank`, `title`, `artist`, `last_week`, `peak_position`, `weeks_on_chart`, `weeks_at_number_one`, `is_new`, `is_reentry`, `source_url`.

`week` is the chart issue date printed on the page (`Week of ...`), not the day the chart was fetched. `last_week` is blank when Billboard prints a dash. `weeks_at_number_one` is blank on charts that do not show that column.

## What changed from the old scraper

`py/billboard_scraper.py` used to request the Hot 100 and read `div.chart-list-item` (`data-rank`, `data-artist`, `data-title`) into MySQL. Those elements are gone, and the script also required a local database. It now delegates to `py/billboard_charts.py`. Chart slugs and the skip list live in `py/billboard_catalog.py`.
