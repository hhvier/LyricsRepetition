# Chart data gaps

Status on 2026-11-10. This lists **gaps in time** only: each chart's stored weeks are treated as complete, whatever their depth.
Week-level detail is in [`charts/billboard/unrecovered_intervals.csv`](charts/billboard/unrecovered_intervals.csv). On the `v2` branch (not pushed yet), `python -m pipeline report` also writes every chart's span and missing weeks to `data/gaps.csv`.
Which charts were checked against another source is in [`charts/billboard/verification.csv`](charts/billboard/verification.csv) (see [`charts/billboard/README.md`](charts/billboard/README.md)).

## 1. History before 2018 that we don't have

The weekly file's main block starts on 2018-01-03, but these charts are older. Start dates in the table are from Wikipedia, read on 2026-11-10. Canadian Hot 100 from 2007-03-31, the Official U.K. chart from 2011-01-29, and Adult Contemporary from 2010-01-02 are now in the weekly file. What was recovered, and what was left as a scope decision, is in section 8.

| Chart | Started | Years missing | Note |
| --- | --- | ---: | --- |
| The Official U.K. Singles Chart (`official-uk-songs`) | 1952-11-14 | 58 | weekly file starts 2011-01-29; Billboard's page shows 10 to 20 positions |
| Adult Contemporary (`adult-contemporary`) | 1961-07-17 | 48 | weekly file starts 2010-01-02 |
| Mainstream Rock Airplay (`hot-mainstream-rock-tracks`) | 1981-03 | 37 |  |
| Alternative Airplay (`alternative-airplay`) | 1988-09-10 | 29 |  |
| Bubbling Under Hot 100 (`bubbling-under-hot-100-singles`) | 1992 | 26 | current run since its 1992 revival |
| Adult R&B Airplay (`hot-adult-r-and-b-airplay`) | 1993-09 | 24 |  |
| Regional Mexican Airplay (`latin-regional-mexican-airplay`) | 1994-10 | 23 |  |
| Latin Pop Airplay (`latin-pop-airplay`) | 1994-10 | 23 |  |
| Tropical Airplay (`latin-tropical-airplay`) | 1994-10 | 23 |  |
| Christian Airplay (`christian-airplay`) | 2003-06-21 | 15 |  |
| Dance Airplay (`hot-dance-airplay`) | 2003-08-16 | 14 |  |
| Digital Song Sales (`digital-song-sales`) | 2005-01-22 | 13 | sales tracked from 2004-10-30 |
| Hot Gospel Songs (`gospel-songs`) | 2005-03-19 | 13 |  |
| Latin Rhythm Airplay (`latin-rhythm-airplay`) | 2005-08 | 12 | about three months after 2005-05-21 |
| Hot R&B Songs (`r-and-b-songs`) | 2012-10-11 | 5 |  |
| Country Airplay (`country-airplay`) | 2012-10-20 | 5 | Billboard also counts airplay-only Hot Country Songs from 1990-01-20 |
| Latin Airplay (`latin-airplay`) | 2012-10-20 | 5 |  |
| Streaming Songs (`streaming-songs`) | 2013-01-19 | 5 | first number one |

These 28 charts were already running on 2018-01-03, so some history is missing, but their start dates were not checked:

