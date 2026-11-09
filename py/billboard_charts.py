"""Download weekly Billboard song charts from the public chart pages.

The historical scraper in this repo read ``div.chart-list-item`` attributes
that Billboard no longer serves, and it only covered the Hot 100. Chart pages
now render ``ul.o-chart-results-list-row`` entries. This script walks every
selected song chart from the first chart week of 2018 (2018-01-03) through
the latest week Billboard is publishing for that chart.

Requests are rate-limited, retried with backoff, and cached as one JSON file
per chart-week so a stopped run continues without refetching. Login walls,
paywalls, and anti-bot challenges are not bypassed: a block stops that chart
and, if it persists, stops the run.

Usage (from the repository root):

    python py/billboard_charts.py scrape
    python py/billboard_charts.py export
    python py/billboard_charts.py validate
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))

from billboard_catalog import (  # noqa: E402
    LAUNCH_NOTES,
    PROBE_CANDIDATES,
    SKIPPED_CHARTS,
    SONG_CHARTS,
)

RANGE_START = date(2018, 1, 3)
# A normal next issue is 7 days. 14 days still fits the one-off Wednesday
# chart plus one unpublished Saturday. Longer moves are not treated as
# "the next issue" unless the chart is seasonal.
MAX_NEXT_ISSUE_DAYS = 14
SEASONAL_CATEGORIES = frozenset({"holiday", "summer"})
USER_AGENT = (
    "LyricsRepetition-billboard-charts/1.0 "
    "(research dataset; modest rate; +https://github.com/)"
)
COLUMNS = [
    "chart",
    "region",
    "category",
    "chart_name",
    "week",
    "rank",
    "title",
    "artist",
    "last_week",
    "peak_position",
    "weeks_on_chart",
    "weeks_at_number_one",
    "is_new",
    "is_reentry",
    "source_url",
]

# title substring, artist substring. Artist text is whatever Billboard prints.
SPOT_CHECKS = [
    ("hot-100", "2018-01-03", 1, "Perfect", "Ed Sheeran"),
    ("hot-100", "2018-01-06", 1, "Perfect", "Ed Sheeran"),
    ("hot-100", "2018-01-06", 100, "Juice", "Yo Gotti"),
    ("hot-100", "2018-02-03", 1, "God's Plan", "Drake"),
    ("hot-100", "2026-11-07", 1, "Choosin' Texas", "Ella Langley"),
    ("pop-songs", "2018-01-06", 1, "Havana", "Camila Cabello"),
    ("canadian-hot-100", "2018-01-06", 1, "Perfect", "Ed Sheeran"),
    ("official-uk-songs", "2018-01-06", 1, "Perfect", "Ed Sheeran"),
    ("billboard-global-200", "2020-09-19", 1, "WAP", "Cardi B"),
]


class FetchError(Exception):
    def __init__(self, kind: str, message: str, status: int | None = None):
        super().__init__(message)
        self.kind = kind
        self.status = status


@dataclass
class ChartSpec:
    slug: str
    name: str
    region: str
    category: str


@dataclass
class ParsedChart:
    week: date | None
    chart_name: str
    rows: list[dict]
    final_url: str = ""
    requested_url: str = ""
    fetched_at: str | None = None


def classify_advance(cursor: date, printed: date | None, category: str) -> str:
    """Classify a step from a recovered issue to the next printed week.

    ``accept`` is a normal next issue (at most 14 days). ``hiatus`` is a longer
    gap on a seasonal chart. ``unexplained`` is a longer gap on any other chart:
    the live site sometimes resolves an old URL to a much later issue, and that
    must not be treated as proof the weeks in between were unpublished.
    ``reject`` means the page did not move forward.
    """
    if printed is None or printed <= cursor:
        return "reject"
    gap_days = (printed - cursor).days
    if gap_days <= MAX_NEXT_ISSUE_DAYS:
        return "accept"
    if category in SEASONAL_CATEGORIES:
        return "hiatus"
    return "unexplained"


def assess_coverage(weeks: list[date], category: str, range_start: date = RANGE_START) -> dict:
    """Describe what a recovered week list does, and does not, establish."""
    ordered = sorted(weeks)
    jumps = []
    hiatuses = []
    for left, right in zip(ordered, ordered[1:]):
        kind = classify_advance(left, right, category)
        record = {
            "after": left.isoformat(),
            "next_recovered": right.isoformat(),
            "gap_days": (right - left).days,
        }
        if kind == "unexplained":
            jumps.append(record)
        elif kind == "hiatus":
            hiatuses.append(record)
    leading = None
    if ordered and category not in SEASONAL_CATEGORIES:
        gap_days = (ordered[0] - range_start).days
        if gap_days > MAX_NEXT_ISSUE_DAYS:
            leading = {
                "range_start": range_start.isoformat(),
                "first_recovered": ordered[0].isoformat(),
                "gap_days": gap_days,
            }
    if not ordered:
        label = "not_recovered"
    elif category in SEASONAL_CATEGORIES:
        label = "seasonal"
    elif jumps:
        label = "unexplained_jump"
    elif leading:
        label = "unknown_before_first_recovered"
    else:
        label = "recovered_from_range_start"
    return {
        "label": label,
        "unexplained_jumps": jumps,
        "seasonal_hiatuses": hiatuses,
        "leading_unrecovered": leading,
        "claim_complete_since_2018": label == "recovered_from_range_start",
    }


@dataclass
class RateLimiter:
    min_interval: float
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _next: float = 0.0
    requests: int = 0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            delay = max(0.0, self._next - now)
            self._next = max(now, self._next) + self.min_interval
            self.requests += 1
        if delay:
            time.sleep(delay)


def clean(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\xa0", " ").split())


def parse_week_heading(text: str) -> date | None:
    text = clean(text)
    if not text.startswith("Week of "):
        return None
    try:
        return datetime.strptime(text[len("Week of ") :], "%B %d, %Y").date()
    except ValueError:
        return None


def _parse_stat_label(label: str) -> tuple[int | None, int | None, int | None, int | None] | None:
    """Return last week, peak, weeks on chart, weeks at No. 1.

    Billboard prints the numbers inside the stat label (``LW 1 PEAK 1 ...``).
    The separate digit nodes are not reliable siblings of that label.
    """
    with_top = re.search(
        r"LW\s+(\d+|-)\s+PEAK\s+(\d+|-)\s+WEEKS AT NO\. 1\s+(\d+|-)\s+WEEKS ON CHART\s+(\d+|-)",
        label,
    )
    if with_top:
        last_week, peak, weeks_at_one, weeks = with_top.groups()
        return (_blank_int(last_week), _blank_int(peak), _blank_int(weeks), _blank_int(weeks_at_one))
    plain = re.search(r"LW\s+(\d+|-)\s+PEAK\s+(\d+|-)\s+WEEKS ON CHART\s+(\d+|-)", label)
    if plain:
        last_week, peak, weeks = plain.groups()
        return (_blank_int(last_week), _blank_int(peak), _blank_int(weeks), None)
    return None


def _blank_int(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if value in {"", "-"}:
        return None
    if re.fullmatch(r"\d+", value):
        return int(value)
    return None


def parse_chart_html(html: str, final_url: str = "") -> ParsedChart:
    """Parse a Billboard chart page. Rows follow the public list only."""
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.select_one("h1")
    chart_name = clean(h1.get_text(" ", strip=True) if h1 else "")
    week = None
    for heading in soup.find_all("h2"):
        week = parse_week_heading(heading.get_text(" ", strip=True))
        if week:
            break

    rows: list[dict] = []
    seen_ranks: set[int] = set()
    for row in soup.select("ul.o-chart-results-list-row"):
        cells = row.find_all("li", recursive=False)
        if not cells:
            continue
        rank_text = clean(cells[0].get_text(" ", strip=True))
        rank_match = re.search(r"\d+", rank_text)
        if not rank_match:
            continue
        rank = int(rank_match.group())
        if rank in seen_ranks:
            continue
        seen_ranks.add(rank)

        badge = clean(cells[2].get_text(" ", strip=True)) if len(cells) > 2 else ""
        badge_key = badge.replace(" ", "").replace("-", "").upper()
        rank_key = rank_text.replace(" ", "").replace("-", "").upper()
        is_reentry = "REENTRY" in badge_key or "REENTRY" in rank_key
        is_new = (not is_reentry) and ("NEW" in badge_key or rank_text.upper().endswith("NEW"))

        title_el = row.select_one("h3#title-of-a-story")
        artist_el = row.select_one("span.a-no-trucate")
        title = clean(title_el.get_text(" ", strip=True) if title_el else "")
        artist = clean(artist_el.get_text(" ", strip=True) if artist_el else "")

        last_week = peak = weeks = weeks_at_one = None
        container = row.select_one("li.a-chart-result-item-container")
        if container:
            for item in container.select("ul > li"):
                label = clean(item.get_text(" ", strip=True))
                if not label.startswith("LW"):
                    continue
                parsed_stats = _parse_stat_label(label)
                if parsed_stats is None:
                    continue
                last_week, peak, weeks, weeks_at_one = parsed_stats
                break

        image = ""
        img = row.select_one("img")
        if img:
            image = img.get("src") or img.get("data-src") or ""

        rows.append(
            {
                "rank": rank,
                "title": title,
                "artist": artist,
                "last_week": last_week,
                "peak_position": peak,
                "weeks_on_chart": weeks,
                "weeks_at_number_one": weeks_at_one,
                "is_new": is_new,
                "is_reentry": is_reentry,
                "image_url": image,
            }
        )

    rows.sort(key=lambda item: item["rank"])
    return ParsedChart(week=week, chart_name=chart_name, rows=rows, final_url=final_url)


def chart_url(slug: str, week: date | None = None) -> str:
    if week is None:
        return f"https://www.billboard.com/charts/{slug}/"
    return f"https://www.billboard.com/charts/{slug}/{week.isoformat()}/"


def fetch_html(session: requests.Session, url: str, limiter: RateLimiter, stop: threading.Event) -> tuple[str, str]:
    """GET a chart page via curl so a stalled connection cannot hang the run.

    ``requests`` timeouts were not interrupting reads that sat in poll. curl's
    ``--max-time`` is a hard limit, and the subprocess timeout is a second one.
    The ``session`` argument is unused; callers still pass one.
    """
    del session
    backoff = 2.0
    last_error = "request failed"
    marker = b"\n__BB_META__ "
    for attempt in range(6):
        if stop.is_set():
            raise FetchError("stopped", "stop requested before request")
        limiter.wait()
        command = [
            "curl",
            "-sS",
            "--compressed",
            "--location",
            "--connect-timeout",
            "15",
            "--max-time",
            "40",
            "-A",
            USER_AGENT,
            "-H",
            "Accept: text/html,application/xhtml+xml",
            "-H",
            "Accept-Language: en-US,en;q=0.9",
            "-w",
            "\n__BB_META__ %{http_code} %{url_effective}",
            url,
        ]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                timeout=50,
                check=False,
            )
        except subprocess.TimeoutExpired:
            last_error = f"timeout for {url}"
            if attempt == 5:
                raise FetchError("network", last_error)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue
        if completed.returncode != 0 and not completed.stdout:
            last_error = completed.stderr.decode("utf-8", "replace")[:300] or f"curl exit {completed.returncode}"
            if attempt == 5:
                raise FetchError("network", last_error)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue
        raw = completed.stdout
        split_at = raw.rfind(marker)
        if split_at < 0:
            last_error = f"curl response missing status for {url}"
            if attempt == 5:
                raise FetchError("network", last_error)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue
        meta = raw[split_at + len(marker) :].decode("utf-8", "replace").strip().split(" ", 1)
        try:
            status = int(meta[0])
        except (IndexError, ValueError):
            last_error = f"bad curl status for {url}"
            if attempt == 5:
                raise FetchError("network", last_error)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue
        final_url = meta[1] if len(meta) > 1 else url
        text = raw[:split_at].decode("utf-8", "replace")
        if status == 404:
            raise FetchError("not_found", f"404 for {url}", 404)
        if status in {401, 403, 429}:
            last_error = f"HTTP {status} for {url}"
            if attempt >= 2:
                raise FetchError("blocked", last_error, status)
            time.sleep(20 * (attempt + 1))
            continue
        if status >= 500:
            last_error = f"HTTP {status} for {url}"
            if attempt == 5:
                raise FetchError("http", last_error, status)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue
        if status != 200:
            raise FetchError("http", f"HTTP {status} for {url}", status)
        head = text[:8000].lower()
        if "cf-challenge" in head or ("just a moment" in head and "cloudflare" in head):
            raise FetchError("blocked", f"anti-bot challenge for {url}", status)
        if "captcha" in head and "chart-results" not in text and "o-chart-results-list-row" not in text:
            raise FetchError("blocked", f"captcha interstitial for {url}", status)
        return text, final_url
    raise FetchError("network", last_error)


class Store:
    def __init__(self, root: Path):
        self.root = root
        self.cache = root / "cache"
        self.weekly = root / "weekly"
        self.cache.mkdir(parents=True, exist_ok=True)
        self.weekly.mkdir(parents=True, exist_ok=True)
        self.log_path = root / "scrape.log"
        self.progress_path = root / "progress.json"
        self._log_lock = threading.Lock()

    def log(self, message: str) -> None:
        line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {message}"
        with self._log_lock:
            print(line, flush=True)
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def chart_dir(self, slug: str) -> Path:
        path = self.cache / slug
        path.mkdir(parents=True, exist_ok=True)
        return path

    def state_path(self, slug: str) -> Path:
        return self.chart_dir(slug) / "_state.json"

    def week_path(self, slug: str, week: date) -> Path:
        return self.chart_dir(slug) / f"{week.isoformat()}.json"

    def load_state(self, slug: str) -> dict:
        path = self.state_path(slug)
        if not path.exists():
            return {"slug": slug, "status": "new", "weeks": [], "error": ""}
        return json.loads(path.read_text(encoding="utf-8"))

    def save_state(self, state: dict) -> None:
        state["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        path = self.state_path(state["slug"])
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
        temporary.replace(path)

    def save_week(self, spec: ChartSpec, parsed: ParsedChart) -> None:
        if parsed.week is None:
            return
        list_key = [
            [
                row.get("rank"),
                row.get("title"),
                row.get("artist"),
                row.get("last_week"),
                row.get("peak_position"),
                row.get("weeks_on_chart"),
                row.get("weeks_at_number_one"),
            ]
            for row in parsed.rows
        ]
        payload = {
            "chart": spec.slug,
            "region": spec.region,
            "category": spec.category,
            "chart_name": parsed.chart_name or spec.name,
            "week": parsed.week.isoformat(),
            "source_url": chart_url(spec.slug, parsed.week),
            "requested_url": parsed.requested_url,
            "final_url": parsed.final_url,
            "fetched_at": parsed.fetched_at,
            "list_sha256": hashlib.sha256(
                json.dumps(list_key, ensure_ascii=False).encode()
            ).hexdigest(),
            "rows": parsed.rows,
        }
        path = self.week_path(spec.slug, parsed.week)
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        temporary.replace(path)

    def has_week(self, slug: str, week: date) -> bool:
        return self.week_path(slug, week).exists()

    def write_progress(self, payload: dict) -> None:
        temporary = self.progress_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temporary.replace(self.progress_path)


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    return session


def _cached_chart(store: Store, slug: str, week: date) -> ParsedChart | None:
    """Return a cached chart only when the file is the printed week ``week``.

    A file stored under a probe date but containing a later printed week would
    hide a redirect. Those files are ignored so the probe is fetched again.
    """
    path = store.week_path(slug, week)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    printed = payload.get("week")
    if printed != week.isoformat():
        return None
    return ParsedChart(
        week=date.fromisoformat(printed),
        chart_name=payload.get("chart_name") or "",
        rows=payload.get("rows") or [],
        final_url=payload.get("final_url") or payload.get("source_url") or "",
        requested_url=payload.get("requested_url") or "",
        fetched_at=payload.get("fetched_at"),
    )


def load_parsed(session, url, limiter, stop, spec_name: str) -> ParsedChart:
    html, final_url = fetch_html(session, url, limiter, stop)
    parsed = parse_chart_html(html, final_url)
    if parsed.chart_name == "":
        parsed.chart_name = spec_name
    parsed.requested_url = url
    parsed.final_url = final_url or parsed.final_url
    parsed.fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return parsed


def remember_week(store: Store, spec: ChartSpec, state: dict, parsed: ParsedChart) -> bool:
    """Persist a chart week. Returns True when the week was not already stored."""
    if parsed.week is None or not parsed.rows:
        return False
    iso = parsed.week.isoformat()
    fresh = iso not in state["weeks"]
    if fresh or not store.has_week(spec.slug, parsed.week):
        store.save_week(spec, parsed)
    if fresh:
        state["weeks"].append(iso)
        state["chart_name"] = parsed.chart_name or spec.name
        store.save_state(state)
    return fresh


def _fetch_chart(session, store, spec, limiter, stop, probe: date, fetcher):
    cached = _cached_chart(store, spec.slug, probe)
    if cached is not None:
        return cached
    url = chart_url(spec.slug, probe)
    if fetcher is not None:
        parsed = fetcher(url)
    else:
        parsed = load_parsed(session, url, limiter, stop, spec.name)
    if parsed.requested_url == "":
        parsed.requested_url = url
    return parsed


def next_published_week(
    session,
    store: Store,
    spec: ChartSpec,
    limiter: RateLimiter,
    stop: threading.Event,
    cursor: date,
    end: date,
    fetcher=None,
) -> tuple[ParsedChart | None, str]:
    """Find the next issue after ``cursor``.

    Returns ``(chart, decision)``. ``decision`` is one of ``accept``,
    ``hiatus``, ``unexplained``, or ``reject``. A redirect that lands on a
    much later issue, including the latest issue, is ``unexplained`` unless
    the chart is seasonal. The probe list does not include the latest date
    itself, so a failed step cannot skip straight to the end and look complete.
    """
    del end  # latest date is not a probe; callers compare after a real step
    offsets = []
    for offset in (1, 7, 14):
        if offset not in offsets:
            offsets.append(offset)
    parsed = None
    for offset in offsets:
        if stop.is_set():
            raise FetchError("stopped", "stop requested")
        probe = cursor + timedelta(days=offset)
        try:
            parsed = _fetch_chart(session, store, spec, limiter, stop, probe, fetcher)
        except FetchError as exc:
            if exc.kind in {"blocked", "stopped"}:
                raise
            store.log(f"{spec.slug} probe {probe} failed ({exc.kind}): {exc}")
            continue
        decision = classify_advance(cursor, parsed.week, spec.category)
        if decision in {"accept", "hiatus"}:
            return parsed, decision
        if decision == "unexplained" and parsed.week is not None:
            closer = _closer_issue(session, store, spec, limiter, stop, cursor, parsed, fetcher)
            if closer is not None:
                closer_decision = classify_advance(cursor, closer.week, spec.category)
                if closer_decision in {"accept", "hiatus"}:
                    return closer, closer_decision
                parsed = closer
            return parsed, "unexplained"
    return parsed, "reject"


def _closer_issue(session, store, spec, limiter, stop, cursor: date, far: ParsedChart, fetcher):
    """If a probe jumped far ahead, look for an issue strictly in between.

    When the midpoint resolves to the same distant week, the archive is not
    serving the interval. That is left as an unexplained jump.
    """
    if far.week is None:
        return None
    found = far
    hi = far.week
    for _ in range(6):
        if stop.is_set():
            raise FetchError("stopped", "stop requested")
        gap_days = (hi - cursor).days
        if gap_days <= MAX_NEXT_ISSUE_DAYS:
            return found
        mid = cursor + timedelta(days=gap_days // 2)
        if mid <= cursor or mid >= hi:
            return found
        try:
            parsed = _fetch_chart(session, store, spec, limiter, stop, mid, fetcher)
        except FetchError as exc:
            if exc.kind in {"blocked", "stopped"}:
                raise
            store.log(f"{spec.slug} midpoint {mid} failed ({exc.kind}): {exc}")
            return found
        if parsed.week and cursor < parsed.week < hi:
            found = parsed
            hi = parsed.week
            continue
        return found
    return found


def _apply_coverage(state: dict, spec: ChartSpec, end: date | None) -> None:
    weeks = [date.fromisoformat(value) for value in state.get("weeks") or []]
    coverage = assess_coverage(weeks, spec.category)
    state["coverage_since_2018"] = coverage["label"]
    state["unexplained_jumps"] = coverage["unexplained_jumps"]
    state["claim_complete_since_2018"] = coverage["claim_complete_since_2018"]
    last = max(weeks) if weeks else None
    if last is None:
        if state.get("status") not in {"failed", "skipped"}:
            state["status"] = "failed"
            state["error"] = state.get("error") or "walk produced no weeks"
        return
    if end is not None and last < end:
        state["status"] = "incomplete"
        state["error"] = f"stopped at {last.isoformat()} before latest {end.isoformat()}"
        return
    if coverage["label"] == "unexplained_jump":
        state["status"] = "partial"
        state["error"] = "unexplained forward jump; intervening weeks were not recovered"
        return
    if coverage["label"] == "unknown_before_first_recovered":
        state["status"] = "partial"
        state["error"] = (
            "weeks before the first recovered issue were not recovered; "
            "the first printed week is not evidence of the chart's launch"
        )
        return
    state["status"] = "done"
    state["error"] = ""


def scrape_one(
    spec: ChartSpec,
    store: Store,
    limiter: RateLimiter,
    stop: threading.Event,
    max_weeks: int | None,
    fetcher=None,
) -> dict:
    session = make_session()
    state = store.load_state(spec.slug)
    state.setdefault("weeks", [])
    state.setdefault("error", "")
    state["name"] = spec.name
    state["region"] = spec.region
    state["category"] = spec.category

    def get_url(url: str) -> ParsedChart:
        if fetcher is not None:
            parsed = fetcher(url)
            if parsed.requested_url == "":
                parsed.requested_url = url
            return parsed
        return load_parsed(session, url, limiter, stop, spec.name)

    if stop.is_set():
        state["status"] = state.get("status") or "stopped"
        store.save_state(state)
        return state

    try:
        latest = get_url(chart_url(spec.slug))
    except FetchError as exc:
        state["status"] = "failed" if exc.kind != "not_found" else "skipped"
        state["error"] = f"{exc.kind}: {exc}"
        store.save_state(state)
        store.log(f"{spec.slug} stopped on latest page: {state['error']}")
        return state

    if latest.week is None or not latest.rows:
        state["status"] = "skipped"
        state["error"] = "Billboard did not return a chart list for the current URL."
        store.save_state(state)
        store.log(f"{spec.slug} skipped: {state['error']}")
        return state

    if latest.week < RANGE_START:
        state["status"] = "skipped"
        state["error"] = (
            f"Last published week is {latest.week.isoformat()}, before {RANGE_START.isoformat()}."
        )
        state["latest"] = latest.week.isoformat()
        store.save_state(state)
        store.log(f"{spec.slug} skipped: {state['error']}")
        return state

    end = latest.week
    state["latest"] = end.isoformat()
    state["positions_last"] = len(latest.rows)
    # Cache the latest issue, but do not append it ahead of the chronological walk.
    store.save_week(spec, latest)

    if state["weeks"]:
        last_saved = max(date.fromisoformat(value) for value in state["weeks"])
        if last_saved >= end:
            _apply_coverage(state, spec, end)
            store.save_state(state)
            store.log(
                f"{spec.slug} already current through {last_saved.isoformat()} "
                f"({len(state['weeks'])} weeks, {state['coverage_since_2018']})"
            )
            return state
        store.log(f"{spec.slug} updating {last_saved.isoformat()} -> {end.isoformat()}")

    if not state["weeks"] or date.fromisoformat(min(state["weeks"])) > end:
        state["weeks"] = []

    if not state["weeks"]:
        parsed = _first_week_in_range(session, store, spec, limiter, stop, end, fetcher)
        if parsed is None:
            state["status"] = "skipped"
            state["error"] = f"No published week from {RANGE_START.isoformat()} through {end.isoformat()}."
            store.save_state(state)
            store.log(f"{spec.slug} skipped: {state['error']}")
            return state
        remember_week(store, spec, state, parsed)
        store.log(
            f"{spec.slug} first week {parsed.week.isoformat()} "
            f"({len(parsed.rows)} positions) latest {end.isoformat()}"
        )

    cursor = date.fromisoformat(state["weeks"][-1])
    added = 0
    while cursor < end:
        if max_weeks is not None and len(state["weeks"]) >= max_weeks:
            state["status"] = "partial"
            state["error"] = f"stopped at --max-weeks {max_weeks}"
            store.save_state(state)
            store.log(f"{spec.slug} {state['error']}")
            return state
        parsed, decision = next_published_week(
            session, store, spec, limiter, stop, cursor, end, fetcher
        )
        if decision == "reject" or parsed is None or parsed.week is None or parsed.week <= cursor:
            break
        if decision == "unexplained":
            state.setdefault("jump_log", []).append(
                {
                    "after": cursor.isoformat(),
                    "resolved_week": parsed.week.isoformat(),
                    "requested_url": parsed.requested_url,
                    "final_url": parsed.final_url,
                    "fetched_at": parsed.fetched_at,
                }
            )
            store.log(
                f"{spec.slug} unexplained jump after {cursor.isoformat()} "
                f"to printed {parsed.week.isoformat()}"
            )
        fresh = remember_week(store, spec, state, parsed)
        cursor = parsed.week
        if cursor > end:
            end = cursor
            state["latest"] = end.isoformat()
            store.save_state(state)
        if fresh:
            added += 1
            if added % 25 == 0:
                store.log(f"{spec.slug} {cursor.isoformat()} weeks={len(state['weeks'])} rows={len(parsed.rows)}")

    state["positions_last"] = len(latest.rows)
    _apply_coverage(state, spec, end)
    store.save_state(state)
    last = max(state["weeks"]) if state["weeks"] else "-"
    store.log(
        f"{spec.slug} {state['status']} weeks={len(state['weeks'])} "
        f"coverage={state.get('coverage_since_2018')} last={last} ({state['error']})"
    )
    return state


def _first_week_in_range(session, store, spec, limiter, stop, end: date, fetcher=None) -> ParsedChart | None:
    probe = RANGE_START
    best: ParsedChart | None = None
    for _ in range(6):
        parsed = _fetch_chart(session, store, spec, limiter, stop, probe, fetcher)
        if parsed.week is None or not parsed.rows:
            return best
        if RANGE_START <= parsed.week <= end:
            return parsed
        if parsed.week < RANGE_START:
            probe = parsed.week + timedelta(days=1)
            continue
        # Jumped past `end`. Keep the earliest in-range page if we already saw one.
        if best is None or (parsed.week and best.week and parsed.week < best.week):
            if parsed.week <= end + timedelta(days=14):
                best = parsed
        return best
    return best


def probe_extra_charts(store: Store, limiter: RateLimiter, stop: threading.Event) -> list[ChartSpec]:
    found: list[ChartSpec] = []
    known = {slug for slug, *_ in SONG_CHARTS}
    session = make_session()
    for slug, name, region, category in PROBE_CANDIDATES:
        if slug in known:
            continue
        try:
            parsed = load_parsed(session, chart_url(slug), limiter, stop, name)
        except FetchError as exc:
            store.log(f"probe {slug} not included ({exc.kind}): {exc}")
            store.save_state(
                {
                    "slug": slug,
                    "status": "skipped",
                    "weeks": [],
                    "error": f"probed historical slug; {exc.kind}: {exc}",
                    "name": name,
                    "region": region,
                    "category": category,
                }
            )
            continue
        final_slug = ""
        if parsed.final_url:
            parts = [part for part in parsed.final_url.rstrip("/").split("/") if part]
            if "charts" in parts:
                final_slug = parts[parts.index("charts") + 1]
        if final_slug in known or final_slug in {item.slug for item in found}:
            store.log(f"probe {slug} redirects to existing chart {final_slug}; skipping alias")
            continue
        if parsed.week is None or not parsed.rows or parsed.week < RANGE_START:
            reason = "probed slug has no song chart in the 2018-present window"
            if parsed.week:
                reason += f" (page week {parsed.week.isoformat()}, rows {len(parsed.rows)})"
            store.log(f"probe {slug} skipped: {reason}")
            store.save_state(
                {
                    "slug": slug,
                    "status": "skipped",
                    "weeks": [],
                    "error": reason,
                    "name": parsed.chart_name or name,
                    "region": region,
                    "category": category,
                }
            )
            continue
        if "album" in (parsed.chart_name or name).lower():
            store.log(f"probe {slug} skipped: page is an album chart ({parsed.chart_name})")
            continue
        spec = ChartSpec(slug, parsed.chart_name or name, region, category)
        found.append(spec)
        store.log(
            f"probe {slug} included as {spec.name!r} "
            f"latest {parsed.week.isoformat()} positions {len(parsed.rows)}"
        )
    return found


def selected_charts(only: set[str] | None, extras: list[ChartSpec]) -> list[ChartSpec]:
    charts = [ChartSpec(*item) for item in SONG_CHARTS]
    charts.extend(extras)
    if only:
        charts = [chart for chart in charts if chart.slug in only]
    return charts


def scrape(args: argparse.Namespace) -> None:
    root = Path(args.data_dir)
    store = Store(root)
    limiter = RateLimiter(args.interval)
    stop = threading.Event()
    only = set(args.only.split(",")) if args.only else None
    extras: list[ChartSpec] = []
    if not args.skip_probe and (only is None or any(slug in only for slug, *_rest in PROBE_CANDIDATES)):
        extras = probe_extra_charts(store, limiter, stop)
        if only:
            extras = [chart for chart in extras if chart.slug in only]
    charts = selected_charts(only, extras)
    store.log(f"scraping {len(charts)} charts interval={args.interval}s workers={args.workers}")

    results = []
    blocks = {"count": 0}
    block_lock = threading.Lock()

    def runner(spec: ChartSpec) -> dict:
        if stop.is_set():
            return {"slug": spec.slug, "status": "stopped", "error": "run stopped after a block"}
        try:
            state = scrape_one(spec, store, limiter, stop, args.max_weeks)
        except FetchError as exc:
            state = store.load_state(spec.slug)
            state["slug"] = spec.slug
            state["status"] = "failed"
            state["error"] = f"{exc.kind}: {exc}"
            state.setdefault("weeks", [])
            store.save_state(state)
            store.log(f"{spec.slug} failed: {state['error']}")
        except Exception as exc:  # noqa: BLE001 — keep the rest of the run going
            state = store.load_state(spec.slug)
            state["slug"] = spec.slug
            state["status"] = "failed"
            state["error"] = f"error: {exc}"
            state.setdefault("weeks", [])
            store.save_state(state)
            store.log(f"{spec.slug} failed: {exc}")
        if str(state.get("error", "")).startswith("blocked") or "anti-bot" in str(state.get("error", "")):
            with block_lock:
                blocks["count"] += 1
                if blocks["count"] >= 2:
                    stop.set()
                    store.log("stopping the run after repeated blocks")
        elif state.get("status") == "done":
            with block_lock:
                blocks["count"] = 0
        store.write_progress(
            {
                "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "requests": limiter.requests,
                "finished_slug": spec.slug,
                "status": state.get("status"),
                "weeks": len(state.get("weeks") or []),
            }
        )
        return state

    workers = max(1, args.workers)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(runner, spec) for spec in charts]
        for future in as_completed(futures):
            results.append(future.result())

    done = sum(1 for item in results if item.get("status") == "done")
    store.log(f"scrape finished charts={len(results)} done={done} http_requests={limiter.requests}")
    if not args.skip_export:
        export_and_validate(root)


def _week_files(cache: Path, slug: str) -> list[Path]:
    directory = cache / slug
    if not directory.exists():
        return []
    return sorted(path for path in directory.glob("????-??-??.json"))


def _load_week(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _median(values: list[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _depth_note(slug: str, chart_name: str, counts: list[int], full_100: bool) -> str:
    if not counts:
        return ""
    lo, hi = min(counts), max(counts)
    if full_100:
        return "Every recovered week has 100 positions on the public page."
    if slug == "official-uk-songs":
        return (
            f"The Official U.K. Singles Chart is a 100-song chart. "
            f"Billboard's public page lists {lo} positions in every recovered week, not 100."
            if lo == hi
            else f"The Official U.K. Singles Chart public page lists {lo}-{hi} positions, not 100."
        )
    hot100_name = "hot-100" in slug or "Hot 100" in (chart_name or "")
    if hot100_name and hi < 100:
        span = str(lo) if lo == hi else f"{lo}-{hi}"
        return (
            f"Public page lists {span} positions. This is not a recovered 100-position chart."
        )
    if slug.endswith("-hotw"):
        span = str(lo) if lo == hi else f"{lo}-{hi}"
        return f"Hits of the World public page lists {span} positions. Not a 100-position chart."
    if "global-200" in slug or "global-excl" in slug:
        return f"Public page lists {lo if lo == hi else f'{lo}-{hi}'} positions."
    if lo == hi:
        return f"Public page lists {lo} positions in every recovered week. Not a 100-position chart."
    return f"Public page lists {lo}-{hi} positions across recovered weeks. Not a 100-position chart."


def expected_hot100_weeks(last: date) -> list[date]:
    """Hot 100 issue dates: the one-off Wednesday chart, then Saturdays."""
    weeks = [RANGE_START]
    cursor = date(2018, 1, 6)
    while cursor <= last:
        weeks.append(cursor)
        cursor += timedelta(days=7)
    return weeks


def export_and_validate(root: Path) -> None:
    root = Path(root)
    cache = root / "cache"
    weekly = root / "weekly"
    weekly.mkdir(parents=True, exist_ok=True)
    catalog_rows = []
    stats = []
    total_rows = 0
    combined_path = root / "billboard_weekly_songs.csv.gz"
    combined = gzip.open(combined_path, "wt", encoding="utf-8", newline="")
    combined_writer = csv.DictWriter(combined, fieldnames=COLUMNS, extrasaction="ignore")
    combined_writer.writeheader()

    seen_slugs = set()
    for slug, name, region, category in SONG_CHARTS:
        seen_slugs.add(slug)
        catalog_rows.append(_export_chart(cache, weekly, combined_writer, slug, name, region, category, stats))
    for slug, name, region, category in PROBE_CANDIDATES:
        state_path = cache / slug / "_state.json"
        if slug in seen_slugs or not state_path.exists():
            continue
        seen_slugs.add(slug)
        catalog_rows.append(_export_chart(cache, weekly, combined_writer, slug, name, region, category, stats))

    for slug, name, reason in SKIPPED_CHARTS:
        catalog_rows.append(
            {
                "chart": slug,
                "chart_name": name,
                "region": "",
                "category": "",
                "status": "skipped",
                "reason": reason,
                "first_week": "",
                "last_week": "",
                "weeks": 0,
                "rows": 0,
                "min_rows": "",
                "median_rows": "",
                "max_rows": "",
                "gap_count": "",
                "notes": "Not a weekly song chart in this collection.",
                "launch_date": "",
                "launch_evidence": "",
                "coverage_since_2018": "not_applicable",
                "claim_complete_since_2018": False,
                "public_depth": "",
                "full_100": False,
                "depth_note": "",
            }
        )

    combined.close()
    for item in stats:
        total_rows += item["rows"]

    catalog_path = root / "catalog.csv"
    with catalog_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catalog_rows[0].keys()))
        writer.writeheader()
        writer.writerows(catalog_rows)

    combined_size = combined_path.stat().st_size
    if combined_size > 95 * 1024 * 1024:
        combined_path.unlink()
        combined_note = (
            f"The combined CSV was {combined_size / 1e6:.1f} MB gzipped, over the git file limit, "
            "so it was left out. Use the per-chart files in data/billboard/weekly/."
        )
    else:
        combined_note = (
            f"Combined file: data/billboard/billboard_weekly_songs.csv.gz "
            f"({combined_size / 1e6:.1f} MB, {total_rows} rows)."
        )

    report = _validation_report(root, stats, catalog_rows, total_rows, combined_note)
    report_path = root / "VALIDATION.md"
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"wrote {catalog_path} and {report_path}")


def _export_chart(cache, weekly, combined_writer, slug, name, region, category, stats) -> dict:
    state_path = cache / slug / "_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    files = _week_files(cache, slug)
    status = state.get("status") or ("done" if files else "missing")
    reason = state.get("error") or ""
    if not files:
        return {
            "chart": slug,
            "chart_name": state.get("chart_name") or state.get("name") or name,
            "region": region,
            "category": category,
            "status": status,
            "reason": reason,
            "first_week": "",
            "last_week": "",
            "weeks": 0,
            "rows": 0,
            "min_rows": "",
            "median_rows": "",
            "max_rows": "",
            "gap_count": "",
            "notes": "",
            "launch_date": "",
            "launch_evidence": "",
            "coverage_since_2018": "not_recovered",
            "claim_complete_since_2018": False,
            "public_depth": "",
            "full_100": False,
            "depth_note": "",
        }

    out_path = weekly / f"{slug}.csv.gz"
    counts = []
    gaps = []
    dup_ranks = 0
    missing_ranks = 0
    row_count = 0
    weeks = []
    chart_name = name
    with gzip.open(out_path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        previous = None
        for path in files:
            payload = _load_week(path)
            chart_name = payload.get("chart_name") or chart_name
            week = date.fromisoformat(payload["week"])
            weeks.append(week)
            if previous is not None:
                delta = (week - previous).days
                if delta not in {3, 7}:
                    gaps.append((previous.isoformat(), week.isoformat(), delta))
            previous = week
            ranks = [row["rank"] for row in payload["rows"]]
            if len(ranks) != len(set(ranks)):
                dup_ranks += 1
            if ranks:
                expected = set(range(1, max(ranks) + 1))
                if set(ranks) != expected:
                    missing_ranks += 1
            counts.append(len(payload["rows"]))
            for row in payload["rows"]:
                record = {
                    "chart": slug,
                    "region": payload.get("region") or region,
                    "category": payload.get("category") or category,
                    "chart_name": chart_name,
                    "week": payload["week"],
                    "rank": row["rank"],
                    "title": row["title"],
                    "artist": row["artist"],
                    "last_week": "" if row["last_week"] is None else row["last_week"],
                    "peak_position": "" if row["peak_position"] is None else row["peak_position"],
                    "weeks_on_chart": "" if row["weeks_on_chart"] is None else row["weeks_on_chart"],
                    "weeks_at_number_one": ""
                    if row["weeks_at_number_one"] is None
                    else row["weeks_at_number_one"],
                    "is_new": "true" if row["is_new"] else "false",
                    "is_reentry": "true" if row["is_reentry"] else "false",
                    "source_url": payload.get("source_url") or chart_url(slug, week),
                }
                writer.writerow(record)
                combined_writer.writerow(record)
                row_count += 1

    notes = []
    coverage = assess_coverage(weeks, category)
    if coverage["label"] != "recovered_from_range_start":
        notes.append(f"coverage {coverage['label']}")
    launch_date = LAUNCH_NOTES.get(slug, ("", ""))[0]
    if coverage["leading_unrecovered"]:
        leading = coverage["leading_unrecovered"]
        if launch_date and launch_date == leading["first_recovered"]:
            notes.append(
                f"Launch evidence dates this chart at {launch_date}. "
                "Earlier weeks are outside its life, not a missing archive."
            )
        else:
            notes.append(
                f"No recovered issue from {leading['range_start']} until {leading['first_recovered']}. "
                "That first printed week is not evidence of the launch date."
            )
    if launch_date and weeks and weeks[0].isoformat() != launch_date:
        notes.append(
            f"Independent launch evidence is {launch_date}. "
            "Issues from that date until the first recovered week were not recovered."
        )
    if coverage["unexplained_jumps"]:
        notes.append(
            f"{len(coverage['unexplained_jumps'])} unexplained gap(s) inside the recovered span."
        )
    median_rows = _median(counts)
    full_100 = bool(counts) and min(counts) == 100 and max(counts) == 100
    depth_note = _depth_note(slug, chart_name, counts, full_100)
    if depth_note:
        notes.append(depth_note)
    if category in {"holiday", "summer"}:
        notes.append("Seasonal chart: multi-week gaps between seasons are expected.")
    if dup_ranks:
        notes.append(f"{dup_ranks} weeks have duplicate ranks.")
    if missing_ranks:
        notes.append(f"{missing_ranks} weeks are missing a rank in 1..max.")
    long_gaps = [gap for gap in gaps if gap[2] > 14]
    if long_gaps and category not in {"holiday", "summer"}:
        notes.append(f"{len(long_gaps)} gaps longer than 14 days.")

    if coverage["label"] in {"unexplained_jump", "unknown_before_first_recovered"}:
        status = "partial"
    stats.append(
        {
            "chart": slug,
            "chart_name": chart_name,
            "region": region,
            "category": category,
            "status": status,
            "coverage": coverage["label"],
            "weeks": weeks,
            "counts": counts,
            "gaps": gaps,
            "rows": row_count,
            "dup_ranks": dup_ranks,
            "missing_ranks": missing_ranks,
            "notes": notes,
        }
    )
    return {
        "chart": slug,
        "chart_name": chart_name,
        "region": region,
        "category": category,
        "status": status,
        "reason": reason,
        "first_week": weeks[0].isoformat(),
        "last_week": weeks[-1].isoformat(),
        "weeks": len(weeks),
        "rows": row_count,
        "min_rows": min(counts),
        "median_rows": median_rows,
        "max_rows": max(counts),
        "gap_count": len(gaps),
        "notes": " ".join(notes),
        "launch_date": LAUNCH_NOTES.get(slug, ("", ""))[0],
        "launch_evidence": LAUNCH_NOTES.get(slug, ("", ""))[1],
        "coverage_since_2018": coverage["label"],
        "claim_complete_since_2018": coverage["claim_complete_since_2018"],
        "public_depth": median_rows if median_rows is not None else "",
        "full_100": full_100,
        "depth_note": depth_note,
    }


def _spot_checks(cache: Path) -> list[str]:
    lines = []
    for slug, week, rank, title, artist in SPOT_CHECKS:
        path = cache / slug / f"{week}.json"
        if not path.exists():
            lines.append(f"- FAIL {slug} {week} rank {rank}: week file missing")
            continue
        payload = _load_week(path)
        match = next((row for row in payload["rows"] if row["rank"] == rank), None)
        if match is None:
            lines.append(f"- FAIL {slug} {week} rank {rank}: rank missing ({len(payload['rows'])} rows)")
            continue
        ok = title.lower() in match["title"].lower() and artist.lower() in match["artist"].lower()
        flag = "OK" if ok else "FAIL"
        lines.append(
            f"- {flag} {slug} {week} #{rank}: {match['title']} — {match['artist']} "
            f"(expected {title} / {artist})"
        )
    return lines


def _validation_report(root: Path, stats: list[dict], catalog_rows: list[dict], total_rows: int, combined_note: str) -> str:
    cache = root / "cache"
    included = [row for row in catalog_rows if row["status"] in {"done", "incomplete", "partial", "failed"} or row["rows"]]
    skipped = [row for row in catalog_rows if row["status"] == "skipped" and not row["rows"]]
    by_status = Counter(row["status"] for row in catalog_rows if row["rows"] or row["status"] != "skipped")
    # status counter over attempted song charts only
    attempted = [row for row in catalog_rows if row["chart"] not in {slug for slug, *_ in SKIPPED_CHARTS}]
    status_counts = Counter(row["status"] for row in attempted)

    hot = next((item for item in stats if item["chart"] == "hot-100"), None)
    hot_lines = ["Hot 100 was not scraped."]
    if hot and hot["weeks"]:
        expected = expected_hot100_weeks(hot["weeks"][-1])
        have = set(hot["weeks"])
        missing = [day.isoformat() for day in expected if day not in have]
        extra = [day.isoformat() for day in hot["weeks"] if day not in set(expected)]
        hot_lines = [
            f"Recovered Hot 100 printed weeks: {len(hot['weeks'])} ({hot['weeks'][0].isoformat()} through {hot['weeks'][-1].isoformat()}).",
            "These are the dates printed on the parsed pages. Matching the Saturday grid plus 2018-01-03 describes that set; it is not an outside census of every chart Billboard published.",
            f"Saturday grid from 2018-01-06 through {hot['weeks'][-1].isoformat()}, plus 2018-01-03: {len(expected)}.",
            f"Printed dates missing from that grid: {len(missing)}" + (f" ({', '.join(missing[:12])})" if missing else "."),
            f"Printed dates outside that grid: {len(extra)}" + (f" ({', '.join(extra[:12])})" if extra else "."),
            "2018-01-03 and 2018-01-06 are different lists: Juice is No. 93 on 3 Jan (last week 96, 3 weeks on chart) and No. 100 on 6 Jan (last week 93, 4 weeks on chart). Twelve songs share a rank. Perfect's weeks-on-chart go from 17 to 18.",
            f"Rows per week: min {min(hot['counts'])}, median {_median(hot['counts'])}, max {max(hot['counts'])}.",
            f"Duplicate-rank weeks: {hot['dup_ranks']}. Weeks with a hole in 1..max rank: {hot['missing_ranks']}. Rank uniqueness is not treated as proof of a correct snapshot.",
        ]

    problem_lines = []
    for item in stats:
        if item["dup_ranks"] or item["missing_ranks"] or item.get("coverage") == "unexplained_jump":
            problem_lines.append(
                f"- {item['chart']}: status {item['status']}, coverage {item.get('coverage')}, "
                f"weeks {len(item['weeks'])}, dup ranks {item['dup_ranks']}, "
                f"rank holes {item['missing_ranks']}. " + " ".join(item["notes"])
            )
    if not problem_lines:
        problem_lines.append("- No rank-hole or duplicate-rank failures were recorded in this pass.")
    problem_lines.append(
        "- `coverage_since_2018=recovered_from_range_start` means the recovered printed weeks start by 2018-01-17 and have no internal gap over 14 days. It does not mean an external index was checked."
    )
    problem_lines.append(
        "- `unknown_before_first_recovered` means the live site did not yield earlier issues. The first printed week is not a launch date unless `launch_evidence` says so."
    )
    problem_lines.append(
        "- `source_url` in the CSV is the Billboard URL for the printed week. The Nov 9 scrape did not retain the request URL, final redirect URL, or HTTP timestamp for those files. Do not read `source_url` as a stored fetch log. Exceptions are recorded in `resolution_checks.json` and the Thailand 2022-02-19 cache file."
    )

    region_counts = Counter()
    for item in stats:
        region_counts[item["region"]] += item["rows"]

    lines = [
        "# Billboard weekly chart validation",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}.",
        f"Song-chart rows: {total_rows}.",
        "These are recovered printed weeks, not a claim that every Billboard song chart since 2018 was collected.",
        combined_note,
        "",
        "## Coverage",
        "",
        "Attempted song-chart statuses: " + ", ".join(f"{key}={value}" for key, value in sorted(status_counts.items())),
        f"Menu charts recorded as skipped (albums, artist/credit charts, all-time lists): {len(skipped)}.",
        "",
        "Rows by region:",
        "",
    ]
    for region, count in sorted(region_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {region}: {count}")
    lines.extend(["", "## Hot 100", ""])
    lines.extend(hot_lines)
    lines.extend(["", "## Spot checks", ""])
    lines.extend(_spot_checks(cache))
    lines.extend(["", "## Gaps, failures, partial lists", ""])
    lines.extend(problem_lines)
    lines.extend(
        [
            "",
            "Thailand Songs launch evidence is the week of 19 Feb 2022 (Workpoint Today, 18 Feb 2022).",
            "The live URL for 2022-02-19 currently prints 1 Aug 2026, so the live site is not an archive of that chart.",
            "Internet Archive capture 20220215211337 of that URL prints Week of 19 Feb 2022, 25 songs, No. 1 Until Then by Tilly Birds.",
            "That one week was added from the archive (fetched 2026-11-09T18:31:23Z). Availability API checks for 19 Mar 2022, 18 Jun 2022, 17 Dec 2022, 17 Jun 2023, 17 Feb 2024, 15 Feb 2025, and 25 Jul 2026 returned no snapshot.",
            "A prefix CDX listing of every Thailand week timed out. The span from 26 Feb 2022 through 25 Jul 2026 was not recovered.",
            "Both Vietnam charts launch 14 Jan 2022 according to Billboard's 11 Jan 2022 chart-beat article.",
            "Requesting 2022-01-14 on the live site prints 31 May 2025 (Hot 100) and 28 Jun 2025 (Top Vietnamese Songs), which is where the recovered live series starts.",
            "Wayback availability for those 2022 URLs, and for slug variants vietnam-hot-100, returned no snapshot. The 2022-to-2025 Vietnam issues were not recovered.",
            "On 2026-11-09 the undated Top Vietnamese Songs page printed 31 Oct 2026, one week past the earlier scrape. That week was fetched the same day and added.",
            "The same day's undated pages matched the saved last week for Hot 100 (7 Nov), Japan (31 Oct, 25 rows), Official U.K. (14 Nov, 20 rows), Arabic (31 Oct, 25 rows), both Philippines charts (17 Oct, 25 rows), Colombia (24 Oct, 25 rows), and Vietnam Hot 100 (31 Oct, 25 rows).",
            "WARM Global Dance Radio's live URL for 1 Jun 2024 prints 14 Mar 2026. That first recovered week is not a documented launch.",
            "Single missing issue dates were re-requested and resolved to the next saved week, not to the latest issue: LyricFind 26 May 2018, Argentina 19 Aug 2023, Italy 23 Sep 2023, Arabic 21 Feb 2026.",
            "`full_100` is true only when every recovered week has 100 rows.",
            "A 25-row Hits of the World chart, a 25-row Japan Hot 100 page, and a 20-row Official U.K. page are not full 100s.",
            "Dance Club Songs: every recovered week has 55 rows, 118 weeks, 2018-01-03 through 2020-03-28. Bubbling Under: every recovered week has 25 rows, 463 weeks. Neither was re-checked against a printed magazine in this pass.",
            "Those two counts describe the saved pages. They were not re-checked against a printed magazine.",
            "",
            "Nine pairs of consecutive weeks repeat the same ranks, titles, and artists while last-week or weeks-on-chart changes.",
            "No consecutive weeks repeat the full stat line. That argues against storing one HTTP response under two dates.",
            "The pairs are Argentina Hot 100 around 12–26 Jan 2019, Philippines Top Philippine Songs 28 Feb–7 Mar 2026,",
            "Gospel Streaming Songs 28 Sep–5 Oct 2024, LyricFind U.S. and Global at the ends of 2018 and 2019, and R&B Streaming Songs 17–24 Mar 2018.",
            "",
            "## Included charts",
            "",
            "| chart | region | weeks | first recovered | last recovered | rows | public depth | full 100 | coverage |",
            "| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in included:
        if not row["rows"] and row["status"] in {"skipped", "missing"}:
            continue
        lines.append(
            f"| {row['chart']} | {row['region']} | {row['weeks']} | {row['first_week']} | "
            f"{row['last_week']} | {row['rows']} | {row['public_depth']} | {row['full_100']} | "
            f"{row['coverage_since_2018']} |"
        )
    lines.extend(["", "## Skipped probe or empty charts", ""])
    lines.append(
        "A live 404, or a page that resolves to a week before 2018, is not proof the slug never had a 2018-present chart. "
        "Internet Archive CDX lookups for these slugs timed out or were not available in this pass, so their history was not recovered."
    )
    for row in attempted:
        if row["status"] == "skipped" or (row["status"] == "failed" and not row["rows"]):
            lines.append(f"- `{row['chart']}` ({row['chart_name']}): {row['reason'] or row['status']}")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--data-dir", default="data/billboard", help="Dataset directory")
    parser = argparse.ArgumentParser(description="Download weekly Billboard song charts.", parents=[common])
    sub = parser.add_subparsers(dest="command", required=True)

    scrape_parser = sub.add_parser("scrape", help="Fetch charts, then export and validate", parents=[common])
    scrape_parser.add_argument("--interval", type=float, default=0.55, help="Minimum seconds between HTTP requests")
    scrape_parser.add_argument("--workers", type=int, default=3, help="Charts fetched at once")
    scrape_parser.add_argument("--only", default="", help="Comma-separated slugs to fetch")
    scrape_parser.add_argument("--max-weeks", type=int, default=0, help="Stop each chart after this many weeks (0 = all)")
    scrape_parser.add_argument("--skip-probe", action="store_true", help="Do not check archived extra slugs")
    scrape_parser.add_argument("--skip-export", action="store_true", help="Leave export/validation for later")
    scrape_parser.set_defaults(func=scrape)

    export_parser = sub.add_parser("export", help="Write CSV.gz files and VALIDATION.md from the cache", parents=[common])
    export_parser.set_defaults(func=lambda args: export_and_validate(Path(args.data_dir)))

    validate_parser = sub.add_parser("validate", help="Alias of export", parents=[common])
    validate_parser.set_defaults(func=lambda args: export_and_validate(Path(args.data_dir)))
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "max_weeks", 0) == 0:
        args.max_weeks = None
    args.func(args)


if __name__ == "__main__":
    main()
