# Billboard weekly chart validation

Generated 2026-11-09T18:40:02+00:00.
Song-chart rows: 1370417.
These are recovered printed weeks, not a claim that every Billboard song chart since 2018 was collected.
Combined file: data/billboard/billboard_weekly_songs.csv.gz (16.9 MB, 1370417 rows).

## Coverage

Attempted song-chart statuses: done=57, partial=63, skipped=18
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
- Vietnam: 3650
- Colombia: 1250
- South Korea: 1225
- Thailand: 400

## Hot 100

Recovered Hot 100 printed weeks: 463 (2018-01-03 through 2026-11-07).
These are the dates printed on the parsed pages. Matching the Saturday grid plus 2018-01-03 describes that set; it is not an outside census of every chart Billboard published.
Saturday grid from 2018-01-06 through 2026-11-07, plus 2018-01-03: 463.
Printed dates missing from that grid: 0.
Printed dates outside that grid: 0.
2018-01-03 and 2018-01-06 are different lists: Juice is No. 93 on 3 Jan (last week 96, 3 weeks on chart) and No. 100 on 6 Jan (last week 93, 4 weeks on chart). Twelve songs share a rank. Perfect's weeks-on-chart go from 17 to 18.
Rows per week: min 100, median 100, max 100.
Duplicate-rank weeks: 0. Weeks with a hole in 1..max rank: 0. Rank uniqueness is not treated as proof of a correct snapshot.

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

- christian-songs: status done, coverage recovered_from_range_start, weeks 463, dup ranks 0, rank holes 1. Public page lists 49-50 positions across recovered weeks. Not a 100-position chart. 1 weeks are missing a rank in 1..max.
- thailand-songs-hotw: status partial, coverage unexplained_jump, weeks 16, dup ranks 0, rank holes 0. coverage unexplained_jump Launch evidence dates this chart at 2022-02-19. Earlier weeks are outside its life, not a missing archive. 1 unexplained gap(s) inside the recovered span. Hits of the World public page lists 25 positions. Not a 100-position chart. 1 gaps longer than 14 days.
- `coverage_since_2018=recovered_from_range_start` means the recovered printed weeks start by 2018-01-17 and have no internal gap over 14 days. It does not mean an external index was checked.
- `unknown_before_first_recovered` means the live site did not yield earlier issues. The first printed week is not a launch date unless `launch_evidence` says so.
- `source_url` in the CSV is the Billboard URL for the printed week. The Nov 9 scrape did not retain the request URL, final redirect URL, or HTTP timestamp for those files. Do not read `source_url` as a stored fetch log. Exceptions are recorded in `resolution_checks.json` and the Thailand 2022-02-19 cache file.

Thailand Songs launch evidence is the week of 19 Feb 2022 (Workpoint Today, 18 Feb 2022).
The live URL for 2022-02-19 currently prints 1 Aug 2026, so the live site is not an archive of that chart.
Internet Archive capture 20220215211337 of that URL prints Week of 19 Feb 2022, 25 songs, No. 1 Until Then by Tilly Birds.
That one week was added from the archive (fetched 2026-11-09T18:31:23Z). Availability API checks for 19 Mar 2022, 18 Jun 2022, 17 Dec 2022, 17 Jun 2023, 17 Feb 2024, 15 Feb 2025, and 25 Jul 2026 returned no snapshot.
A prefix CDX listing of every Thailand week timed out. The span from 26 Feb 2022 through 25 Jul 2026 was not recovered.
Both Vietnam charts launch 14 Jan 2022 according to Billboard's 11 Jan 2022 chart-beat article.
Requesting 2022-01-14 on the live site prints 31 May 2025 (Hot 100) and 28 Jun 2025 (Top Vietnamese Songs), which is where the recovered live series starts.
Wayback availability for those 2022 URLs, and for slug variants vietnam-hot-100, returned no snapshot. The 2022-to-2025 Vietnam issues were not recovered.
On 2026-11-09 the undated Top Vietnamese Songs page printed 31 Oct 2026, one week past the earlier scrape. That week was fetched the same day and added.
The same day's undated pages matched the saved last week for Hot 100 (7 Nov), Japan (31 Oct, 25 rows), Official U.K. (14 Nov, 20 rows), Arabic (31 Oct, 25 rows), both Philippines charts (17 Oct, 25 rows), Colombia (24 Oct, 25 rows), and Vietnam Hot 100 (31 Oct, 25 rows).
WARM Global Dance Radio's live URL for 1 Jun 2024 prints 14 Mar 2026. That first recovered week is not a documented launch.
Single missing issue dates were re-requested and resolved to the next saved week, not to the latest issue: LyricFind 26 May 2018, Argentina 19 Aug 2023, Italy 23 Sep 2023, Arabic 21 Feb 2026.
`full_100` is true only when every recovered week has 100 rows.
A 25-row Hits of the World chart, a 25-row Japan Hot 100 page, and a 20-row Official U.K. page are not full 100s.
Dance Club Songs: every recovered week has 55 rows, 118 weeks, 2018-01-03 through 2020-03-28. Bubbling Under: every recovered week has 25 rows, 463 weeks. Neither was re-checked against a printed magazine in this pass.
Those two counts describe the saved pages. They were not re-checked against a printed magazine.

