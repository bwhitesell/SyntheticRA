from collections import Counter
import csv
import json
import logging
import pandas as pd
import re
from synthetic_ra.data.client import SubredditPostScan
from torchtext.data import get_tokenizer


logger = logging.getLogger(__name__)


def generate_dataset(save_path: str, n_posts: int,
                     scan: SubredditPostScan) -> None:

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


def count_tokens_over_dataset(dataset_path: str) -> Counter:
    """ Return a counter object thats run over a dataset. """

    tokenizer = get_tokenizer('basic_english')
    token_counter = Counter()

    with open(dataset_path, 'r') as f:
        dataset_reader = csv.reader(f)
        for title_list in dataset_reader:
            title: str = title_list[0]
            processed_title: str = preprocess_title(title)
            token_counter.update(tokenizer(processed_title))

    return token_counter


def preprocess_title(title: str) -> str:
    """ Apply preprocessing logic to title string for easier tokenization. """

    title = title.lower()
    title = title.replace('(', '[').replace(')', ']')
    title = title.replace('[', ' [ ').replace(']', ' ] ').replace('/', ' / ')
    title = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", title)
    return title


def convert_counter_to_dataframe(counter: Counter) -> pd.DataFrame:
    """
        Convert a counter object to a dataframe explicating the stats of each
        counted item.
    """

    counted_dataset = pd.DataFrame(
        counter.most_common(len(counter)),
        columns=['token', 'token_count']
    )

    counted_dataset.loc[:, 'rank'] = pd.Series(range(len(counted_dataset))) + 1

    counted_dataset.loc[:, 'pct_dataset'] = (
        counted_dataset.token_count / counted_dataset.token_count.sum()
    )

    counted_dataset.loc[:, 'cume_pct_dataset'] = (
        counted_dataset.pct_dataset.cumsum()
    )

    return counted_dataset


def summarize_dataset(dataset_path: str, summary_name: str = 'test') -> None:
    """
        Given a path to a properly formatted datset, generate summary stats
        and plots.
    """
    logger.info(f'Describing dataset @ {dataset_path}')

    counter: Counter = count_tokens_over_dataset(dataset_path)
    counted_dataset: pd.DataFrame = convert_counter_to_dataframe(counter)
    counted_dataset = counted_dataset[:500][::5]

    with open(f'/tmp/synth_ra_dataset_summary_{summary_name}.json', 'w') as f:
        json.dump(counted_dataset.to_dict('records'), f, indent=2)


if __name__ == '__main__':
    dataset_path = '/home/ben/SyntheticRA/ra_dataset_popular.csv'
    summarize_dataset(dataset_path)