- Adult Pop Airplay (`adult-pop-songs`)
- Hot Christian Songs (`christian-songs`)
- Christian Streaming Songs (`christian-streaming-songs`)
- Country Streaming Songs (`country-streaming-songs`)
- Dance Streaming Songs (`dance-electronic-streaming-songs`)
- Gospel Airplay (`gospel-airplay`)
- Gospel Streaming Songs (`gospel-streaming-songs`)
- Holiday Airplay (`holiday-songs`)
- Holiday Streaming Songs (`holiday-streaming-songs`)
- Christian AC Airplay (`hot-christian-adult-contemporary`)
- Holiday 100 (`hot-holiday-songs`)
- R&B/Hip-Hop Airplay (`hot-r-and-b-hip-hop-airplay`)
- Rap Airplay (`hot-rap-tracks`)
- Hot Rock Songs (`hot-rock-songs`)
- Smooth Jazz Airplay (`jazz-songs`)
- Latin Streaming Songs (`latin-streaming-songs`)
- LyricFind Global (`lyricfind-global`)
- LyricFind U.S. (`lyricfind-us`)
- Mainstream R&B/Hip-Hop Airplay (`mainstream-r-and-b-hip-hop`)
- R&B/Hip-Hop Streaming Songs (`r-and-b-hip-hop-streaming-songs`)
- R&B Streaming Songs (`r-and-b-streaming-songs`)
- Radio Songs (`radio-songs`)
- Hot Rap Songs (`rap-song`)
- Rap Streaming Songs (`rap-streaming-songs`)
- Rhythmic Airplay (`rhythmic-40`)
- Rock & Alternative Airplay (`rock-airplay`)
- Rock Streaming Songs (`rock-streaming-songs`)
- Adult Alternative Airplay (`triple-a`)

Already covered before 2018:

- Billboard Canadian Hot 100 (`canadian-hot-100`): weekly file from 2007-03-31 (chart launch)
- Billboard Hot 100™ (`hot-100`): mhollingshead/billboard-hot-100 from 1958-08-04
- Hot Country Songs (`country-songs`): chartscraper from 1958-10-20
- Hot R&B/Hip-Hop Songs (`r-b-hip-hop-songs`): chartscraper from 1958-10-20
- Hot Latin Songs (`latin-songs`): chartscraper from 1986-09-20 (chart launch)
- Pop Airplay (`pop-songs`): chartscraper from 1992-10-03 (chart launch)
- Hot Rock & Alternative Songs (`rock-songs`): chartscraper from 2009-06-20 (chart launch)
- Hot Dance/Electronic Songs (`dance-electronic-songs`): chartscraper from 2013-01-26 (chart launch)
- Billboard Japan Hot 100 (`japan-hot-100`): chartscraper from 2011-04-09; the chart began 2008-02, so 2008-02 to 2011-04 is missing

## 2. Holes inside a chart's run

| Chart | Missing | Why |
| --- | --- | --- |
| Thailand Songs (`thailand-songs-hotw`) | 2022-02-26 to 2026-07-25, about 4.4 years | Only the 2022-02-19 launch week survives, from the Internet Archive; the live site redirects old weeks to 2026 |
| Billboard Vietnam Hot 100 (`billboard-vietnam-hot-100-songs`) | 2022-01-14 to 2025-05-24, about 3.4 years | Launched January 2022; the live site starts at 2025-05-31 and no archive copy was found |
| Billboard Vietnam Top Vietnamese Songs (`billboard-vietnam-top-vietnamese-songs`) | 2022-01-14 to 2025-06-21, about 3.4 years | Same as above; live data starts 2025-06-28 |
| LyricFind U.S. and LyricFind Global | week of 2018-05-26 | That date resolves to the next stored week |
| Billboard Argentina Hot 100 | week of 2023-08-19 | Same |
| Billboard Italy Hot 100 | week of 2023-09-23 | Same |
| The Arabic Hot 100 | week of 2026-02-21 | Same |

## 3. Charts that stopped

- YouTube Songs: weekly data runs 2011-08-27 to 2018-12-29 (chartscraper); its Billboard page no longer exists.
- Dance Club Songs (`dance-club-play-songs`): began 1976, ended 2020; we hold 2018-01-03 to 2020-03-28 only, so 1976 to 2017 is missing.

## 4. Billboard song charts with no data at all

These were probed and return 404 today, so nothing was recovered for any period:

