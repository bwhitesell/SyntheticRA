from datetime import datetime

from synthetic_ra.data.client import SubredditPostScan
from synthetic_ra.data.constants import RA_SUBREDDIT_NAME


exhaustive_title_scan: SubredditPostScan = SubredditPostScan(
    subreddit=RA_SUBREDDIT_NAME,
    scan_start=datetime(2016, 1, 1),
    interval_hrs=6,
)

recent_pop_title_scan: SubredditPostScan = SubredditPostScan(
    subreddit=RA_SUBREDDIT_NAME,
    scan_start=datetime(2020, 1, 1),
    interval_hrs=24,
)

balanced_title_scan: SubredditPostScan = SubredditPostScan(
    subreddit=RA_SUBREDDIT_NAME,
    scan_start=datetime(2019, 1, 1),
    interval_hrs=12,
)
