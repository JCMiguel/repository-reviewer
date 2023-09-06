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
    def __init__(self):
        pass

    """
        Cosas privadas de la clase BasicEngine
    """
    __cfg_dict = {}

    """
        Métodos públicos de la clase BasicEngine
    """
    def read_yaml(self, file_path: str):
        with open(file_path, "r") as f:
            self.__cfg_dict = yaml.safe_load(f)

    # TODO: Migrar logging acá