- `tiktok-billboard-top-50`
- `country-digital-song-sales`
- `rock-digital-song-sales`
- `r-and-b-hip-hop-digital-song-sales`
- `rap-digital-song-sales`
- `latin-digital-song-sales`
- `dance-electronic-digital-song-sales`
- `christian-digital-song-sales`
- `gospel-digital-song-sales`
- `world-digital-song-sales`
- `kpop-hot-100`
- `billboard-korea-100`
- `youtube-songs`
- `on-demand-streaming-songs`

## 5. First stored week after 2018, launch not checked

These charts start later than 2018-01-03. Many are probably new charts, but a first stored week is not proof of a launch: Billboard's site sends some old dates to a much later week (see Thailand and Vietnam above). Any of these may hide missing history:

- Songs Of The Summer (`summer-songs`): 2018-06-09
- Billboard Argentina Hot 100 (`billboard-argentina-hot-100`): 2018-11-10
- Alternative Streaming Songs (`alternative-streaming-songs`): 2020-06-13
- Hard Rock Streaming Songs (`hard-rock-streaming-songs`): 2020-06-13
- Hot Alternative Songs (`hot-alternative-songs`): 2020-06-13
- Hot Hard Rock Songs (`hot-hard-rock-songs`): 2020-06-13
- Billboard Global 200 (`billboard-global-200`): 2020-09-19
- Billboard Global Excl. US (`billboard-global-excl-us`): 2020-09-19
- Australia Songs (`australia-songs-hotw`): 2022-02-19
- Austria Songs (`austria-songs-hotw`): 2022-02-19
- Belgium Songs (`belgium-songs-hotw`): 2022-02-19
- Bolivia Songs (`bolivia-songs-hotw`): 2022-02-19
- Chile Songs (`chile-songs-hotw`): 2022-02-19
- Croatia Songs (`croatia-songs-hotw`): 2022-02-19
- Czech Republic Songs (`czech-republic-songs-hotw`): 2022-02-19
- Denmark Songs (`denmark-songs-hotw`): 2022-02-19
- Ecuador Songs (`ecuador-songs-hotw`): 2022-02-19
- Finland Songs (`finland-songs-hotw`): 2022-02-19
- France Songs (`france-songs-hotw`): 2022-02-19
- Germany Songs (`germany-songs-hotw`): 2022-02-19
- Greece Songs (`greece-songs-hotw`): 2022-02-19
- Hong Kong Songs (`hong-kong-songs-hotw`): 2022-02-19
- Hungary Songs (`hungary-songs-hotw`): 2022-02-19
- Iceland Songs (`iceland-songs-hotw`): 2022-02-19
- India Songs (`india-songs-hotw`): 2022-02-19
- Indonesia Songs (`indonesia-songs-hotw`): 2022-02-19
- Ireland Songs (`ireland-songs-hotw`): 2022-02-19
- Luxembourg Songs (`luxembourg-songs-hotw`): 2022-02-19
- Malaysia Songs (`malaysia-songs-hotw`): 2022-02-19
- Mexico Songs (`mexico-songs-hotw`): 2022-02-19
- Netherlands Songs (`netherlands-songs-hotw`): 2022-02-19
- New Zealand Songs (`new-zealand-songs-hotw`): 2022-02-19
- Norway Songs (`norway-songs-hotw`): 2022-02-19
- Peru Songs (`peru-songs-hotw`): 2022-02-19
- Poland Songs (`poland-songs-hotw`): 2022-02-19
- Portugal Songs (`portugal-songs-hotw`): 2022-02-19
- Romania Songs (`romania-songs-hotw`): 2022-02-19
- Singapore Songs (`singapore-songs-hotw`): 2022-02-19
- Slovakia Songs (`slovakia-songs-hotw`): 2022-02-19
- South Africa Songs (`south-africa-songs-hotw`): 2022-02-19
- Spain Songs (`spain-songs-hotw`): 2022-02-19
- Sweden Songs (`sweden-songs-hotw`): 2022-02-19
- Switzerland Songs (`switzerland-songs-hotw`): 2022-02-19
- Taiwan Songs (`taiwan-songs-hotw`): 2022-02-19
- Turkey Songs (`turkey-songs-hotw`): 2022-02-19
- U.K. Songs (`u-k-songs-hotw`): 2022-02-19
- Billboard U.S. Afrobeats Songs (`billboard-u-s-afrobeats-songs`): 2022-04-02
- China TME UNI Chart (`china-tme-uni-songs`): 2022-11-05
- Billboard Italy Hot 100 (`billboard-italy-hot-100`): 2023-06-17
- Billboard Brasil Hot 100 (`billboard-brasil-hot-100`): 2023-09-02
- Billboard Arabic Hot 100 (`the-arabic-hot-100`): 2023-12-16
- Billboard Philippines Hot 100 (`billboard-philippines-hot-100`): 2024-07-06
- Billboard Philippines Top Philippine Songs (`billboard-philippines-top-philippine-songs`): 2024-07-06
- Hot Dance/Pop Songs (`hot-dance-pop-songs`): 2025-01-18
- Hot Latin Pop Songs (`hot-latin-pop-songs`): 2025-04-12
- Hot Latin Rhythm Songs (`hot-latin-rhythm-songs`): 2025-04-12
- Hot Regional Mexican Songs (`hot-regional-mexican-songs`): 2025-04-12
- Hot Tropical Songs (`hot-tropical-songs`): 2025-04-12
- Billboard Colombia Hot 100 (`billboard-colombia-hot-100`): 2025-11-15
- Billboard Korea Global K-Songs (`billboard-korea-global-k-songs`): 2025-12-06
- WARM Global Dance Radio (`warm-global-dance-radio`): 2026-03-14

