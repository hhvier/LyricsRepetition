# Weekly Billboard song charts

The dataset in `data/billboard/` is the weekly **song** chart issues this collector could read from public pages, plus one Thailand week recovered from the Internet Archive. A chart whose first recovered week is after 2018-01-03 is not claimed to have launched on that week. Billboard sometimes answers an old URL with a much later issue. `catalog.csv` column `recovered_temporal_grid` describes stored printed dates only, and only when a scrape `_state.json` is present. `contiguous_stored_weeks` means those dates start by 2018-01-17 and step by at most 14 days. It is not a census of published issues and it is not a depth claim. `every_stored_week_has_100_rows` is a separate depth fact. Japan (25), the Official U.K. page (20), and Hits of the World (25) are false. Open spans are in `unrecovered_intervals.csv`.

`source_url` is the Billboard URL for the printed week. The original scrape did not keep request URLs or fetch timestamps. Those fields are stored only when a later fetch recorded them (see `data/billboard/resolution_checks.json` and the Thailand 2022-02-19 note in `data/billboard/provenance.json`).

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
| `data/billboard/VALIDATION.md` | Week counts, coverage labels, depth flags, and spot checks |
| `data/billboard/provenance.json` | Archive recovery and live resolution checks, with real fetch times |
| `data/billboard/resolution_checks.json` | The live-page checks alone |
| `data/billboard/cache/` | Local resume cache, not committed |

CSV columns: `chart`, `region`, `category`, `chart_name`, `week`, `rank`, `title`, `artist`, `last_week`, `peak_position`, `weeks_on_chart`, `weeks_at_number_one`, `is_new`, `is_reentry`, `source_url`.

`week` is the chart issue date printed on the page (`Week of ...`), not the day the chart was fetched. `last_week` is blank when Billboard prints a dash. `weeks_at_number_one` is blank on charts that do not show that column.

## What changed from the old scraper

`py/billboard_scraper.py` used to request the Hot 100 and read `div.chart-list-item` (`data-rank`, `data-artist`, `data-title`) into MySQL. Those elements are gone, and the script also required a local database. It now delegates to `py/billboard_charts.py`. Chart slugs and the skip list live in `py/billboard_catalog.py`.
