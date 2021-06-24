from datetime import date, timedelta
from datetime import datetime as dt
import json
import logging
import time
import requests
from typing import Dict, Union

from synthetic_ra.data.constants import REDDIT_IO_BASE_SEARCH_URL, _2020


logger = logging.getLogger(__name__)


class RedditSearchIOAPIClient:
    """
        A client to handle retrieval of subreddit posts from the
        redditsearch.io api

        Supports direct post search between fixed time intervals.
    """

    _HEADERS: Dict[str, str] = {'User-Agent': 'Mozilla/5.0'}
    _MINIMUM_MS_BETWEEN_REQUESTS: int = 2000

    def __init__(self, subreddit: str = 'relationship_advice') -> None:
        self.subreddit: str = subreddit
        self._last_request_sent_time: dt = dt.now()

    def find_posts(
        self,
        interval_start_unix: int,
        interval_end_unix: int
    ) -> Dict[str, str]:

        self.guarantee_ms_between_reqs()
        request_url: str = self.build_time_interval_search_req_url(
            interval_start_unix,
            interval_end_unix
        )

        resp: requests.Response = requests.get(
            request_url,
            headers=self._HEADERS
        )
        resp_content: Dict[str, str] = json.loads(resp.text)
        return resp_content['data']

    def guarantee_ms_between_reqs(self):
        while self.time_since_last_req < self._MINIMUM_MS_BETWEEN_REQUESTS:
            time.sleep(.001)
        self._last_request_sent_time = dt.now()

    @property
    def time_since_last_req(self) -> float:
        return (
            dt.now() - self._last_request_sent_time
        ).total_seconds() * 1000

    def build_time_interval_search_req_url(
        self,
        interval_start_unix: int,
        interval_end_unix: int
    ) -> str:

        request_url: str = REDDIT_IO_BASE_SEARCH_URL
        request_url += f'&subreddit={self.subreddit}'
        request_url += (
            f'&after={interval_start_unix}&'
            f'before={interval_end_unix}'
        )

        return request_url


class SubredditPostScan:
    """
        A 'scanning' strategy to find posts from a given subreddit using the
        redditsearch.io internal api.

        The redditsearch.io api isn't obviously exhausive, no more than 100
        posts can be returned in a single request, always returning by sort
        order, which the client specifies as popular.

        The smaller the interval_hrs the more likely the request returns
        exhaustive results. Conversely, the larger the interval_hrs the more
        likely the request is to return popular posts.
    """

    def __init__(
        self,
        subreddit: str,
        scan_start: dt = _2020,
        interval_hrs: int = 24
    ) -> None:

        self.client = RedditSearchIOAPIClient(subreddit=subreddit)
        self._scan_dt: dt = scan_start
        self.scan_interval_hrs: int = interval_hrs

    def __iter__(self):
        return self

    def __next__(self) -> Dict[str, str]:

        try:
            posts = self.client.find_posts(
                interval_start_unix=self.to_unix(self._scan_dt),
                interval_end_unix=self.to_unix(self.scan_interval_end),
            )
        except Exception:
            logger.error(
                f'Unable to pull posts for search range: {self._scan_dt} '
                f'to {self.scan_interval_end}'
            )

        self._scan_dt = self.scan_interval_end

        if self._scan_dt >= dt.now():
            raise StopIteration

        return posts

    @property
    def scan_interval_end(self) -> dt:
        return (
            self._scan_dt + timedelta(hours=self.scan_interval_hrs)
        )

    @staticmethod
    def to_unix(date: Union[date, dt]) -> int:
        return int(time.mktime(date.timetuple()))