## 6. Not gaps

- **Seasonal charts.** Holiday charts run only around December and Songs of the Summer only from about June to September, by design.
- **Hot Country Songs at 2018-12-31 to 2019-01-12.** Chartscraper dates country weeks five days before Billboard's issue date, so this 12-day step has no missing week (checked: the two sources agree once shifted).
- **Hot 100 at 1961-12-25 to 1962-01-06.** A 12-day step where the dates move from Mondays to Saturdays; probably a label change, not a missing week, but not checked.

## 7. Other sources used by V2

- **Billboard Hot 100:** 1958-08-04 to now, weekly, no breaks apart from the 1962 step above.
- **Chartscraper genre charts:** to 2018-12-31; continued by the weekly file from 2019.
- **Mais Tocadas (Brazil):** yearly top 100, 1959 to 2025; the 2026 list is not final yet.
- **Spotify weekly charts (Kworb, 21 markets):** still downloading; spans not known yet.

## 8. Follow-up, 2026-11-10

The introduction and the opening of section 1 point here. Sections 2 to 7 are unchanged. This section records what was checked after them. The week-level file is [`charts/billboard/unrecovered_intervals.csv`](charts/billboard/unrecovered_intervals.csv). The weekly file has 1,444,116 rows, including Adult Contemporary for 2010-01-02.

**Issue dates.** A hole between two stored issues is the issue dates strictly inside that hole: the next issue after the earlier week through the issue before the later week. Thailand Songs is 2022-02-26 to 2026-07-25. Billboard Vietnam Hot 100 ends 2025-05-24, and Billboard Vietnam Top Vietnamese Songs ends 2025-06-21. Those three rows in `unrecovered_intervals.csv` now use those dates. Rows labeled `before_first_stored_week` still end on the calendar day before the first stored week. They mean "nothing earlier is stored." They are not a list of missing issues.

**2018-01-03.** Fifty-six charts have this Wednesday issue. The rows are still in the weekly file. `verification.csv` flags them, and the chart README says to leave them out of analysis. It is not a time gap, and it was not deleted. On the three charts extended below, 2017-12-30 is followed by 2018-01-03 and then 2018-01-06. That 4-day step is the Wednesday issue, not a missing Saturday.

