#!/usr/bin/python3
# -*- coding: utf8

import yaml
import logging
import logging.config
import traceback
from repos import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def querier(debug: bool, query: str = "", content: str = "", from_year: str = "",
            to_year: str = "", title: str = "", abstract: str = "", redirect_logs = False):
    print("Cargando archivo de configuración")
    cfg = read_yaml("config/querier_config.yml")  # TODO: Pendiente hacer chequeo de errores

    if debug:
        print("El debug esta habilitado")

    print("Cargando clases de repositorios")
    for repo in cfg['repos'].keys():
        try:
            # La línea siguiente invoca a la clase dentro del package.
            # Ejemplo: invoca al constructor ieee() de repos.ieee_def
            if cfg['repos'][repo]['enabled'] is True:
                id = getattr(globals()[repo + '_def'], repo)(cfg['repos'][repo], cfg['params'], debug)
                if id is not None:
                    id.say_hello()
                    if query == "" or query is None:
                        id.add_query_param(content, 'content')
                        id.add_query_param(from_year, 'from_year')
                        id.add_query_param(title, 'title')
                        id.add_query_param(to_year, 'to_year')
                        id.add_query_param(abstract, 'abstract')
                    else:
                        id.load_query(args.query)
                    id.search()
                    del id
        except Exception:
            traceback.print_exc()
    print("Fin de ejecución")
