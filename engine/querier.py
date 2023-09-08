#!/usr/bin/python3
# -*- coding: utf8

from engine.base import BasicEngine
import yaml
import traceback
from os import path
from historic.history import *
from repos import *


def build_querier_dictionary(query: str = "", content: str = "", from_year: str = "", to_year: str = "",
                             title: str = "", abstract: str = "", keywords: str = "") -> dict:
    args = dict()
    if len(content) > 0:
        args['content'] = content
    else:
        args['content'] = None

    if len(from_year) > 0:
        args['fromYear'] = from_year
    else:
        args['fromYear'] = None

    if len(title) > 0:
        args['title'] = title
    else:
        args['title'] = None

    if len(to_year) > 0:
        args['toYear'] = to_year
    else:
        args['toYear'] = None

    if len(abstract) > 0:
        args['abstract'] = abstract
    else:
        args['abstract'] = None

    if len(query) > 0:
        args['query'] = query
    else:
        args['query'] = None
    return args


class Querier(DataSearch, BasicEngine):
    """
        Una clase destinada a hacer la busqueda de artículos
    """
    def __init__(self, search_params: dict):
        BasicEngine.__init__(self)
        DataSearch.__init__(self, search_params)
        self.__config_loaded = False
        self.__config_filename = "config/querier_config.yml"

    def __check_config(self) -> bool:
        return self.__config_loaded

    def configure(self):
        print("Cargando archivo de configuración")
        if self._load_config(self.__config_filename):
            self.__config_loaded = True
        else:
            self.__config_loaded = False

    def search(self, debug: bool):
        if not self.__check_config():
            print("ERROR: Querier no configurado!")
            return

        # cfg = self._read_yaml("config/querier_config.yml")  # TODO: Pendiente hacer chequeo de errores

        if debug:
            print("El debug esta habilitado")

        print("Cargando clases de repositorios")
        print(self._cfg_dict)
        for repo_name in self._cfg_dict['repos'].keys():
            try:
                # La línea siguiente invoca a la clase dentro del package.
                # Ejemplo: invoca al constructor ieee() de repos.ieee_def
                if self._cfg_dict['repos'][repo_name]['enabled'] is True:
                    repo = getattr(globals()[repo_name + '_def'], repo_name)(self._cfg_dict['repos'][repo_name],
                                                                             self._cfg_dict['params'],
                                                                             debug)
                    if repo is not None:
                        repo.say_hello()
                        if self._search_params['query'] == "" or self._search_params['query'] is None:
                            repo.add_query_param(self._search_params['content'], 'content')
                            repo.add_query_param(self._search_params['fromYear'], 'from_year')
                            repo.add_query_param(self._search_params['title'], 'title')
                            repo.add_query_param(self._search_params['toYear'], 'to_year')
                            repo.add_query_param(self._search_params['abstract'], 'abstract')
                        else:
                            repo.load_query(self._search_params['query'])
                        self.append_partial_res(repo.search())
                        repo.export_csv()
                        del repo
            except Exception:
                traceback.print_exc()
        History.Add(self)


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


# TODO: Migrar a clase Querier
def querier_func(debug: bool, query: str = "", content: str = "", from_year: str = "",
            to_year: str = "", title: str = "", abstract: str = "", keywords: str = "", redirect_logs = False):
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
                        id.load_query(query)
                    id.search()
                    del id
        except Exception:
            traceback.print_exc()
    print("Fin de ejecución")
