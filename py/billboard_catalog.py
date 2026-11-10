"""Billboard chart catalog used by the weekly scraper.

Slugs come from the public chart menu on billboard.com (fetched 2026-11-09)
plus a short list of archived song charts that are no longer linked from that
menu but still resolve. Album, artist, songwriter/producer, and all-time
rankings are recorded as skipped.
"""

from __future__ import annotations

# slug, chart name, region, category
SONG_CHARTS = [
    # All-genre United States
    ("hot-100", "Billboard Hot 100", "United States", "all-genre"),
    ("streaming-songs", "Streaming Songs", "United States", "all-genre"),
    ("radio-songs", "Radio Songs", "United States", "all-genre"),
    ("digital-song-sales", "Digital Song Sales", "United States", "all-genre"),
    ("bubbling-under-hot-100-singles", "Bubbling Under Hot 100", "United States", "all-genre"),
    # Pop
    ("pop-songs", "Pop Airplay", "United States", "pop"),
    ("adult-contemporary", "Adult Contemporary", "United States", "pop"),
    ("adult-pop-songs", "Adult Pop Airplay", "United States", "pop"),
    # Country
    ("country-songs", "Hot Country Songs", "United States", "country"),
    ("country-streaming-songs", "Country Streaming Songs", "United States", "country"),
    ("country-airplay", "Country Airplay", "United States", "country"),
    # Rock & alternative
    ("rock-songs", "Hot Rock & Alternative Songs", "United States", "rock"),
    ("rock-airplay", "Rock & Alternative Airplay", "United States", "rock"),
    ("hot-rock-songs", "Hot Rock Songs", "United States", "rock"),
    ("rock-streaming-songs", "Rock Streaming Songs", "United States", "rock"),
    ("hot-alternative-songs", "Hot Alternative Songs", "United States", "rock"),
    ("alternative-streaming-songs", "Alternative Streaming Songs", "United States", "rock"),
    ("alternative-airplay", "Alternative Airplay", "United States", "rock"),
    ("hot-hard-rock-songs", "Hot Hard Rock Songs", "United States", "rock"),
    ("hard-rock-streaming-songs", "Hard Rock Streaming Songs", "United States", "rock"),
    ("triple-a", "Adult Alternative Airplay", "United States", "rock"),
    ("hot-mainstream-rock-tracks", "Mainstream Rock Airplay", "United States", "rock"),
    # R&B / hip-hop
    ("r-b-hip-hop-songs", "Hot R&B/Hip-Hop Songs", "United States", "r&b/hip-hop"),
    ("r-and-b-hip-hop-streaming-songs", "R&B/Hip-Hop Streaming Songs", "United States", "r&b/hip-hop"),
    ("hot-r-and-b-hip-hop-airplay", "R&B/Hip-Hop Airplay", "United States", "r&b/hip-hop"),
    ("r-and-b-songs", "Hot R&B Songs", "United States", "r&b/hip-hop"),
    ("r-and-b-streaming-songs", "R&B Streaming Songs", "United States", "r&b/hip-hop"),
    ("rap-song", "Hot Rap Songs", "United States", "r&b/hip-hop"),
    ("rap-streaming-songs", "Rap Streaming Songs", "United States", "r&b/hip-hop"),
    ("hot-rap-tracks", "Rap Airplay", "United States", "r&b/hip-hop"),
    ("mainstream-r-and-b-hip-hop", "Mainstream R&B/Hip-Hop Airplay", "United States", "r&b/hip-hop"),
    ("hot-adult-r-and-b-airplay", "Adult R&B Airplay", "United States", "r&b/hip-hop"),
    ("rhythmic-40", "Rhythmic Airplay", "United States", "r&b/hip-hop"),
    # Latin
    ("latin-songs", "Hot Latin Songs", "United States", "latin"),
    ("latin-airplay", "Latin Airplay", "United States", "latin"),
    ("latin-streaming-songs", "Latin Streaming Songs", "United States", "latin"),
    ("hot-regional-mexican-songs", "Hot Regional Mexican Songs", "United States", "latin"),
    ("latin-regional-mexican-airplay", "Regional Mexican Airplay", "United States", "latin"),
    ("hot-latin-pop-songs", "Hot Latin Pop Songs", "United States", "latin"),
    ("latin-pop-airplay", "Latin Pop Airplay", "United States", "latin"),
    ("hot-tropical-songs", "Hot Tropical Songs", "United States", "latin"),
    ("latin-tropical-airplay", "Tropical Airplay", "United States", "latin"),
    ("hot-latin-rhythm-songs", "Hot Latin Rhythm Songs", "United States", "latin"),
    ("latin-rhythm-airplay", "Latin Rhythm Airplay", "United States", "latin"),
    # Dance / electronic
    ("dance-electronic-songs", "Hot Dance/Electronic Songs", "United States", "dance"),
    ("hot-dance-pop-songs", "Hot Dance/Pop Songs", "United States", "dance"),
    ("hot-dance-airplay", "Dance Airplay", "United States", "dance"),
    ("dance-electronic-streaming-songs", "Dance Streaming Songs", "United States", "dance"),
    ("warm-global-dance-radio", "WARM Global Dance Radio", "Global", "dance"),
    # Removed from the live menu; the archive still publishes through 2020-03-28.
    ("dance-club-play-songs", "Dance Club Songs", "United States", "dance"),
    # Christian / gospel / jazz
    ("christian-songs", "Hot Christian Songs", "United States", "christian"),
    ("christian-streaming-songs", "Christian Streaming Songs", "United States", "christian"),
    ("christian-airplay", "Christian Airplay", "United States", "christian"),
    ("hot-christian-adult-contemporary", "Christian AC Airplay", "United States", "christian"),
    ("gospel-songs", "Hot Gospel Songs", "United States", "gospel"),
    ("gospel-streaming-songs", "Gospel Streaming Songs", "United States", "gospel"),
    ("gospel-airplay", "Gospel Airplay", "United States", "gospel"),
    ("jazz-songs", "Smooth Jazz Airplay", "United States", "jazz"),
    # Seasonal song charts. Large gaps between seasons are expected.
    ("hot-holiday-songs", "Holiday 100", "United States", "holiday"),
    ("holiday-streaming-songs", "Holiday Streaming Songs", "United States", "holiday"),
    ("holiday-songs", "Holiday Airplay", "United States", "holiday"),
    ("summer-songs", "Songs of the Summer", "United States", "summer"),
    # Afrobeats and lyric charts
    ("billboard-u-s-afrobeats-songs", "Billboard U.S. Afrobeats Songs", "United States", "afrobeats"),
    ("lyricfind-us", "LyricFind U.S.", "United States", "lyric"),
    ("lyricfind-global", "LyricFind Global", "Global", "lyric"),
    # Global and territory Hot-100-style charts
    ("billboard-global-200", "Billboard Global 200", "Global", "global"),
    ("billboard-global-excl-us", "Billboard Global Excl. U.S.", "Global excluding United States", "global"),
    ("the-arabic-hot-100", "Billboard Arabic Hot 100", "Arabic (worldwide)", "international"),
    ("billboard-argentina-hot-100", "Billboard Argentina Hot 100", "Argentina", "international"),
    ("billboard-brasil-hot-100", "Billboard Brasil Hot 100", "Brazil", "international"),
    ("canadian-hot-100", "Billboard Canadian Hot 100", "Canada", "international"),
    ("billboard-colombia-hot-100", "Billboard Colombia Hot 100", "Colombia", "international"),
    ("billboard-italy-hot-100", "Billboard Italy Hot 100", "Italy", "international"),
    ("japan-hot-100", "Billboard Japan Hot 100", "Japan", "international"),
    ("billboard-korea-global-k-songs", "Billboard Korea Global K-Songs", "South Korea", "international"),
    ("billboard-philippines-hot-100", "Billboard Philippines Hot 100", "Philippines", "international"),
    ("billboard-philippines-top-philippine-songs", "Billboard Philippines Top Philippine Songs", "Philippines", "international"),
    ("billboard-vietnam-hot-100-songs", "Billboard Vietnam Hot 100", "Vietnam", "international"),
    ("billboard-vietnam-top-vietnamese-songs", "Billboard Vietnam Top Vietnamese Songs", "Vietnam", "international"),
    ("official-uk-songs", "The Official U.K. Singles Chart", "United Kingdom", "international"),
    ("china-tme-uni-songs", "China TME UNI Chart", "China", "international"),
    # Hits of the World song charts (Billboard's own territory rankings; usually 25 positions)
    ("australia-songs-hotw", "Australia Songs", "Australia", "hits-of-the-world"),
    ("austria-songs-hotw", "Austria Songs", "Austria", "hits-of-the-world"),
    ("belgium-songs-hotw", "Belgium Songs", "Belgium", "hits-of-the-world"),
    ("bolivia-songs-hotw", "Bolivia Songs", "Bolivia", "hits-of-the-world"),
    ("chile-songs-hotw", "Chile Songs", "Chile", "hits-of-the-world"),
    ("croatia-songs-hotw", "Croatia Songs", "Croatia", "hits-of-the-world"),
    ("czech-republic-songs-hotw", "Czech Republic Songs", "Czech Republic", "hits-of-the-world"),
    ("denmark-songs-hotw", "Denmark Songs", "Denmark", "hits-of-the-world"),
    ("ecuador-songs-hotw", "Ecuador Songs", "Ecuador", "hits-of-the-world"),
    ("finland-songs-hotw", "Finland Songs", "Finland", "hits-of-the-world"),
    ("france-songs-hotw", "France Songs", "France", "hits-of-the-world"),
    ("germany-songs-hotw", "Germany Songs", "Germany", "hits-of-the-world"),
    ("greece-songs-hotw", "Greece Songs", "Greece", "hits-of-the-world"),
    ("hong-kong-songs-hotw", "Hong Kong Songs", "Hong Kong", "hits-of-the-world"),
    ("hungary-songs-hotw", "Hungary Songs", "Hungary", "hits-of-the-world"),
    ("iceland-songs-hotw", "Iceland Songs", "Iceland", "hits-of-the-world"),
    ("india-songs-hotw", "India Songs", "India", "hits-of-the-world"),
    ("indonesia-songs-hotw", "Indonesia Songs", "Indonesia", "hits-of-the-world"),
    ("ireland-songs-hotw", "Ireland Songs", "Ireland", "hits-of-the-world"),
    ("luxembourg-songs-hotw", "Luxembourg Songs", "Luxembourg", "hits-of-the-world"),
    ("malaysia-songs-hotw", "Malaysia Songs", "Malaysia", "hits-of-the-world"),
    ("mexico-songs-hotw", "Mexico Songs", "Mexico", "hits-of-the-world"),
    ("netherlands-songs-hotw", "Netherlands Songs", "Netherlands", "hits-of-the-world"),
    ("new-zealand-songs-hotw", "New Zealand Songs", "New Zealand", "hits-of-the-world"),
    ("norway-songs-hotw", "Norway Songs", "Norway", "hits-of-the-world"),
    ("peru-songs-hotw", "Peru Songs", "Peru", "hits-of-the-world"),
    ("poland-songs-hotw", "Poland Songs", "Poland", "hits-of-the-world"),
    ("portugal-songs-hotw", "Portugal Songs", "Portugal", "hits-of-the-world"),
    ("romania-songs-hotw", "Romania Songs", "Romania", "hits-of-the-world"),
    ("singapore-songs-hotw", "Singapore Songs", "Singapore", "hits-of-the-world"),
    ("slovakia-songs-hotw", "Slovakia Songs", "Slovakia", "hits-of-the-world"),
    ("south-africa-songs-hotw", "South Africa Songs", "South Africa", "hits-of-the-world"),
    ("spain-songs-hotw", "Spain Songs", "Spain", "hits-of-the-world"),
    ("sweden-songs-hotw", "Sweden Songs", "Sweden", "hits-of-the-world"),
    ("switzerland-songs-hotw", "Switzerland Songs", "Switzerland", "hits-of-the-world"),
    ("taiwan-songs-hotw", "Taiwan Songs", "Taiwan", "hits-of-the-world"),
    ("thailand-songs-hotw", "Thailand Songs", "Thailand", "hits-of-the-world"),
    ("turkey-songs-hotw", "Turkey Songs", "Turkey", "hits-of-the-world"),
    ("u-k-songs-hotw", "U.K. Songs", "United Kingdom", "hits-of-the-world"),
]

