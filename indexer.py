#!/usr/bin/python3
# -*- coding: utf8

import argparse
import sys

from engine.indexer import Indexer


def main() -> int:
    indexer = Indexer()

    # Create the arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', required=False)
    sp = parser.add_subparsers()

    # GET
    get_parser = sp.add_parser('get')
    get_parser.add_argument('--all', dest='all', action='store_true', required=False)
    get_parser.add_argument('--filename', dest='filename', type=str, required=False)
    get_parser.add_argument('--index', dest='index', type=str, required=False)
    get_parser.set_defaults(func=indexer.get_index_card)

    # SAVE
    save_parser = sp.add_parser('save')
    # FIXME?: save_parser.add_argument('--to', dest='dest', type=str, required=False)
    save_parser.set_defaults(func=indexer.save_index_card)

    # EDIT
    edit_parser = sp.add_parser('edit')
    edit_parser.add_argument('index', metavar='index', type=int)
    edit_parser.set_defaults(func=indexer.edit_index_card)

    # DELETE
    delete_parser = sp.add_parser('delete')
    delete_parser.add_argument('index', metavar='index', type=int)
    delete_parser.set_defaults(func=indexer.delete_index_card)

    args = parser.parse_args()

    __debug_flag = False
    if args.debug:
        print("El debug esta habilitado")
        __debug_flag = True
    else:
        __debug_flag = False

    data = args.func(args)

    print("Fin de ejecución")
    return 0


if __name__ == "__main__":
    sys.exit(main())
