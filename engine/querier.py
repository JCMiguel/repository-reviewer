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

    def __check_config(self) -> bool:
        return self.__config_loaded

    def configure(self):
        print("Cargando archivo de configuración")
        if self._configure_repos() and self._configure_params():
            self.__config_loaded = True
        else:
            self.__config_loaded = False

    def search(self, debug: bool):
        if not self.__check_config():
            print("ERROR: Querier no configurado!")
            return

        if debug:
            print("El debug esta habilitado")

        # TODO: validar errores en el config.yml. hay que asegurar que exista todo lo necesario.
        # Ejemplo: url, params, apikey, etc.
        # Y que exista una clase llamada como en el config.yml

        # TODO: Levantar estructura de la tabla de artículos del config, quizás un archivo results_config.yml
        # Mi idea para este config es la siguiente:
        # [NO] Definir en base.py una lista de campos elementales y clave ['abstract', 'title', 'keywords', ...]
        # [OK] Pasarle esa lista al constructor de abc_def.py, que por defecto esté vacía, pero que si viene presente
        #  que arme otro formato de salida de artículos en función de los parámetros de la lista (línea 105)
        # [  ] Que el formato del results_config pueda tener N campos de usuario y un subcampo key para indicar
        #  cuáles son campos clave de la salida del querier. Estos campos key tendrían relación con los elementos de la
        #  lista indicada en la primera viñeta.
        #  La idea de esto es que el usuario pueda definir un campo "Abstract" o "Resumen" para la tabla, pero que con
        #  la referencia del "key" el script sepa que ambos textos corresponden al elemento "abstract" en las queries de
        #  búsqueda.

        print("Cargando clases de repositorios")
        for repo_name in self._cfg_dict['repos'].keys():
            try:
                # La línea siguiente invoca a la clase dentro del package.
                # Ejemplo: invoca al constructor ieee() de repos.ieee_def
                if self._cfg_dict['repos'][repo_name]['enabled'] is True:
                    repo = getattr(globals()[repo_name + '_def'], repo_name)(repo_params=self._cfg_dict['repos'][repo_name],
                                                                             config_params=self._cfg_dict['params'],
                                                                             debug=debug)
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