**Section 2.** On 2026-11-10 the same four dates still printed the next stored week, not a chart of their own: LyricFind U.S. and LyricFind Global 2018-05-26 printed 2018-06-02; Argentina 2023-08-19 printed 2023-08-26; Italy 2023-09-23 printed 2023-09-30; Arabic 2026-02-21 printed 2026-02-28. No rows were added. They stay `requested_date_resolved_to_next_stored_week`.

**Section 5, confirmed first issues.** These first stored weeks match a contemporary source, so weeks before them are not gaps. `catalog.csv` records the source.

- Billboard Global 200 and Billboard Global Excl. US, 2020-09-19. Billboard, 14 Sep 2020. Stored No. 1 songs are WAP and Hawái.
- Hot Alternative Songs, Hot Hard Rock Songs, Alternative Streaming Songs and Hard Rock Streaming Songs, 2020-06-13. Billboard, 10 Jun 2020. The two Hot charts' stored No. 1 songs match the article (Death Bed; Popular Monster).
- Hits of the World charts whose first stored week is 2022-02-19. Billboard, 14 Feb 2022 and 15 Feb 2022, dates the inaugural rankings 19 Feb 2022. The 15 Feb article names the stored No. 1 for Australia, Slovakia, Austria, Germany, Luxembourg, Bolivia, Ecuador, Peru, Iceland, Ireland, the U.K. and Portugal. Bandwagon, 17 Feb 2022, names India, Indonesia and Taiwan. The other territories in this file are the same program launch and are not named one by one. On 2026-11-10 the 2022-02-12 URLs for Australia and France printed 2022-02-19.
- Billboard U.S. Afrobeats Songs, 2022-04-02. Billboard, 29 Mar 2022. Stored No. 1 is Love Nwantiti.
- Billboard Italy Hot 100, 2023-06-17. The page still prints that week, and the top songs are marked new with debut date 06/17/23.
- Billboard Brasil Hot 100, 2023-09-02. On 2026-11-10 the 2023-08-26 URL printed 2023-09-02. A Wikipedia number-one list cites an archived Billboard Brasil page for the week of 28 Aug 2023; those Monday labels sit five days before the Saturday issue dates, and the stored No. 1 songs match through 2023-10-07. That archive page was not opened. pt.wikipedia gives 2023-08-28 as the first week; the first stored billboard.com issue is 2023-09-02.
- Billboard Arabic Hot 100, 2023-12-16. SRMG's 14 Dec 2023 announcement lists the same top three songs.
- Billboard Philippines Hot 100 and Top Philippine Songs, 2024-07-06. GMA News, 4 Jul 2024, and Billboard Philippines. The stored top songs match.

**Section 5, launch known and still missing.** Billboard Argentina Hot 100 launched with the chart dated 2018-10-13 (Billboard Argentina, 12 Oct 2018; Billboard, 17 Oct 2018; No. 1 Cuando Te Besé). The stored file starts 2018-11-10. On 2026-11-10 the URLs for 2018-10-13, 2018-10-20, 2018-10-27 and 2018-11-03 each printed 2018-11-10, so those four issue dates were not recovered. The stored public list is 25 songs in every week. The launch article describes a 100-song chart. No other list was imported.

**Section 5, not confirmed.** Songs of the Summer is the seasonal chart in section 6. On 2026-11-10 the 2018-06-02 URL printed 2018-06-09. For China TME UNI, Hot Dance/Pop, the four April 2025 Latin song charts, Colombia, Korea Global K-Songs and WARM Global Dance Radio, the previous Saturday URL printed the first stored week. No contemporary launch article was found, so those spans stay `before_first_stored_week`: not a launch, and not a claim that the earlier weeks were published and missed.

**Section 4, the four slugs that are not in the list of 14.** On 2026-11-10, `heatseekers-songs` printed the week of 2014-11-29 with 25 songs. It is not a 404, and it has no post-2018 week in this file. `alternative-digital-song-sales`, `hard-rock-digital-song-sales` and `dance-mix-show-airplay` resolve to year-end artist pages (Alternative Digital Song Sales Artists, Hard Rock Digital Song Sales Artists, Dance/Mix Show Airplay Artists), not a weekly song chart. Section 4 is the song-chart slugs that 404.