# Archived or easily-missed song charts. Confirmed with one request before scraping.
# Independent launch notes. These are not inferred from the oldest Billboard URL
# that still resolves. Empty means this pass did not establish a launch date.
_GLOBAL_200 = (
    "2020-09-19",
    "Billboard, 14 Sep 2020: the first Billboard Global 200 and Billboard Global Excl. U.S. "
    "charts are dated 19 Sep 2020. Stored No. 1 songs match the article: WAP on Global 200 "
    "and Hawái on Global Excl. U.S. "
    "https://www.billboard.com/pro/billboard-launches-new-global-charts/",
)
_ROCK_2020 = (
    "2020-06-13",
    "Billboard, 10 Jun 2020: Hot Alternative Songs, Hot Hard Rock Songs, Alternative "
    "Streaming Songs and Hard Rock Streaming Songs debut on the chart dated 13 Jun 2020. "
    "Stored No. 1 songs match the article for the two Hot charts: Death Bed and Popular Monster. "
    "https://www.billboard.com/pro/hot-rock-alternative-songs-chart-revamped/",
)
_HOTW_PROGRAM = (
    "Billboard, 14 Feb 2022, says the new Hits of the World top-25 charts launch the next day, "
    "and the 15 Feb 2022 article dates the inaugural rankings 19 Feb 2022. "
    "https://www.billboard.com/music/chart-beat/billboard-hits-of-the-world-weekly-chart-announcement-1235031189/ "
    "https://www.billboard.com/music/chart-beat/gayle-glass-animals-bruno-top-billboards-new-hits-of-the-world-charts-1235032069/"
)
_HOTW_NAMED = {
    "australia-songs-hotw": "The 15 Feb 2022 article names Heat Waves at No. 1 in Australia, matching the stored week.",
    "slovakia-songs-hotw": "The 15 Feb 2022 article names Heat Waves at No. 1 in Slovakia, matching the stored week.",
    "austria-songs-hotw": "The 15 Feb 2022 article names abcdefu at No. 1 in Austria, matching the stored week.",
    "germany-songs-hotw": "The 15 Feb 2022 article names abcdefu at No. 1 in Germany, matching the stored week.",
    "luxembourg-songs-hotw": "The 15 Feb 2022 article names abcdefu at No. 1 in Luxembourg, matching the stored week.",
    "bolivia-songs-hotw": "The 15 Feb 2022 article names Desesperados at No. 1 in Bolivia, matching the stored week.",
    "ecuador-songs-hotw": "The 15 Feb 2022 article names Desesperados at No. 1 in Ecuador, matching the stored week.",
    "peru-songs-hotw": "The 15 Feb 2022 article names Desesperados at No. 1 in Peru, matching the stored week.",
    "iceland-songs-hotw": "The 15 Feb 2022 article names We Don't Talk About Bruno at No. 1 in Iceland, matching the stored week.",
    "ireland-songs-hotw": "The 15 Feb 2022 article names We Don't Talk About Bruno at No. 1 in Ireland, matching the stored week.",
    "u-k-songs-hotw": "The 15 Feb 2022 article names We Don't Talk About Bruno at No. 1 in the U.K., matching the stored week.",
    "portugal-songs-hotw": "The 15 Feb 2022 article names Malvadao 3 at No. 1 in Portugal, matching the stored week.",
    "india-songs-hotw": "Bandwagon, 17 Feb 2022, names Srivalli at No. 1 in India, matching the stored week.",
    "indonesia-songs-hotw": "Bandwagon, 17 Feb 2022, names Merasa Indah at No. 1 in Indonesia, matching the stored week.",
    "taiwan-songs-hotw": "Bandwagon, 17 Feb 2022, names Red Scarf at No. 1 in Taiwan, matching the stored week.",
}
_HOTW_SLUGS = [
    "australia-songs-hotw", "austria-songs-hotw", "belgium-songs-hotw", "bolivia-songs-hotw",
    "chile-songs-hotw", "croatia-songs-hotw", "czech-republic-songs-hotw", "denmark-songs-hotw",
    "ecuador-songs-hotw", "finland-songs-hotw", "france-songs-hotw", "germany-songs-hotw",
    "greece-songs-hotw", "hong-kong-songs-hotw", "hungary-songs-hotw", "iceland-songs-hotw",
    "india-songs-hotw", "indonesia-songs-hotw", "ireland-songs-hotw", "luxembourg-songs-hotw",
    "malaysia-songs-hotw", "mexico-songs-hotw", "netherlands-songs-hotw", "new-zealand-songs-hotw",
    "norway-songs-hotw", "peru-songs-hotw", "poland-songs-hotw", "portugal-songs-hotw",
    "romania-songs-hotw", "singapore-songs-hotw", "slovakia-songs-hotw", "south-africa-songs-hotw",
    "spain-songs-hotw", "sweden-songs-hotw", "switzerland-songs-hotw", "taiwan-songs-hotw",
    "turkey-songs-hotw", "u-k-songs-hotw",
]

