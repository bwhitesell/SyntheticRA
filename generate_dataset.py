#!/usr/bin/env python

import argparse
import logging

from synthetic_ra.data import scans
from synthetic_ra.data.utils import generate_dataset


logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='config for building dataset.')
parser.add_argument(
    '--path',
    type=str,
    help='path to save dataset to.',
)
parser.add_argument(
    '--size_cutoff',
    type=int,
    help='number of post titles to stop building dataaset at.',
    default=10000,
)
parser.add_argument(
    '--scan_type',
    type=str,
    help='The scan strategy to use to find posts.'
)


if __name__ == '__main__':
    args = parser.parse_args()

    generate_dataset(
        save_path=args.path,
        n_posts=args.size_cutoff,
        scan=getattr(scans, args.scan_type),
    )
