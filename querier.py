#!/usr/bin/python3
# -*- coding: utf8

import argparse
import sys
from engine.querier import Querier

# Create the arguments parser
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest='debug', action='store_true', required=False)
parser.add_argument('--title', dest='title', type=str, required=False)
parser.add_argument('--abstract', dest='abstract', type=str, required=False)
parser.add_argument('--from-year', dest='fromYear', type=str, required=False)
parser.add_argument('--to-year', dest='toYear', type=str, required=False)
parser.add_argument('--query', dest='query', type=str, required=False)
parser.add_argument('--content', dest='content', type=str, required=False)


def main() -> int:
    args = parser.parse_args()

    if args.debug:
        __debug_flag = True
    else:
        __debug_flag = False

    querier = Querier(args.__dict__)
    querier.configure()
    querier.search(__debug_flag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