LAUNCH_NOTES = {
    "billboard-vietnam-hot-100-songs": (
        "2022-01-14",
        "Billboard chart-beat article, 11 Jan 2022: Billboard Vietnam Hot 100 and "
        "Billboard Vietnam Top Vietnamese Songs launch Friday 14 Jan 2022. "
        "https://www.billboard.com/music/chart-beat/billboard-vietnam-charts-1235016406/",
    ),
    "billboard-vietnam-top-vietnamese-songs": (
        "2022-01-14",
        "Same Billboard article as the Vietnam Hot 100: both charts launch 14 Jan 2022. "
        "https://www.billboard.com/music/chart-beat/billboard-vietnam-charts-1235016406/",
    ),
    "thailand-songs-hotw": (
        "2022-02-19",
        "Workpoint Today, 18 Feb 2022: Thailand Songs debuts the week of 19 Feb 2022 "
        "as a 25-song chart, No. 1 Tilly Birds, 'Until Then'. "
        "https://www.workpointtoday.com/billboard-thailand-songs-1",
    ),
    "billboard-global-200": _GLOBAL_200,
    "billboard-global-excl-us": _GLOBAL_200,
    "hot-alternative-songs": _ROCK_2020,
    "hot-hard-rock-songs": _ROCK_2020,
    "alternative-streaming-songs": _ROCK_2020,
    "hard-rock-streaming-songs": _ROCK_2020,
    "billboard-u-s-afrobeats-songs": (
        "2022-04-02",
        "Billboard, 29 Mar 2022: the inaugural Billboard U.S. Afrobeats Songs chart is dated "
        "2 Apr 2022, with Love Nwantiti at No. 1. The stored week matches. "
        "https://www.billboard.com/music/chart-beat/ckays-love-nwantiti-tops-first-billboard-us-afrobeats-songs-chart-1235050658/",
    ),
    "billboard-italy-hot-100": (
        "2023-06-17",
        "The billboard.com page for 2023-06-17 still prints that week, and the top songs are "
        "marked NEW with one week and debut chart date 06/17/23. No earlier issue was recovered.",
    ),
    "billboard-brasil-hot-100": (
        "2023-09-02",
        "On 2026-11-10 the billboard.com URL for 2023-08-26 printed 2023-09-02, so no earlier "
        "billboard.com issue was stored. Wikipedia's 2023 Brazil number-one list, citing an "
        "archived Billboard Brasil page titled for the week of 28 Aug 2023, uses Monday dates "
        "five days before these Saturday issue dates, and the stored No. 1 songs match that list "
        "through 2023-10-07. That archive page was not opened in this pass.",
    ),
    "billboard-argentina-hot-100": (
        "2018-10-13",
        "Billboard Argentina, 12 Oct 2018, and Billboard, 17 Oct 2018: the first Argentina Hot 100 "
        "is the chart dated 13 Oct 2018, No. 1 Cuando Te Besé. The stored file begins 2018-11-10. "
        "On 2026-11-10 the URLs for 2018-10-13, 2018-10-20, 2018-10-27 and 2018-11-03 each printed "
        "2018-11-10, so those four issue dates were not recovered. "
        "https://www.billboard.com/pro/argentina-hot-100-chart-debuts-becky-g-paulo-londra/",
    ),
    "the-arabic-hot-100": (
        "2023-12-16",
        "SRMG, 14 Dec 2023, announced the Billboard Arabia Hot 100 with Kalam Eneih, "
        "El Watar Al Hassas and Ya Leil W Yal Ein at Nos. 1-3. The stored 2023-12-16 issue "
        "matches that ranking. https://www.srmg.com/en/article/billboard-arabia-launches-its-website-and-music-charts-creating-the-ultimate-destination-to-spotlight-and-discover-arab-artists-and-music",
    ),
    "billboard-philippines-hot-100": (
        "2024-07-06",
        "GMA News, 4 Jul 2024, and Billboard Philippines: the first Hot 100 issue is the week "
        "of 6 Jul 2024, led by Dilaw, Salamin Salamin and Please Please Please. The stored week matches.",
    ),
    "billboard-philippines-top-philippine-songs": (
        "2024-07-06",
        "Same launch as the Philippines Hot 100. The stored 2024-07-06 top three are Dilaw, "
        "Salamin, Salamin and Pantropiko, matching the contemporary reports.",
    ),
}
for _slug in _HOTW_SLUGS:
    _extra = _HOTW_NAMED.get(_slug, "This territory is not named individually in those two Billboard articles.")
    LAUNCH_NOTES[_slug] = ("2022-02-19", _HOTW_PROGRAM + " " + _extra)

