from datetime import datetime


REDDIT_IO_BASE_SEARCH_URL: str = (
    'https://api.pushshift.io/reddit/search/submission/'
    '?q=&subreddit=relationship_advice'
    '&author=&aggs=&metadata=true&frequency=hour&advanced=false&sort=desc'
    '&domain=&sort_type=num_comments&size=500'
)

_2020: datetime = datetime(2020, 1, 1)