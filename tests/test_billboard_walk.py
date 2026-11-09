import shutil
import sys
import tempfile
import threading
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "py"))

from billboard_charts import (  # noqa: E402
    ChartSpec,
    FetchError,
    ParsedChart,
    RateLimiter,
    Store,
    _cached_chart,
    assess_coverage,
    classify_advance,
    next_published_week,
    scrape_one,
)


def entry(week: date) -> ParsedChart:
    return ParsedChart(
        week=week,
        chart_name="Test",
        rows=[
            {
                "rank": 1,
                "title": "Song",
                "artist": "Artist",
                "last_week": 1,
                "peak_position": 1,
                "weeks_on_chart": 2,
                "weeks_at_number_one": None,
                "is_new": False,
                "is_reentry": False,
            }
        ],
    )


def next_saturday(day: date) -> date:
    if day.weekday() == 5:
        return day
    return day + timedelta(days=(5 - day.weekday()) % 7)


class ClassifyAdvanceTest(unittest.TestCase):
    def test_normal_and_midweek_steps_are_accepted(self):
        self.assertEqual(classify_advance(date(2018, 1, 6), date(2018, 1, 13), "all-genre"), "accept")
        self.assertEqual(classify_advance(date(2018, 1, 3), date(2018, 1, 6), "all-genre"), "accept")
        self.assertEqual(classify_advance(date(2018, 5, 19), date(2018, 6, 2), "lyric"), "accept")

    def test_long_nonseasonal_jump_is_unexplained(self):
        self.assertEqual(
            classify_advance(date(2022, 2, 19), date(2026, 8, 1), "hits-of-the-world"),
            "unexplained",
        )
        self.assertEqual(classify_advance(date(2018, 5, 19), date(2018, 6, 3), "lyric"), "unexplained")

    def test_seasonal_gap_is_a_hiatus(self):
        self.assertEqual(classify_advance(date(2018, 1, 3), date(2018, 12, 8), "holiday"), "hiatus")
        coverage = assess_coverage(
            [date(2018, 1, 3), date(2018, 12, 8), date(2018, 12, 15)],
            "holiday",
        )
        self.assertEqual(coverage["label"], "seasonal_stored_weeks")
        self.assertEqual(len(coverage["seasonal_hiatuses"]), 1)
        self.assertEqual(coverage["unexplained_jumps"], [])

    def test_leading_gap_is_not_a_launch(self):
        coverage = assess_coverage([date(2026, 8, 1), date(2026, 8, 8)], "hits-of-the-world")
        self.assertEqual(coverage["label"], "stored_weeks_start_later")
        self.assertEqual(coverage["leading_unrecovered"]["first_recovered"], "2026-08-01")


class WalkBehaviorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.store = Store(self.tmp)
        self.limiter = RateLimiter(0)
        self.stop = threading.Event()
        self.spec = ChartSpec("sample-chart", "Sample", "Testland", "hits-of-the-world")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _run(self, fetcher):
        return scrape_one(self.spec, self.store, self.limiter, self.stop, None, fetcher=fetcher)

    def test_redirect_to_latest_does_not_claim_completeness(self):
        calls = []

        def fetcher(url):
            calls.append(url)
            if "/20" not in url:
                return entry(date(2026, 11, 7))
            requested = date.fromisoformat(url.rstrip("/").split("/")[-1])
            if requested < date(2026, 8, 1):
                return entry(date(2026, 8, 1))
            week = next_saturday(requested)
            if week < date(2026, 8, 1):
                week = date(2026, 8, 1)
            if week > date(2026, 11, 7):
                week = date(2026, 11, 7)
            return entry(week)

        state = self._run(fetcher)
        self.assertEqual(state["status"], "partial")
        self.assertEqual(state["recovered_temporal_grid"], "stored_weeks_start_later")
        self.assertNotIn("2022-02-19", state["weeks"])
        self.assertIn("2026-08-01", state["weeks"])
        self.assertIn("2026-11-07", state["weeks"])
        self.assertTrue(all("2022-02-19" not in url for url in calls))

    def test_internal_redirect_is_an_unexplained_jump(self):
        self.store.save_week(self.spec, entry(date(2022, 2, 19)))
        state = self.store.load_state(self.spec.slug)
        state["weeks"] = ["2022-02-19"]
        self.store.save_state(state)

        def fetcher(url):
            if "/20" not in url:
                return entry(date(2026, 11, 7))
            requested = date.fromisoformat(url.rstrip("/").split("/")[-1])
            if requested < date(2026, 8, 1):
                return entry(date(2026, 8, 1))
            week = next_saturday(requested)
            if week > date(2026, 11, 7):
                week = date(2026, 11, 7)
            return entry(week)

        state = self._run(fetcher)
        self.assertEqual(state["recovered_temporal_grid"], "unexplained_internal_gap")
        self.assertEqual(state["status"], "partial")
        self.assertNotIn("2022-03-05", state["weeks"])
        self.assertTrue(state["unexplained_jumps"])
        self.assertEqual(state["jump_log"][0]["after"], "2022-02-19")
        self.assertEqual(state["jump_log"][0]["resolved_week"], "2026-08-01")

    def test_resume_does_not_refetch_cached_weeks(self):
        calls = []
        for week in (date(2018, 1, 6), date(2018, 1, 13)):
            self.store.save_week(self.spec, entry(week))
        state = self.store.load_state(self.spec.slug)
        state["weeks"] = ["2018-01-06", "2018-01-13"]
        self.store.save_state(state)

        def fetcher(url):
            calls.append(url)
            if "/20" not in url:
                return entry(date(2018, 1, 20))
            requested = date.fromisoformat(url.rstrip("/").split("/")[-1])
            return entry(next_saturday(requested) if requested.weekday() != 5 else requested)

        state = self._run(fetcher)
        self.assertEqual(state["status"], "done")
        self.assertEqual(state["recovered_temporal_grid"], "contiguous_stored_weeks")
        self.assertEqual(state["weeks"], ["2018-01-06", "2018-01-13", "2018-01-20"])
        self.assertFalse(any(url.rstrip("/").endswith("2018-01-06") for url in calls))
        self.assertFalse(any(url.rstrip("/").endswith("2018-01-13") for url in calls))

    def test_export_without_state_does_not_certify_the_temporal_grid(self):
        import csv
        import io

        from billboard_charts import COLUMNS, _export_chart

        self.store.save_week(self.spec, entry(date(2018, 1, 6)))
        state_path = self.store.state_path(self.spec.slug)
        if state_path.exists():
            state_path.unlink()
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        row = _export_chart(
            self.store.cache,
            self.store.weekly,
            writer,
            self.spec.slug,
            self.spec.name,
            self.spec.region,
            self.spec.category,
            [],
        )
        self.assertEqual(row["status"], "partial")
        self.assertEqual(row["recovered_temporal_grid"], "unknown_no_scrape_state")
        self.assertNotIn("claim_complete_since_2018", row)
        self.assertFalse(row["every_stored_week_has_100_rows"])

    def test_network_failure_is_not_marked_done(self):
        def fetcher(url):
            raise FetchError("network", f"timeout for {url}")

        state = self._run(fetcher)
        self.assertEqual(state["status"], "failed")
        self.assertEqual(state["weeks"], [])
        self.assertIn("network", state["error"])

    def test_empty_parse_stores_nothing(self):
        def fetcher(url):
            return ParsedChart(week=date(2026, 11, 7), chart_name="Test", rows=[])

        state = self._run(fetcher)
        self.assertEqual(state["status"], "skipped")
        self.assertEqual(list(self.store.chart_dir(self.spec.slug).glob("????-??-??.json")), [])

    def test_cache_file_with_a_different_printed_week_is_not_reused(self):
        path = self.store.week_path(self.spec.slug, date(2018, 1, 13))
        path.write_text(
            '{"week":"2026-08-01","chart_name":"Wrong","rows":[{"rank":1}],"source_url":"x"}',
            encoding="utf-8",
        )
        self.assertIsNone(_cached_chart(self.store, self.spec.slug, date(2018, 1, 13)))

    def test_next_week_does_not_treat_a_far_redirect_as_the_next_issue(self):
        def fetcher(url):
            return entry(date(2026, 11, 7))

        parsed, decision = next_published_week(
            None,
            self.store,
            self.spec,
            self.limiter,
            self.stop,
            date(2022, 2, 19),
            date(2026, 11, 7),
            fetcher,
        )
        self.assertEqual(decision, "unexplained")
        self.assertEqual(parsed.week, date(2026, 11, 7))


if __name__ == "__main__":
    unittest.main()
