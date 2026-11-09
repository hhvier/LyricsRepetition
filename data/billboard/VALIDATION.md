# Billboard weekly chart validation

Generated 2026-11-09T18:22:21+00:00.
Song-chart rows: 1370367.
Combined file: data/billboard/billboard_weekly_songs.csv.gz (16.9 MB, 1370367 rows).

## Coverage

Attempted song-chart statuses: done=120, skipped=18
Menu charts recorded as skipped (albums, artist/credit charts, all-time lists): 145.

Rows by region:

- United States: 881489
- Global: 77150
- Global excluding United States: 64200
- Canada: 46300
- United Kingdom: 15455
- Japan: 11550
- China: 10500
- Argentina: 10425
- Australia: 6175
- Austria: 6175
- Belgium: 6175
- Bolivia: 6175
- Chile: 6175
- Croatia: 6175
- Czech Republic: 6175
- Denmark: 6175
- Ecuador: 6175
- Finland: 6175
- France: 6175
- Germany: 6175
- Greece: 6175
- Hong Kong: 6175
- Hungary: 6175
- Iceland: 6175
- India: 6175
- Indonesia: 6175
- Ireland: 6175
- Luxembourg: 6175
- Malaysia: 6175
- Mexico: 6175
- Netherlands: 6175
- New Zealand: 6175
- Norway: 6175
- Peru: 6175
- Poland: 6175
- Portugal: 6175
- Singapore: 6175
- Slovakia: 6175
- South Africa: 6175
- Spain: 6175
- Sweden: 6175
- Switzerland: 6175
- Taiwan: 6175
- Turkey: 6175
- Romania: 6173
- Philippines: 6000
- Italy: 4425
- Brazil: 4175
- Arabic (worldwide): 3750
- Vietnam: 3625
- Colombia: 1250
- South Korea: 1225
- Thailand: 375

## Hot 100

Hot 100 weeks fetched: 463 (2018-01-03 through 2026-11-07).
Expected Saturday issues from 2018-01-06 through 2026-11-07, plus the 2018-01-03 mid-week chart: 463.
Missing expected dates: 0.
Extra dates: 0.
Rows per week: min 100, median 100, max 100.
Duplicate-rank weeks: 0. Weeks with a hole in 1..max rank: 0.

## Spot checks

- OK hot-100 2018-01-03 #1: Perfect — Ed Sheeran (expected Perfect / Ed Sheeran)
- OK hot-100 2018-01-06 #1: Perfect — Ed Sheeran (expected Perfect / Ed Sheeran)
- OK hot-100 2018-01-06 #100: Juice — Yo Gotti (expected Juice / Yo Gotti)
- OK hot-100 2018-02-03 #1: God's Plan — Drake (expected God's Plan / Drake)
- OK hot-100 2026-11-07 #1: Choosin' Texas — Ella Langley (expected Choosin' Texas / Ella Langley)
- OK pop-songs 2018-01-06 #1: Havana — Camila Cabello Featuring Young Thug (expected Havana / Camila Cabello)
- OK canadian-hot-100 2018-01-06 #1: Perfect — Ed Sheeran (expected Perfect / Ed Sheeran)
- OK official-uk-songs 2018-01-06 #1: Perfect — Ed Sheeran (expected Perfect / Ed Sheeran)
- OK billboard-global-200 2020-09-19 #1: WAP — Cardi B Featuring Megan Thee Stallion (expected WAP / Cardi B)

## Gaps, failures, partial lists

- christian-songs: status done, weeks 463, dup ranks 0, rank holes 1. The 2023-10-21 page lists 49 songs and skips rank 30. That is how the public page is printed.
- A few charts skip one issue date. Requesting the missing date returns the next published week, so Billboard did not publish that issue: LyricFind U.S. and LyricFind Global have no 2018-05-26 chart; Argentina Hot 100 has no 2023-08-19 chart; Italy Hot 100 has no 2023-09-23 chart; Arabic Hot 100 has no 2026-02-21 chart.
- Romania Songs published 24 songs, ranks 1–24, on 2025-09-20 and 2025-09-27.
- Thailand Songs begins 2026-08-01. Requests for 2022 and 2024 resolve to that first week.
- Holiday and Songs of the Summer gaps are the off-season. Dance Club Songs ends 2020-03-28. Japan Hot 100's latest public week in this run is 2026-10-31. The Official U.K. Singles Chart's latest issue is 2026-11-14, one week ahead of the Hot 100. Several territory charts publish only 25 positions on the public page even when the chart name says Hot 100.

Charts whose public page lists fewer than 100 songs are kept in full as published.
That includes airplay charts (often 20–50 positions), Hits of the World (usually 25),
and some territory charts that still carry a Hot 100 name. See `notes` in `catalog.csv`.

