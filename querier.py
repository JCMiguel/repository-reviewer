#!/usr/bin/python3
# -*- coding: utf8

import argparse
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


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def querier(debug: bool, query: str = "", content: str = "", from_year: str = "", title: str = "", arguments = None):
    print("Cargando archivo de configuración")
    cfg = read_yaml("config/querier_config.yml") # TODO: Pendiente hacer chequeo de errores

    print(debug)
    print("Cargando clases de repositorios")
    for repo in cfg['repos'].keys():
        try:
            # La línea siguiente invoca a la clase dentro del package.
            # Ejemplo: invoca al constructor ieee() de repos.ieee_def
            if cfg['repos'][repo]['enabled'] is True:
                id = getattr(globals()[repo + '_def'], repo)(cfg['repos'][repo], cfg['params'], __debug_flag)
                if id is not None:
                    id.say_hello()
                    if args.query == "" or args.query is None:
                        id.add_query_param(args.content, 'content')
                        id.add_query_param(args.fromYear, 'from_year')
                        id.add_query_param(args.title, 'title')
                        id.add_query_param(args.toYear, 'to_year')
                        id.add_query_param(args.abstract, 'abstract')
                    else:
                        # TODO: Si me funciona con IEEE, tengo que ver cómo hacerlo para scopus.
                        id.load_query(args.query)
                    id.search()
                    del id
        except Exception:
            traceback.print_exc()
    print("Fin de ejecución")


if __name__ == "__main__" :
    args = parser.parse_args()

    if args.debug:
        __debug_flag = True
    else:
        __debug_flag = False

    querier(__debug_flag, args.query, args.content, args.fromYear, args.title)