# slug, fallback name, region, category
PROBE_CANDIDATES = [
    ("tiktok-billboard-top-50", "TikTok Billboard Top 50", "United States", "all-genre"),
    ("heatseekers-songs", "Heatseekers Songs", "United States", "all-genre"),
    ("country-digital-song-sales", "Country Digital Song Sales", "United States", "country"),
    ("rock-digital-song-sales", "Rock Digital Song Sales", "United States", "rock"),
    ("alternative-digital-song-sales", "Alternative Digital Song Sales", "United States", "rock"),
    ("hard-rock-digital-song-sales", "Hard Rock Digital Song Sales", "United States", "rock"),
    ("r-and-b-hip-hop-digital-song-sales", "R&B/Hip-Hop Digital Song Sales", "United States", "r&b/hip-hop"),
    ("rap-digital-song-sales", "Rap Digital Song Sales", "United States", "r&b/hip-hop"),
    ("latin-digital-song-sales", "Latin Digital Song Sales", "United States", "latin"),
    ("dance-electronic-digital-song-sales", "Dance/Electronic Digital Song Sales", "United States", "dance"),
    ("dance-mix-show-airplay", "Dance/Mix Show Airplay", "United States", "dance"),
    ("christian-digital-song-sales", "Christian Digital Song Sales", "United States", "christian"),
    ("gospel-digital-song-sales", "Gospel Digital Song Sales", "United States", "gospel"),
    ("world-digital-song-sales", "World Digital Song Sales", "United States", "world"),
    ("kpop-hot-100", "K-Pop Hot 100", "South Korea", "international"),
    ("billboard-korea-100", "Billboard Korea 100", "South Korea", "international"),
    ("youtube-songs", "YouTube Songs", "United States", "all-genre"),
    ("on-demand-streaming-songs", "On-Demand Streaming Songs", "United States", "all-genre"),
]

