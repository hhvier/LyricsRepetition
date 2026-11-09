import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "py"))

from billboard_charts import parse_chart_html, parse_week_heading  # noqa: E402


FIXTURE = """
<html><body>
<h1>Billboard Hot 100</h1>
<h2>Week of January 6, 2018</h2>
<ul class="o-chart-results-list-row">
  <li class="o-chart-results-list__item"><span class="c-label">1</span></li>
  <li></li><li></li>
  <li class="a-chart-result-item-container"><ul>
    <li><h3 id="title-of-a-story">Perfect</h3>
        <span class="c-label a-no-trucate">Ed Sheeran</span></li>
    <li>LW 1 PEAK 1 WEEKS AT NO. 1 4 WEEKS ON CHART 18</li>
    <li>1</li><li>1</li><li>4</li><li>18</li>
    <li>LW 1 PEAK 1 WEEKS ON CHART 18 WEEKS AT NO. 1 4</li>
    <li>1</li><li>1</li><li>18</li>
  </ul></li>
</ul>
<ul class="o-chart-results-list-row">
  <li class="o-chart-results-list__item"><span class="c-label">100 NEW</span></li>
  <li></li><li>NEW</li>
  <li class="a-chart-result-item-container"><ul>
    <li><h3 id="title-of-a-story">Juice</h3>
        <span class="c-label a-no-trucate">Yo Gotti</span></li>
    <li>LW - PEAK 93 WEEKS ON CHART 4</li>
    <li>-</li><li>93</li><li>4</li>
  </ul></li>
</ul>
<ul class="o-chart-results-list-row">
  <li class="o-chart-results-list__item"><span class="c-label">2 RE- ENTRY</span></li>
  <li></li><li>RE-ENTRY</li>
  <li class="a-chart-result-item-container"><ul>
    <li><h3 id="title-of-a-story">Warotapipo</h3>
        <span class="c-label a-no-trucate">NMB48</span></li>
    <li>LW - PEAK 1 WEEKS AT NO. 1 1 WEEKS ON CHART 2</li>
    <li>-</li><li>1</li><li>1</li><li>2</li>
  </ul></li>
</ul>
</body></html>
"""


class ParseChartTest(unittest.TestCase):
    def test_week_heading(self):
        self.assertEqual(parse_week_heading("Week of January 6, 2018"), date(2018, 1, 6))
        self.assertIsNone(parse_week_heading("Billboard Hot 100"))

    def test_rows_stats_and_badges(self):
        parsed = parse_chart_html(FIXTURE)
        self.assertEqual(parsed.week, date(2018, 1, 6))
        self.assertEqual([row["rank"] for row in parsed.rows], [1, 2, 100])
        top = parsed.rows[0]
        self.assertEqual(top["title"], "Perfect")
        self.assertEqual(top["artist"], "Ed Sheeran")
        self.assertEqual(top["last_week"], 1)
        self.assertEqual(top["peak_position"], 1)
        self.assertEqual(top["weeks_at_number_one"], 4)
        self.assertEqual(top["weeks_on_chart"], 18)
        self.assertFalse(top["is_new"])
        debut = parsed.rows[2]
        self.assertTrue(debut["is_new"])
        self.assertIsNone(debut["last_week"])
        self.assertEqual(debut["weeks_on_chart"], 4)
        self.assertIsNone(debut["weeks_at_number_one"])
        reentry = parsed.rows[1]
        self.assertTrue(reentry["is_reentry"])
        self.assertFalse(reentry["is_new"])
        self.assertEqual(reentry["weeks_at_number_one"], 1)
        self.assertEqual(reentry["weeks_on_chart"], 2)

    def test_saved_hot100_page_if_present(self):
        path = Path("/tmp/bb_hot100.html")
        if not path.exists():
            self.skipTest("live fixture not downloaded")
        parsed = parse_chart_html(path.read_text(encoding="utf-8", errors="replace"))
        self.assertEqual(parsed.week, date(2018, 1, 6))
        self.assertEqual(len(parsed.rows), 100)
        self.assertEqual(parsed.rows[0]["title"], "Perfect")
        self.assertIn("Ed Sheeran", parsed.rows[0]["artist"])
        self.assertEqual(parsed.rows[-1]["rank"], 100)
        self.assertEqual(parsed.rows[-1]["title"], "Juice")
        self.assertEqual([row["rank"] for row in parsed.rows], list(range(1, 101)))


if __name__ == "__main__":
    unittest.main()
