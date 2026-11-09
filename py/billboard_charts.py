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
    PROBE_CANDIDATES,
    SKIPPED_CHARTS,
    SONG_CHARTS,
)

RANGE_START = date(2018, 1, 3)
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
        payload = {
            "chart": spec.slug,
            "region": spec.region,
            "category": spec.category,
            "chart_name": parsed.chart_name or spec.name,
            "week": parsed.week.isoformat(),
            "source_url": chart_url(spec.slug, parsed.week),
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
    path = store.week_path(slug, week)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return ParsedChart(
        week=date.fromisoformat(payload["week"]),
        chart_name=payload.get("chart_name") or "",
        rows=payload.get("rows") or [],
        final_url=payload.get("source_url") or "",
    )


def load_parsed(session, url, limiter, stop, spec_name: str) -> ParsedChart:
    html, final_url = fetch_html(session, url, limiter, stop)
    parsed = parse_chart_html(html, final_url)
    if parsed.chart_name == "":
        parsed.chart_name = spec_name
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


def next_published_week(
    session,
    store: Store,
    spec: ChartSpec,
    limiter: RateLimiter,
    stop: threading.Event,
    cursor: date,
    end: date,
) -> ParsedChart | None:
    """Find the next issue after ``cursor``.

    Billboard rounds a requested date forward to the next published issue.
    The day after a known issue is usually enough. Wider steps cover seasonal
    charts whose next issue is months away, and the empty page Billboard
    serves after a chart has ended.
    """
    span = max(1, (end - cursor).days)
    offsets = []
    for offset in (1, 7, 14, 21, 35, 70, 140, 210, span):
        if offset not in offsets and offset <= span + 7:
            offsets.append(offset)
    for offset in offsets:
        if stop.is_set():
            raise FetchError("stopped", "stop requested")
        probe = cursor + timedelta(days=offset)
        cached = _cached_chart(store, spec.slug, probe)
        if cached is not None:
            parsed = cached
        else:
            try:
                parsed = load_parsed(session, chart_url(spec.slug, probe), limiter, stop, spec.name)
            except FetchError as exc:
                if exc.kind in {"blocked", "stopped"}:
                    raise
                store.log(f"{spec.slug} probe {probe} failed ({exc.kind}): {exc}")
                continue
        # The site rounds a date forward to the next published issue, so the
        # first probe that moves past `cursor` is the next issue.
        if parsed.week and cursor < parsed.week <= end + timedelta(days=14):
            return parsed
    return None


def scrape_one(
    spec: ChartSpec,
    store: Store,
    limiter: RateLimiter,
    stop: threading.Event,
    max_weeks: int | None,
) -> dict:
    session = make_session()
    state = store.load_state(spec.slug)
    state.setdefault("weeks", [])
    state.setdefault("error", "")
    state["name"] = spec.name
    state["region"] = spec.region
    state["category"] = spec.category

    if stop.is_set():
        state["status"] = state.get("status") or "stopped"
        store.save_state(state)
        return state

    try:
        latest = load_parsed(session, chart_url(spec.slug), limiter, stop, spec.name)
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

    if state.get("status") == "done" and state["weeks"]:
        last_saved = date.fromisoformat(state["weeks"][-1])
        if last_saved >= end:
            store.log(f"{spec.slug} already current through {last_saved.isoformat()} ({len(state['weeks'])} weeks)")
            return state
        store.log(f"{spec.slug} updating {last_saved.isoformat()} -> {end.isoformat()}")

    if not state["weeks"] or date.fromisoformat(state["weeks"][0]) > end:
        state["weeks"] = []

    if not state["weeks"]:
        parsed = _first_week_in_range(session, store, spec, limiter, stop, end)
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
        parsed = next_published_week(session, store, spec, limiter, stop, cursor, end)
        if parsed is None or parsed.week is None or parsed.week <= cursor:
            break
        if parsed.week > end + timedelta(days=14):
            break
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

    last = date.fromisoformat(state["weeks"][-1]) if state["weeks"] else None
    if last is None:
        state["status"] = "failed"
        state["error"] = "walk produced no weeks"
    elif last < end:
        state["status"] = "incomplete"
        state["error"] = f"stopped at {last.isoformat()} before latest {end.isoformat()}"
    else:
        state["status"] = "done"
        state["error"] = ""
    state["positions_last"] = len(latest.rows)
    store.save_state(state)
    store.log(
        f"{spec.slug} {state['status']} weeks={len(state['weeks'])} "
        f"first={state['weeks'][0] if state['weeks'] else '-'} last={last} ({state['error']})"
    )
    return state


def _first_week_in_range(session, store, spec, limiter, stop, end: date) -> ParsedChart | None:
    probe = RANGE_START
    best: ParsedChart | None = None
    for _ in range(6):
        parsed = load_parsed(session, chart_url(spec.slug, probe), limiter, stop, spec.name)
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
                "notes": "",
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
    if status != "done":
        notes.append(f"scrape status {status}")
    median_rows = _median(counts)
    if median_rows is not None and median_rows < 100 and (
        "100" in slug or "100" in chart_name or "200" in slug
    ):
        notes.append(
            f"Public page lists {median_rows} positions in a typical week, "
            "short of the chart's traditional depth. Rows are only those Billboard "
            "prints on the public page."
        )
    if category in {"holiday", "summer"}:
        notes.append("Seasonal chart: multi-week gaps between seasons are expected.")
    if dup_ranks:
        notes.append(f"{dup_ranks} weeks have duplicate ranks.")
    if missing_ranks:
        notes.append(f"{missing_ranks} weeks are missing a rank in 1..max.")
    long_gaps = [gap for gap in gaps if gap[2] > 14]
    if long_gaps and category not in {"holiday", "summer"}:
        notes.append(f"{len(long_gaps)} gaps longer than 14 days.")

    stats.append(
        {
            "chart": slug,
            "chart_name": chart_name,
            "region": region,
            "category": category,
            "status": status,
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
            f"Hot 100 weeks fetched: {len(hot['weeks'])} ({hot['weeks'][0].isoformat()} through {hot['weeks'][-1].isoformat()}).",
            f"Expected Saturday issues from 2018-01-06 through {hot['weeks'][-1].isoformat()}, plus the 2018-01-03 mid-week chart: {len(expected)}.",
            f"Missing expected dates: {len(missing)}" + (f" ({', '.join(missing[:12])})" if missing else "."),
            f"Extra dates: {len(extra)}" + (f" ({', '.join(extra[:12])})" if extra else "."),
            f"Rows per week: min {min(hot['counts'])}, median {_median(hot['counts'])}, max {max(hot['counts'])}.",
            f"Duplicate-rank weeks: {hot['dup_ranks']}. Weeks with a hole in 1..max rank: {hot['missing_ranks']}.",
        ]

    problem_lines = []
    for item in stats:
        if item["status"] != "done" or item["dup_ranks"] or item["missing_ranks"]:
            problem_lines.append(
                f"- {item['chart']}: status {item['status']}, weeks {len(item['weeks'])}, "
                f"dup ranks {item['dup_ranks']}, rank holes {item['missing_ranks']}. "
                + " ".join(item["notes"])
            )
        elif item["category"] not in {"holiday", "summer"}:
            long_gaps = [gap for gap in item["gaps"] if gap[2] > 14]
            if long_gaps:
                sample = ", ".join(f"{a} -> {b} ({d}d)" for a, b, d in long_gaps[:4])
                problem_lines.append(f"- {item['chart']}: {len(long_gaps)} gaps over 14 days ({sample}).")
    if not problem_lines:
        problem_lines.append("- No incomplete charts, duplicate ranks, rank holes, or unexpected gaps over 14 days.")

    region_counts = Counter()
    for item in stats:
        region_counts[item["region"]] += item["rows"]

    lines = [
        "# Billboard weekly chart validation",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}.",
        f"Song-chart rows: {total_rows}.",
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
            "Charts whose public page lists fewer than 100 songs are kept in full as published.",
            "That includes airplay charts (often 20–50 positions), Hits of the World (usually 25),",
            "and some territory charts that still carry a Hot 100 name. See `notes` in `catalog.csv`.",
            "",
            "## Included charts",
            "",
            "| chart | region | weeks | first | last | rows | median positions | status |",
            "| --- | --- | ---: | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in included:
        if not row["rows"] and row["status"] in {"skipped", "missing"}:
            continue
        lines.append(
            f"| {row['chart']} | {row['region']} | {row['weeks']} | {row['first_week']} | "
            f"{row['last_week']} | {row['rows']} | {row['median_rows']} | {row['status']} |"
        )
    lines.extend(["", "## Skipped probe or empty charts", ""])
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
