import csv
import logging
from synthetic_ra.data.client import RedditSearchIOPostScan


logger = logging.getLogger(__name__)


def generate_dataset(save_path: str, n_posts: int,
                     scan: RedditSearchIOPostScan) -> None:

    logger.info(
        'Generating new RA dataset. \n'
        f'Writing dataset to: {save_path} \n'
        f'Building dataset to be of max size: {n_posts} \n'
        f'Using scan strategy: {scan}'
    )

    n_posts_written: int = 0

    with open(save_path + '/ra_dataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Post Title'])

        for posts in scan:
            if n_posts_written >= n_posts:
                break

            for post in posts:
                writer.writerow([f""" "{post.get('title')}" """])
                n_posts_written += 1

            logger.info(f'Current scan date: {scan._scan_dt}')
            logger.info(
                f'New posts processed. {n_posts_written}/{n_posts} written'
            )

    logger.info('Dataset construction done.')
