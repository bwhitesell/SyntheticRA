from collections import Counter
import csv
import json
import logging
import pandas as pd
from pathlib import Path
from torchtext.vocab import Vocab
from typing import List
from typing import Union

from synthetic_ra.data.client import SubredditPostScan
from synthetic_ra.data.titles import RAPostTitle


logger = logging.getLogger(__name__)


def generate_csv_dataset(
    save_path: str,
    max_n_posts: int,
    scan: SubredditPostScan,
) -> None:
    """ Write the post titles from the provided scan policy to a csv. """

    logger.info(
        'Generating new RA dataset. \n'
        f'Writing dataset to: {save_path} \n'
        f'Building dataset to be of max size: {max_n_posts} \n'
        f'Using scan strategy: {scan}'
    )

    n_posts_written: int = 0

    with open(save_path + '/ra_dataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Post Title'])

        for posts in scan:
            logger.info(f'Current scan date: {scan._scan_dt}')

            if posts:
                if n_posts_written >= max_n_posts:
                    break

                for post in posts:
                    writer.writerow([f""" "{post.get('title')}" """])
                    n_posts_written += 1

                logger.info(
                    f'New posts processed. {n_posts_written}/{max_n_posts} written'
                )
            else:
                continue

    logger.info('Dataset construction done.')


def load_titles_from_csv(file: Union[str, Path]) -> List[RAPostTitle]:
    post_titles = list()

    with open(str(file), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers: List[str] = next(csv_reader)

        for line in csv_reader:
            stripped_line: str = line[0][2:-2]
            post_titles.append(RAPostTitle(stripped_line))

    return post_titles
