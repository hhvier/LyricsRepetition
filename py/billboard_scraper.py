"""Legacy Hot 100 entry point.

The original script walked https://www.billboard.com/charts/hot-100/ and read
``div.chart-list-item`` attributes into MySQL. Billboard removed that markup,
so those requests no longer return chart rows. Weekly song charts for the
Hot 100, genre charts, and regional charts are downloaded by billboard_charts.py.

    python py/billboard_charts.py scrape

See docs/billboard_charts.md.
"""

from billboard_charts import main

if __name__ == "__main__":
    main()
