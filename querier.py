#!/usr/bin/python3
# -*- coding: utf8

import argparse
from engine.querier import querier
import yaml
import logging
import logging.config
import traceback
from repos import *

# Create the arguments parser
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest='debug', action='store_true', required=False)
parser.add_argument('--title', dest='title', type=str, required=False)
parser.add_argument('--abstract', dest='abstract', type=str, required=False)
parser.add_argument('--from-year', dest='fromYear', type=str, required=False)
parser.add_argument('--to-year', dest='toYear', type=str, required=False)
parser.add_argument('--query', dest='query', type=str, required=False)
parser.add_argument('--content', dest='content', type=str, required=False)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.debug:
        __debug_flag = True
    else:
        __debug_flag = False

    querier(__debug_flag, args.query, args.content, args.fromYear, args.title)