**YouTube Songs.** Both earlier sentences are true. The chartscraper file runs 2011-08-27 to 2018-12-29, 384 weekly issues. `youtube-songs` on billboard.com is in the 404 list, so those rows were not copied.

**Section 1, what was attempted.** Only weeks whose printed date matched the requested date were stored. Fetched 2026-11-10, 09:07–09:23 America/Sao_Paulo.

| Chart | Stored | Rows | What the live page did not serve |
| --- | --- | ---: | --- |
| Billboard Canadian Hot 100 | 2007-03-31 to 2017-12-30, 562 weeks, 100 positions | 56,200 | 2007-03-24 prints 2007-03-31 |
| The Official U.K. Singles Chart | 2011-01-29 to 2017-12-30, 362 weeks | 4,959 | 2000-01-08 and 2011-01-22 print 2011-01-29. Depth is 10 through 2015-06-06, 9 on 2011-12-31, and 20 from 2015-06-13 |
| Adult Contemporary | 2010-01-02 to 2017-12-30, 418 weeks, 30 positions | 12,540 | 2010-01-02 prints Week of January 2, 2010. 1990-01-06 prints that date with 50 positions and was not collected. 1961-07-22 prints 1961-07-24, so the Wikipedia start is not a matching issue date |

The other charts in section 1 were not requested. Adult Contemporary from 1990 through 2009 was not requested. Nothing was taken back to the 1950s.

`unrecovered_intervals.csv` has one `pre_2018_history_scope` row each for the U.K. chart before 2011-01-29, Adult Contemporary before 2010-01-02, and Canadian Hot 100 at 2007-03-24. Those are scope decisions. They are not failed downloads. The U.K. page does not serve a matching week before 2011-01-29. The 1990 Adult Contemporary issues do print, at 50 positions, and were left out. The Canadian URL for 2007-03-24 prints the first stored week.

On the Official U.K. chart, `last_week`, `weeks_on_chart`, and the new-entry flag follow Billboard's published list, which is 10 positions through 2015-06-06 (9 on 2011-12-31) and 20 from 2015-06-13. They are not the full Official Charts 100. A song can be new on the published list, or lose a last-week rank, when the page deepens from 10 to 20.

**Section 6 and 7, what was actually checked.** Chartscraper files were read, not imported, except for this date check. Hot Country dates in that file are Mondays, 1958-10-20 through 2018-12-31, every step 7 days. Adding five days lines 2018-12-24 and 2018-12-31 up with Billboard's 2018-12-29 and 2019-01-05, and both No. 1 songs are Speechless. Hot R&B/Hip-Hop, Hot Latin, Pop Airplay, Hot Rock & Alternative, Hot Dance/Electronic and Japan Hot 100 use the same dates as Billboard's issue dates: the 2018-12-22 and 2018-12-29 No. 1 songs match with no shift. The five-day offset is the country file only. Hot R&B/Hip-Hop has one non-weekly step inside the file, 1978-11-06 to 1978-11-11. The file spans otherwise match the start and end dates in section 1. That is a check of these files, not a check that every historical Billboard week exists.

The Hot 100 step from 1961-12-25 to 1962-01-06 was not fully audited. The billboard.com URL for 1961-12-30 prints the week of 6 Jan 1962, and a Google Books index of Billboard issues lists 25 Dec 1961 and then 6 Jan 1962. The claim that the Hot 100 has no other break from 1958 was not checked.

Kworb is not in this repository, and there is no download here whose span could be read. Mais Tocadas was not re-downloaded. `py/maistocadas_scraper.py` requests yearly pages from 1959 through 2018. The statement that those lists run through 2025 was not checked. Neither source was merged into the weekly file.
