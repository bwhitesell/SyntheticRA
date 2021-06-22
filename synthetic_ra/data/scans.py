from datetime import datetime

from synthetic_ra.data.client import RedditSearchIOPostScan


exhaustive_title_scan: RedditSearchIOPostScan = RedditSearchIOPostScan(
    scan_start=datetime(2016, 1, 1),
    interval_hrs=6,
)

recent_pop_title_scan: RedditSearchIOPostScan = RedditSearchIOPostScan(
    scan_start=datetime(2020, 1, 1),
    interval_hrs=24,
)

balanced_title_scan: RedditSearchIOPostScan = RedditSearchIOPostScan(
    scan_start=datetime(2019, 1, 1),
    interval_hrs=12,
)
