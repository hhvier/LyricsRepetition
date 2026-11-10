# Chart data gaps

Status on 2026-11-10. This lists **gaps in time** only: each chart's stored weeks are treated as complete, whatever their depth.
Week-level detail is in [`charts/billboard/unrecovered_intervals.csv`](charts/billboard/unrecovered_intervals.csv); on the `v2` branch, `python -m pipeline report` also writes every chart's span and missing weeks to `data/gaps.csv`.
Which charts were checked against another source is in [`charts/billboard/verification.csv`](charts/billboard/verification.csv) (see [`charts/billboard/README.md`](charts/billboard/README.md)).

## 1. History before 2018 that we don't have

The weekly Billboard file starts on 2018-01-03, but these charts are older. Start dates are from Wikipedia, read on 2026-11-10.

| Chart | Started | Years missing before 2018 | Note |
| --- | --- | ---: | --- |
| The Official U.K. Singles Chart (`official-uk-songs`) | 1952-11-14 | 65 | the U.K. chart itself; Billboard's page shows 20 positions |
| Adult Contemporary (`adult-contemporary`) | 1961-07-17 | 56 |  |
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
| Billboard Canadian Hot 100 (`canadian-hot-100`) | 2007-03-31 | 11 |  |
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

Already covered before 2018 by another source used in V2:

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
