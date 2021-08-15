from datetime import datetime


# CLIENT CONSTANTS
RA_SUBREDDIT_NAME: str = 'relationship_advice'

REDDIT_IO_BASE_SEARCH_URL: str = (
    'https://api.pushshift.io/reddit/search/submission/?q='
    '&author=&aggs=&metadata=true&frequency=hour&advanced=false&sort=desc'
    '&domain=&sort_type=num_comments&size=500'
)

_2020: datetime = datetime(2020, 1, 1)


# ENCODING CONSTANTS
START_TOKEN: str = '<start>'
END_TOKEN: str = '<end>'
PAD_TOKEN: str = '<pad>'
