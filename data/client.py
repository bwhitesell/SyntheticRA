from datetime import date, timedelta
from datetime import datetime as dt
import json
import time
import requests
from typing import Dict, Union

from data.constants import REDDIT_IO_BASE_SEARCH_URL, _2020


class RedditSearchIOAPIClient:
    """
        A client to handle retrieval of r/relationship_advice posts from the
        redditsearch.io api

        Supports direct post search between fixed time intervals. Also can be
        used as an iterable to scan for posts over a time range.
    """

    _HEADERS: Dict[str, str] = {'User-Agent': 'Mozilla/5.0'}
    _MINIMUM_MS_BETWEEN_REQUESTS: int = 2000

    def __init__(self, scan_start: dt = _2020, interval_hrs: int = 24) -> None:

        self._scan_dt: dt = scan_start
        self.scan_interval_hrs: int = interval_hrs
        self._last_request_sent_time: dt = dt.now()

    def __iter__(self):
        return self

    def __next__(self) -> Dict[str, str]:

        # Think the api is meant to be internal. Lets keep it courteous.
        while self.time_since_last_req < self._MINIMUM_MS_BETWEEN_REQUESTS:
            time.sleep(.001)

        posts = self.find_posts(
            interval_start_unix=self.to_unix(self._scan_dt),
            interval_end_unix=self.to_unix(self.scan_interval_end),
        )

        self._last_request_sent_time = dt.now()
        self._scan_dt += self.scan_interval_end

        return posts

    def find_posts(
        self,
        interval_start_unix: int,
        interval_end_unix: int
    ) -> Dict[str, str]:

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

    @property
    def time_since_last_req(self) -> float:
        return (
            dt.now() - self._last_request_sent_time
        ).total_seconds() * 1000

    @property
    def scan_interval_end(self) -> dt:
        return (
            self._scan_dt + timedelta(hours=self.scan_interval_hrs)
        )

    @staticmethod
    def to_unix(date: Union[date, dt]) -> int:
        return int(time.mktime(date.timetuple()))

    def build_time_interval_search_req_url(
        self,
        interval_start_unix: int,
        interval_end_unix: int
    ) -> str:

        request_url: str = REDDIT_IO_BASE_SEARCH_URL
        request_url += (
            f'&after={interval_start_unix}&'
            f'before={interval_end_unix}'
        )

        return request_url