# slug, name, reason. These are charts on the public menu that this dataset does not collect.
SKIPPED_CHARTS = [
    ("billboard-200", "Billboard 200", "Album chart. This dataset is weekly song rankings (title and artist)."),
    ("top-album-sales", "Top Album Sales", "Album chart, not a song ranking."),
    ("top-streaming-albums", "Top Streaming Albums", "Album chart, not a song ranking."),
    ("independent-albums", "Independent Albums", "Album chart, not a song ranking."),
    ("vinyl-albums", "Vinyl Albums", "Album chart, not a song ranking."),
    ("indie-store-album-sales", "Indie Store Album Sales", "Album chart, not a song ranking."),
    ("canadian-albums", "Billboard Canadian Albums", "Album chart, not a song ranking."),
    ("billboard-italy-albums-top-100", "Billboard Italy Albums Top 100", "Album chart, not a song ranking."),
    ("official-uk-albums", "The Official U.K. Albums Chart", "Album chart, not a song ranking."),
    ("australian-albums", "Australia Albums", "Album chart, not a song ranking."),
    ("greece-albums", "Greece Albums", "Album chart, not a song ranking."),
    ("country-albums", "Top Country Albums", "Album chart, not a song ranking."),
    ("bluegrass-albums", "Bluegrass Albums", "Album chart, not a song ranking."),
    ("americana-folk-albums", "Americana/Folk Albums", "Album chart, not a song ranking."),
    ("top-rock-alternative-albums", "Top Rock & Alternative Albums", "Album chart, not a song ranking."),
    ("rock-albums", "Top Rock Albums", "Album chart, not a song ranking."),
    ("alternative-albums", "Top Alternative Albums", "Album chart, not a song ranking."),
    ("hard-rock-albums", "Top Hard Rock Albums", "Album chart, not a song ranking."),
    ("r-b-hip-hop-albums", "Top R&B/Hip-Hop Albums", "Album chart, not a song ranking."),
    ("r-and-b-albums", "Top R&B Albums", "Album chart, not a song ranking."),
    ("rap-albums", "Top Rap Albums", "Album chart, not a song ranking."),
    ("latin-albums", "Top Latin Albums", "Album chart, not a song ranking."),
    ("regional-mexican-albums", "Top Regional Mexican Albums", "Album chart, not a song ranking."),
    ("latin-pop-albums", "Top Latin Pop Albums", "Album chart, not a song ranking."),
    ("tropical-albums", "Top Tropical Albums", "Album chart, not a song ranking."),
    ("latin-rhythm-albums", "Top Latin Rhythm Albums", "Album chart, not a song ranking."),
    ("dance-electronic-albums", "Top Dance Albums", "Album chart, not a song ranking."),
    ("christian-albums", "Top Christian Albums", "Album chart, not a song ranking."),
    ("gospel-albums", "Top Gospel Albums", "Album chart, not a song ranking."),
    ("classical-albums", "Classical Albums", "Album chart, not a song ranking."),
    ("classical-crossover-albums", "Classical Crossover Albums", "Album chart, not a song ranking."),
    ("traditional-classic-albums", "Traditional Classical Albums", "Album chart, not a song ranking."),
    ("jazz-albums", "Jazz Albums", "Album chart, not a song ranking."),
    ("contemporary-jazz", "Contemporary Jazz Albums", "Album chart, not a song ranking."),
    ("traditional-jazz-albums", "Traditional Jazz Albums", "Album chart, not a song ranking."),
    ("world-albums", "World Albums", "Album chart, not a song ranking."),
    ("holiday-albums", "Top Holiday Albums", "Album chart, not a song ranking."),
    ("cast-albums", "Cast Albums", "Album chart, not a song ranking."),
    ("soundtracks", "Soundtracks", "Album chart, not a song ranking."),
    ("blues-albums", "Blues Albums", "Album chart, not a song ranking."),
    ("comedy-albums", "Comedy Albums", "Album chart, not a song ranking."),
    ("kids-albums", "Kid Albums", "Album chart, not a song ranking."),
    ("new-age-albums", "New Age/Ambient Albums", "Album chart, not a song ranking."),
    ("reggae-albums", "Reggae Albums", "Album chart, not a song ranking."),
    ("artist-100", "Artist 100", "Artist ranking, not a song list."),
    ("emerging-artists", "Emerging Artists", "Artist ranking, not a song list."),
    ("top-arabic-artist-100", "Billboard Arabic Artist 100", "Artist ranking, not a song list."),
    ("hot-100-songwriters", "Hot 100 Songwriters", "Songwriter credit chart, not a song list."),
    ("hot-100-producers", "Hot 100 Producers", "Producer credit chart, not a song list."),
    ("country-songwriters", "Country Songwriters", "Songwriter credit chart, not a song list."),
    ("country-producers", "Country Producers", "Producer credit chart, not a song list."),
    ("rock-alternative-songwriters", "Rock & Alternative Songwriters", "Songwriter credit chart, not a song list."),
    ("rock-alternative-producers", "Rock & Alternative Producers", "Producer credit chart, not a song list."),
    ("rock-songwriters", "Rock Songwriters", "Songwriter credit chart, not a song list."),
    ("rock-producers", "Rock Producers", "Producer credit chart, not a song list."),
    ("alternative-songwriters", "Alternative Songwriters", "Songwriter credit chart, not a song list."),
    ("alternative-producers", "Alternative Producers", "Producer credit chart, not a song list."),
    ("hard-rock-songwriters", "Hard Rock Songwriters", "Songwriter credit chart, not a song list."),
    ("hard-rock-producers", "Hard Rock Producers", "Producer credit chart, not a song list."),
    ("rb-hip-hop-songwriters", "R&B/Hip-Hop Songwriters", "Songwriter credit chart, not a song list."),
    ("rb-hip-hop-producers", "R&B/Hip-Hop Producers", "Producer credit chart, not a song list."),
    ("rb-songwriters", "R&B Songwriters", "Songwriter credit chart, not a song list."),
    ("rb-producers", "R&B Producers", "Producer credit chart, not a song list."),
    ("rap-songwriters", "Rap Songwriters", "Songwriter credit chart, not a song list."),
    ("rap-producers", "Rap Producers", "Producer credit chart, not a song list."),
    ("latin-songwriters", "Latin Songwriters", "Songwriter credit chart, not a song list."),
    ("latin-producers", "Latin Producers", "Producer credit chart, not a song list."),
    ("dance-electronic-songwriters", "Dance/Electronic Songwriters", "Songwriter credit chart, not a song list."),
    ("dance-electronic-producers", "Dance/Electronic Producers", "Producer credit chart, not a song list."),
    ("dance-pop-songwriters", "Dance/Pop Songwriters", "Songwriter credit chart, not a song list."),
    ("dance-pop-producers", "Dance/Pop Producers", "Producer credit chart, not a song list."),
    ("christian-songwriters", "Christian Songwriters", "Songwriter credit chart, not a song list."),
    ("christian-producers", "Christian Producers", "Producer credit chart, not a song list."),
    ("gospel-songwriters", "Gospel Songwriters", "Songwriter credit chart, not a song list."),
    ("gospel-producers", "Gospel Producers", "Producer credit chart, not a song list."),
    ("holiday-100-songwriters", "Holiday 100 Songwriters", "Songwriter credit chart, not a song list."),
    ("holiday-100-producers", "Holiday 100 Producers", "Producer credit chart, not a song list."),
    ("greatest-of-all-time-artists", "Greatest of All Time Artists", "All-time ranking, not a weekly chart."),
    ("greatest-hot-100-singles", "Greatest of All Time Hot 100 Songs", "All-time ranking, not a weekly chart."),
    ("greatest-hot-100-artists", "Greatest of All Time Hot 100 Artists", "All-time ranking, not a weekly chart."),
    ("greatest-billboard-200-albums", "Greatest of All Time Billboard 200 Albums", "All-time album ranking, not a weekly song chart."),
    ("greatest-billboard-200-artists", "Greatest of All Time Billboard 200 Artists", "All-time ranking, not a weekly chart."),
    ("top-artists-of-the-21st-century", "Top Artists of the 21st Century", "Era ranking, not a weekly chart."),
    ("top-hot-100-songs-of-the-21st-century", "Top Hot 100 Songs of the 21st Century", "Era ranking, not a weekly chart."),
    ("top-billboard-200-albums-of-the-21st-century", "Top Billboard 200 Albums of the 21st Century", "Era album ranking, not a weekly song chart."),
    ("top-women-artists-of-the-21st-century", "Top Women Artists of the 21st Century", "Era ranking, not a weekly chart."),
    ("greatest-hot-100-women-artists", "Greatest of All Time Hot 100 Women Artists", "All-time ranking, not a weekly chart."),
    ("greatest-hot-100-songs-by-women", "Greatest of All Time Hot 100 Songs by Women", "All-time ranking, not a weekly chart."),
    ("greatest-billboard-200-women-artists", "Greatest of All Time Billboard 200 Women Artists", "All-time ranking, not a weekly chart."),
    ("greatest-billboard-200-albums-by-women", "Greatest of All Time Billboard 200 Albums by Women", "All-time album ranking, not a weekly song chart."),
    ("greatest-billboards-top-songs-80s", "Greatest of All Time Songs of the '80s", "Era ranking, not a weekly chart."),
    ("greatest-billboards-top-songs-90s", "Greatest of All Time Songs of the '90s", "Era ranking, not a weekly chart."),
    ("greatest-of-all-time-holiday-100-songs", "Greatest of All Time Holiday 100 Songs", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-top-holiday-albums", "Greatest of All Time Top Holiday Albums", "All-time album ranking, not a weekly song chart."),
    ("greatest-of-all-time-songs-of-the-summer", "Greatest of All Time Songs of the Summer", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-hot-100-no-2-hits", "Greatest of All Time Hot 100 No. 2 Hits", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-pop-songs-artists", "Greatest of All Time Pop Songs Artists", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-pop-songs", "Greatest of All Time Pop Songs", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-adult-contemporary-artists", "Greatest of All Time Adult Contemporary Artists", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-adult-contemporary-songs", "Greatest of All Time Adult Contemporary Songs", "All-time ranking, not a weekly chart."),
    ("greatest-adult-pop-artists", "Greatest of All Time Adult Pop Songs Artists", "All-time ranking, not a weekly chart."),
    ("greatest-adult-pop-songs", "Greatest of All Time Adult Pop Songs", "All-time ranking, not a weekly chart."),
    ("greatest-country-artists", "Greatest of All Time Top Country Artists", "All-time ranking, not a weekly chart."),
    ("greatest-country-songs", "Greatest of All Time Hot Country Songs", "All-time ranking, not a weekly chart."),
    ("greatest-country-albums", "Greatest of All Time Top Country Albums", "All-time album ranking, not a weekly song chart."),
    ("top-country-artists-of-the-21st-century", "Top Country Artists of the 21st Century", "Era ranking, not a weekly chart."),
    ("top-hot-country-songs-of-the-21st-century", "Top Hot Country Songs of the 21st Century", "Era ranking, not a weekly chart."),
    ("top-country-albums-of-the-21st-century", "Top Country Albums of the 21st Century", "Era album ranking, not a weekly song chart."),
    ("greatest-r-b-hip-hop-artists", "Greatest of All Time Top R&B/Hip-Hop Artists", "All-time ranking, not a weekly chart."),
    ("greatest-r-b-hip-hop-songs", "Greatest of All Time Hot R&B/Hip-Hop Songs", "All-time ranking, not a weekly chart."),
    ("greatest-r-b-hip-hop-albums", "Greatest of All Time Top R&B/Hip-Hop Albums", "All-time album ranking, not a weekly song chart."),
    ("top-rb-hip-hop-artists-of-the-21st-century", "Top R&B/Hip-Hop Artists of the 21st Century", "Era ranking, not a weekly chart."),
    ("top-rb-hip-hop-albums-of-the-21st-century", "Top R&B/Hip-Hop Albums of the 21st Century", "Era album ranking, not a weekly song chart."),
    ("top-rb-hip-hop-songs-of-the-21st-century", "Top Hot R&B/Hip-Hop Songs of the 21st Century", "Era ranking, not a weekly chart."),
    ("greatest-alternative-artists", "Greatest of All Time Alternative Artists", "All-time ranking, not a weekly chart."),
    ("greatest-alternative-songs", "Greatest of All Time Alternative Songs", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-adult-alternative-artists", "Greatest of All Time Adult Alternative Artists", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-adult-alternative-songs", "Greatest of All Time Adult Alternative Songs", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-mainstream-rock-artists", "Greatest of All Time Mainstream Rock Artists", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-mainstream-rock-songs", "Greatest of All Time Mainstream Rock Songs", "All-time ranking, not a weekly chart."),
    ("greatest-of-all-time-latin-artists", "Greatest of All Time Latin Artists", "All-time ranking, not a weekly chart."),
    ("greatest-hot-latin-songs-artists", "Greatest of All Time Hot Latin Songs Artists", "All-time ranking, not a weekly chart."),
    ("greatest-hot-latin-songs", "Greatest of All Time Hot Latin Songs", "All-time ranking, not a weekly chart."),
    ("top-latin-artists-of-the-21st-century", "Top Latin Artists of the 21st Century", "Era ranking, not a weekly chart."),
    ("top-latin-albums-of-the-21st-century", "Top Latin Albums of the 21st Century", "Era album ranking, not a weekly song chart."),
    ("top-latin-songs-of-the-21st-century", "Top Hot Latin Songs of the 21st Century", "Era ranking, not a weekly chart."),
    ("greatest-top-dance-club-artists", "Greatest of All Time Top Dance Club Artists", "All-time ranking, not a weekly chart."),
]

