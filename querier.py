#!/usr/bin/python3
# -*- coding: utf8

import argparse
import yaml
import logging
import logging.config
import traceback
from repos import *
from historic import *

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

if __name__ == "__main__" :
    args = parser.parse_args()

    if args.debug:
        print("El debug esta habilitado")
        __debug_flag = True
        print("ARGUMENTS:\n", args.__dict__)
    else:
        __debug_flag = False


    print("Cargando archivo de configuración")
    cfg = read_yaml("config/querier_config.yml") # TODO: Pendiente hacer chequeo de errores
    #TODO: validar errores en el config.yml. hay que asegurar que exista todo lo necesario.
    # Ejemplo: url, params, apikey, etc.
    # Y que exista una clase llamada como en el config.yml

    search_handler = search.Search( args.__dict__ )

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
                    else:
                        # TODO: Si me funciona con IEEE, tengo que ver cómo hacerlo para scopus.
                        id.load_query(args.query)
                    search_handler.append_partial_res( id.search() )
                    id.export_csv()
                    del id
        except Exception:
            traceback.print_exc()
    #del repos

    print( str(search_handler) )
    print("Fin de ejecución")