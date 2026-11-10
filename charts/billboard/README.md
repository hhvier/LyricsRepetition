# Weekly Billboard song charts

1,444,086 chart positions from 120 Billboard song charts, one row per song per week. The 2018-on weeks were read from Billboard's public chart pages on 2026-11-09. On 2026-11-10, three charts gained earlier weeks whose printed date matched the requested date: Canadian Hot 100 from 2007-03-31 (56,200 rows), the Official U.K. Singles Chart from 2011-01-29 (4,959 rows) and Adult Contemporary from 2010-01-09 (12,510 rows). The U.K. page lists 10 positions through 2015-06-06, 9 on 2011-12-31, and 20 from 2015-06-13. Album, artist and credit charts are not included.

Time gaps, including the history before 2018 that is missing, are listed in [`GAPS.md`](../../GAPS.md).

## Files

| File | Contents |
| --- | --- |
| `billboard_weekly_songs.csv.gz` | All positions |
| `verification.csv` | Which charts were checked, against what, and which weeks are flagged |
| `catalog.csv` | Every chart considered: included charts with spans and depth, and skipped ones with the reason |
| `unrecovered_intervals.csv` | Open periods per chart, with evidence |
| `provenance.json` | The one week recovered from the Internet Archive, and live-page checks with fetch times |
| `VALIDATION.md` | The collector's own report from 2026-11-09 |

Columns: `chart`, `region`, `category`, `chart_name`, `week`, `rank`, `title`, `artist`, `last_week`, `peak_position`, `weeks_on_chart`, `weeks_at_number_one`, `is_new`, `is_reentry`, `source_url`. `week` is the issue date printed on the page. `last_week` is blank for new entries.

## Verification

`verification.csv` gives each chart one `status`:

| Status | Charts | Meaning |
| --- | ---: | --- |
| `verified` | 1 | Hot 100, compared with [mhollingshead/billboard-hot-100](https://github.com/mhollingshead/billboard-hot-100) for every week: 99.88% of 46,200 positions are the same song |
| `verified_2018_only` | 7 | Hot Country, Hot R&B/Hip-Hop, Hot Latin, Pop Airplay, Hot Rock & Alternative, Hot Dance/Electronic and Japan Hot 100, compared with [pdp2600/chartscraper](https://github.com/pdp2600/chartscraper) for 2018: 98.3% to 100% the same. Weeks from 2019 on have no outside check |
| `unverified` | 112 | No outside source was available |

Every chart also has an internal check: a row's printed `last_week` should equal the song's rank in the stored week before, wherever we hold that position. All 120 charts agree on 99.4% to 100% of those rows. That shows the weeks are consistent with each other, but it can't catch a wrong chart or a wrong date applied to every week.

**Flagged weeks** (`flagged_weeks` column). Leave these out of analysis:

- **2018-01-03**, in the 56 charts that have it. Billboard's page for that date lists mostly the same songs as the neighbouring weeks but in a different order, and it doesn't match any Hot 100 week in the independent source. Its first regular week is 2018-01-06.
- **Thailand Songs 2022-02-19**, the only Thailand week before 2026. It comes from an Internet Archive copy, not the live site.

**Depth.** Most charts store fewer positions than the full chart: 25 for Hits of the World and Japan, 20 for the Official U.K. chart, and 15 to 60 for many U.S. genre charts. `catalog.csv` gives the depth of each chart. Compare ranks within one chart, not across charts.

## Where it came from

[Pull request #1](https://github.com/hhvier/LyricsRepetition/pull/1) collected the 2018-on files. The collector used for the later pre-2018 weeks and the launch checks is `py/billboard_charts.py` in this branch. The earlier copy remains in commit `4de0808` on `cursor/billboard-weekly-charts-2bc0`.