Nine pairs of consecutive weeks repeat the same ranks, titles, and artists while last-week or weeks-on-chart changes.
No consecutive weeks repeat the full stat line. That argues against storing one HTTP response under two dates.
The pairs are Argentina Hot 100 around 12–26 Jan 2019, Philippines Top Philippine Songs 28 Feb–7 Mar 2026,
Gospel Streaming Songs 28 Sep–5 Oct 2024, LyricFind U.S. and Global at the ends of 2018 and 2019, and R&B Streaming Songs 17–24 Mar 2018.

## Included charts

| chart | region | weeks | first recovered | last recovered | rows | public depth | full 100 | coverage |
| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- |
| hot-100 | United States | 463 | 2018-01-03 | 2026-11-07 | 46300 | 100 | True | recovered_from_range_start |
| streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| radio-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| digital-song-sales | United States | 463 | 2018-01-03 | 2026-11-07 | 19175 | 50 | False | recovered_from_range_start |
| bubbling-under-hot-100-singles | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| pop-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| adult-contemporary | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | False | recovered_from_range_start |
| adult-pop-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| country-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| country-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| country-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 27780 | 60 | False | recovered_from_range_start |
| rock-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| rock-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| hot-rock-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| rock-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| hot-alternative-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | False | unknown_before_first_recovered |
| alternative-streaming-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | False | unknown_before_first_recovered |
| alternative-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| hot-hard-rock-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | False | unknown_before_first_recovered |
| hard-rock-streaming-songs | United States | 335 | 2020-06-13 | 2026-11-07 | 8375 | 25 | False | unknown_before_first_recovered |
| triple-a | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| hot-mainstream-rock-tracks | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| r-b-hip-hop-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| r-and-b-hip-hop-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| hot-r-and-b-hip-hop-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| r-and-b-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| r-and-b-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 6945 | 15 | False | recovered_from_range_start |
| rap-song | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| rap-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 6945 | 15 | False | recovered_from_range_start |
| hot-rap-tracks | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| mainstream-r-and-b-hip-hop | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| hot-adult-r-and-b-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | False | recovered_from_range_start |
| rhythmic-40 | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| latin-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| latin-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 23150 | 50 | False | recovered_from_range_start |
| latin-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| hot-regional-mexican-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | False | unknown_before_first_recovered |
| latin-regional-mexican-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| hot-latin-pop-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | False | unknown_before_first_recovered |
| latin-pop-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| hot-tropical-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | False | unknown_before_first_recovered |
| latin-tropical-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| hot-latin-rhythm-songs | United States | 83 | 2025-04-12 | 2026-11-07 | 2075 | 25 | False | unknown_before_first_recovered |
| latin-rhythm-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| dance-electronic-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 20775 | 50 | False | recovered_from_range_start |
| hot-dance-pop-songs | United States | 95 | 2025-01-18 | 2026-11-07 | 1425 | 15 | False | unknown_before_first_recovered |
| hot-dance-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 18520 | 40 | False | recovered_from_range_start |
| dance-electronic-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 10625 | 25 | False | recovered_from_range_start |
| warm-global-dance-radio | Global | 35 | 2026-03-14 | 2026-11-07 | 1400 | 40 | False | unknown_before_first_recovered |
| dance-club-play-songs | United States | 118 | 2018-01-03 | 2020-03-28 | 6490 | 55 | False | recovered_from_range_start |
| christian-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 23149 | 50 | False | recovered_from_range_start |
| christian-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| christian-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 21560 | 50 | False | recovered_from_range_start |
| hot-christian-adult-contemporary | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | False | recovered_from_range_start |
| gospel-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 11575 | 25 | False | recovered_from_range_start |
| gospel-streaming-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 6945 | 15 | False | recovered_from_range_start |
| gospel-airplay | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | False | recovered_from_range_start |
| jazz-songs | United States | 463 | 2018-01-03 | 2026-11-07 | 13890 | 30 | False | recovered_from_range_start |
| hot-holiday-songs | United States | 45 | 2018-01-03 | 2026-01-03 | 4500 | 100 | True | seasonal |
| holiday-streaming-songs | United States | 45 | 2018-01-03 | 2026-01-03 | 2250 | 50 | False | seasonal |
| holiday-songs | United States | 45 | 2018-01-03 | 2026-01-03 | 2250 | 50 | False | seasonal |
| summer-songs | United States | 126 | 2018-06-09 | 2026-09-12 | 2520 | 20 | False | seasonal |
| billboard-u-s-afrobeats-songs | United States | 241 | 2022-04-02 | 2026-11-07 | 11975 | 50 | False | unknown_before_first_recovered |
| lyricfind-us | United States | 462 | 2018-01-03 | 2026-11-07 | 11550 | 25 | False | recovered_from_range_start |
| lyricfind-global | Global | 462 | 2018-01-03 | 2026-11-07 | 11550 | 25 | False | recovered_from_range_start |
| billboard-global-200 | Global | 321 | 2020-09-19 | 2026-11-07 | 64200 | 200 | False | unknown_before_first_recovered |
| billboard-global-excl-us | Global excluding United States | 321 | 2020-09-19 | 2026-11-07 | 64200 | 200 | False | unknown_before_first_recovered |
| the-arabic-hot-100 | Arabic (worldwide) | 150 | 2023-12-16 | 2026-10-31 | 3750 | 25 | False | unknown_before_first_recovered |
| billboard-argentina-hot-100 | Argentina | 417 | 2018-11-10 | 2026-11-07 | 10425 | 25 | False | unknown_before_first_recovered |
| billboard-brasil-hot-100 | Brazil | 167 | 2023-09-02 | 2026-11-07 | 4175 | 25 | False | unknown_before_first_recovered |
| canadian-hot-100 | Canada | 463 | 2018-01-03 | 2026-11-07 | 46300 | 100 | True | recovered_from_range_start |
| billboard-colombia-hot-100 | Colombia | 50 | 2025-11-15 | 2026-10-24 | 1250 | 25 | False | unknown_before_first_recovered |
| billboard-italy-hot-100 | Italy | 177 | 2023-06-17 | 2026-11-07 | 4425 | 25 | False | unknown_before_first_recovered |
| japan-hot-100 | Japan | 462 | 2018-01-03 | 2026-10-31 | 11550 | 25 | False | recovered_from_range_start |
| billboard-korea-global-k-songs | South Korea | 49 | 2025-12-06 | 2026-11-07 | 1225 | 25 | False | unknown_before_first_recovered |
| billboard-philippines-hot-100 | Philippines | 120 | 2024-07-06 | 2026-10-17 | 3000 | 25 | False | unknown_before_first_recovered |
| billboard-philippines-top-philippine-songs | Philippines | 120 | 2024-07-06 | 2026-10-17 | 3000 | 25 | False | unknown_before_first_recovered |
| billboard-vietnam-hot-100-songs | Vietnam | 75 | 2025-05-31 | 2026-10-31 | 1875 | 25 | False | unknown_before_first_recovered |
| billboard-vietnam-top-vietnamese-songs | Vietnam | 71 | 2025-06-28 | 2026-10-31 | 1775 | 25 | False | unknown_before_first_recovered |
| official-uk-songs | United Kingdom | 464 | 2018-01-03 | 2026-11-14 | 9280 | 20 | False | recovered_from_range_start |
| china-tme-uni-songs | China | 210 | 2022-11-05 | 2026-11-07 | 10500 | 50 | False | unknown_before_first_recovered |
| australia-songs-hotw | Australia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| austria-songs-hotw | Austria | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| belgium-songs-hotw | Belgium | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| bolivia-songs-hotw | Bolivia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| chile-songs-hotw | Chile | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| croatia-songs-hotw | Croatia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| czech-republic-songs-hotw | Czech Republic | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| denmark-songs-hotw | Denmark | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| ecuador-songs-hotw | Ecuador | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| finland-songs-hotw | Finland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| france-songs-hotw | France | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| germany-songs-hotw | Germany | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| greece-songs-hotw | Greece | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| hong-kong-songs-hotw | Hong Kong | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| hungary-songs-hotw | Hungary | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| iceland-songs-hotw | Iceland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| india-songs-hotw | India | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| indonesia-songs-hotw | Indonesia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| ireland-songs-hotw | Ireland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| luxembourg-songs-hotw | Luxembourg | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| malaysia-songs-hotw | Malaysia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| mexico-songs-hotw | Mexico | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| netherlands-songs-hotw | Netherlands | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| new-zealand-songs-hotw | New Zealand | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| norway-songs-hotw | Norway | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| peru-songs-hotw | Peru | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| poland-songs-hotw | Poland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| portugal-songs-hotw | Portugal | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| romania-songs-hotw | Romania | 247 | 2022-02-19 | 2026-11-07 | 6173 | 25 | False | unknown_before_first_recovered |
| singapore-songs-hotw | Singapore | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| slovakia-songs-hotw | Slovakia | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| south-africa-songs-hotw | South Africa | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| spain-songs-hotw | Spain | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| sweden-songs-hotw | Sweden | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| switzerland-songs-hotw | Switzerland | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| taiwan-songs-hotw | Taiwan | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| thailand-songs-hotw | Thailand | 16 | 2022-02-19 | 2026-11-07 | 400 | 25 | False | unexplained_jump |
| turkey-songs-hotw | Turkey | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |
| u-k-songs-hotw | United Kingdom | 247 | 2022-02-19 | 2026-11-07 | 6175 | 25 | False | unknown_before_first_recovered |

## Skipped probe or empty charts

A live 404, or a page that resolves to a week before 2018, is not proof the slug never had a 2018-present chart. Internet Archive CDX lookups for these slugs timed out or were not available in this pass, so their history was not recovered.
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

