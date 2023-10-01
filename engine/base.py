#!/usr/bin/python3
# -*- coding: utf8

import yaml
import logging
import logging.config
import traceback


class BasicEngine:
    """
        Esta clase pretende unificar una base funcional para el
        querier, el indexer y cualquier otro futuro motor.
    """
    articles_fn = 'results\\table_articles.csv'

    def __init__(self):
        pass

    """
        Cosas protegidas de la clase BasicEngine
    """
    _cfg_dict = {}

    def _configure_repos(self) -> bool:
        return self.__read_yaml(self.__repo_config_filename)

    def _configure_params(self) -> bool:
        return self.__read_yaml(self.__params_config_filename)

    """
        Elementos privados de la clase BasicEngine
    """
    __repo_config_filename = "config/repo_config.yml"
    __params_config_filename = "config/params_config.yml"

    def __read_yaml(self, file_path: str) -> bool:
        __success_flag = True
        try:
            with open(file=file_path, mode="r", encoding="utf-8") as f:
                self._cfg_dict = self._cfg_dict | yaml.safe_load(f)
        except EnvironmentError:
            __success_flag = False

        return __success_flag

    # TODO: Migrar logging acá?