## Included charts

| chart | region | weeks | first | last | rows | median positions | status |
| --- | --- | ---: | --- | --- | ---: | ---: | --- |
| hot-100 | United States | 463 | 2018-01-03 | 2026-11-07 | 46300 | 100 | done |
| streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| radio-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| digital-song-sales | United States | 463 | 2018-01-03 | 2026-11-07 | 19175 | 50 | done |
| bubbling-under-hot-100-singles | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| pop-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| adult-contemporary | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | done |
| adult-pop-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| country-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| country-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| country-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 27780 | 60 | done |
| rock-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| rock-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| hot-rock-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| rock-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| hot-alternative-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | done |
| alternative-streaming-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | done |
| alternative-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| hot-hard-rock-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | done |
| hard-rock-streaming-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | done |
| triple-a | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| hot-mainstream-rock-tracks | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| r-b-hip-hop-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| r-and-b-hip-hop-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| hot-r-and-b-hip-hop-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| r-and-b-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| r-and-b-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 6945 | 15 | done |
| rap-song | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| rap-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 6945 | 15 | done |
| hot-rap-tracks | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| mainstream-r-and-b-hip-hop | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| hot-adult-r-and-b-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | done |
| rhythmic-40 | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| latin-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| latin-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | done |
| latin-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| hot-regional-mexican-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | done |
| latin-regional-mexican-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| hot-latin-pop-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | done |
| latin-pop-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| hot-tropical-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | done |
| latin-tropical-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| hot-latin-rhythm-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | done |
| latin-rhythm-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| dance-electronic-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 20775 | 50 | done |
| hot-dance-pop-songs | United States | 95 | 2025-01-18 | 2026-11-07 | 1425 | 15 | done |
| hot-dance-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | done |
| dance-electronic-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 10625 | 25 | done |
| warm-global-dance-radio | Global | 35 | 2026-03-14 | 2026-11-07 | 1400 | 40 | done |
| dance-club-play-songs | United States | 118 | 2018-01-03 | 2020-03-28 | 6490 | 55 | done |
| christian-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23149 | 50 | done |
| christian-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| christian-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 21560 | 50 | done |
| hot-christian-adult-contemporary | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | done |
| gospel-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | done |
| gospel-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 6945 | 15 | done |
| gospel-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | done |
| jazz-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | done |
| hot-holiday-songs | United States | 45 | 2018-01-03 | 2026-01-03 | 4500 | 100 | done |
| holiday-streaming-songs | United States | 45 | 2018-01-03 | 2026-01-03 | 2250 | 50 | done |
| holiday-songs | United States | 45 | 2018-01-03 | 2026-01-03 | 2250 | 50 | done |
| summer-songs | United States | 126 | 2018-06-09 | 2026-09-12 | 2520 | 20 | done |
| billboard-u-s-afrobeats-songs | United States | 241 | 2022-04-02 | 2026-11-07 | 11975 | 50 | done |
| lyricfind-us | United States | 462 | 2018-01-03 | 2026-11-07 | 11550 | 25 | done |
| lyricfind-global | Global | 462 | 2018-01-03 | 2026-11-07 | 11550 | 25 | done |
| billboard-global-200 | Global | 321 | 2020-09-19 | 2026-11-07 | 64200 | 200 | done |
| billboard-global-excl-us | Global excluding United States | 321 | 2020-09-19 | 2026-11-07 | 64200 | 200 | done |
| the-arabic-hot-100 | Arabic (worldwide) | 150 | 2023-12-16 | 2026-10-31 | 3750 | 25 | done |
| billboard-argentina-hot-100 | Argentina | 417 | 2018-11-10 | 2026-11-07 | 10425 | 25 | done |
| billboard-brasil-hot-100 | Brazil | 167 | 2023-09-02 | 2026-11-07 | 4175 | 25 | done |
| canadian-hot-100 | Canada | 463 | 2018-01-03 | 2026-11-07 | 46300 | 100 | done |
| billboard-colombia-hot-100 | Colombia | 50 | 2025-11-15 | 2026-10-24 | 1250 | 25 | done |
| billboard-italy-hot-100 | Italy | 177 | 2023-06-17 | 2026-11-07 | 4425 | 25 | done |
| japan-hot-100 | Japan | 462 | 2018-01-03 | 2026-10-31 | 11550 | 25 | done |
| billboard-korea-global-k-songs | South Korea | 49 | 2025-12-06 | 2026-11-07 | 1225 | 25 | done |
| billboard-philippines-hot-100 | Philippines | 120 | 2024-07-06 | 2026-10-17 | 3000 | 25 | done |
| billboard-philippines-top-philippine-songs | Philippines | 120 | 2024-07-06 | 2026-10-17 | 3000 | 25 | done |
| billboard-vietnam-hot-100-songs | Vietnam | 75 | 2025-05-31 | 2026-10-31 | 1875 | 25 | done |
| billboard-vietnam-top-vietnamese-songs | Vietnam | 70 | 2025-06-28 | 2026-10-24 | 1750 | 25 | done |
| official-uk-songs | United Kingdom | 464 | 2018-01-03 | 2026-11-14 | 9280 | 20 | done |
| china-tme-uni-songs | China | 210 | 2022-11-05 | 2026-11-07 | 10500 | 50 | done |
| australia-songs-hotw | Australia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| austria-songs-hotw | Austria | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| belgium-songs-hotw | Belgium | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| bolivia-songs-hotw | Bolivia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| chile-songs-hotw | Chile | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| croatia-songs-hotw | Croatia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| czech-republic-songs-hotw | Czech Republic | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| denmark-songs-hotw | Denmark | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| ecuador-songs-hotw | Ecuador | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| finland-songs-hotw | Finland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| france-songs-hotw | France | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| germany-songs-hotw | Germany | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| greece-songs-hotw | Greece | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| hong-kong-songs-hotw | Hong Kong | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| hungary-songs-hotw | Hungary | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| iceland-songs-hotw | Iceland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| india-songs-hotw | India | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| indonesia-songs-hotw | Indonesia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| ireland-songs-hotw | Ireland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| luxembourg-songs-hotw | Luxembourg | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| malaysia-songs-hotw | Malaysia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| mexico-songs-hotw | Mexico | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| netherlands-songs-hotw | Netherlands | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| new-zealand-songs-hotw | New Zealand | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| norway-songs-hotw | Norway | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| peru-songs-hotw | Peru | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| poland-songs-hotw | Poland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| portugal-songs-hotw | Portugal | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| romania-songs-hotw | Romania | 247 | 2022-02-19 | 2026-11-07 | 6173 | 25 | done |
| singapore-songs-hotw | Singapore | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| slovakia-songs-hotw | Slovakia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| south-africa-songs-hotw | South Africa | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| spain-songs-hotw | Spain | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| sweden-songs-hotw | Sweden | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| switzerland-songs-hotw | Switzerland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| taiwan-songs-hotw | Taiwan | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| thailand-songs-hotw | Thailand | 15 | 2026-08-01 | 2026-11-07 | 375 | 25 | done |
| turkey-songs-hotw | Turkey | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |
| u-k-songs-hotw | United Kingdom | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | done |

## Skipped probe or empty charts

- `tiktok-billboard-top-50` (TikTok Billboard Top 50): probed historical slug; not_found: 404 for https://www.billboard.com/charts/tiktok-billboard-top-50/
- `heatseekers-songs` (Heatseekers Songs): probed slug has no song chart in the 2018-present window (page week 2014-11-29, rows 25)
- `country-digital-song-sales` (Country Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/country-digital-song-sales/
- `rock-digital-song-sales` (Rock Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/rock-digital-song-sales/
- `alternative-digital-song-sales` (Alternative Digital Song Sales): probed slug has no song chart in the 2018-present window
- `hard-rock-digital-song-sales` (Hard Rock Digital Song Sales Artists): probed slug has no song chart in the 2018-present window
- `r-and-b-hip-hop-digital-song-sales` (R&B/Hip-Hop Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/r-and-b-hip-hop-digital-song-sales/
- `rap-digital-song-sales` (Rap Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/rap-digital-song-sales/
- `latin-digital-song-sales` (Latin Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/latin-digital-song-sales/
- `dance-electronic-digital-song-sales` (Dance/Electronic Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/dance-electronic-digital-song-sales/
- `dance-mix-show-airplay` (Dance/Mix Show Airplay Artists): probed slug has no song chart in the 2018-present window
- `christian-digital-song-sales` (Christian Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/christian-digital-song-sales/
- `gospel-digital-song-sales` (Gospel Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/gospel-digital-song-sales/
- `world-digital-song-sales` (World Digital Song Sales): probed historical slug; not_found: 404 for https://www.billboard.com/charts/world-digital-song-sales/
- `kpop-hot-100` (K-Pop Hot 100): probed historical slug; not_found: 404 for https://www.billboard.com/charts/kpop-hot-100/
- `billboard-korea-100` (Billboard Korea 100): probed historical slug; not_found: 404 for https://www.billboard.com/charts/billboard-korea-100/
- `youtube-songs` (YouTube Songs): probed historical slug; not_found: 404 for https://www.billboard.com/charts/youtube-songs/
- `on-demand-streaming-songs` (On-Demand Streaming Songs): probed historical slug; not_found: 404 for https://www.billboard.com/charts/on-demand-streaming-songs/

