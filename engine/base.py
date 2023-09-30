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
        Cosas protegidas de la clase BasicEngine
    """
    _cfg_dict = {}
    _results_columns = ['Prueba', 'Atomic', 'Bomb']  # FIXME: Esto lo tengo que sacar del configure()

    _base_dict_df = {  # Nombre del archivo - artículo descargado
        'Nombre de archivo': 'string',
        # Título del artículo
        'Título': 'string',
        # Autor(es) del artículo
        'Autor(es)': 'string',
        # Indica si es un estudio primario
        'Estudio primario': 'boolean',
        # Indica si su análisis está pendiente
        'Pendiente analizar': 'boolean',
        # Repositorio donde fue hallado el artículo
        'Medio de publicación': 'string',
        # Año de publicación
        'Año de publicación': 'int32',
        # Fecha de fichaje
        'Fecha de fichaje': 'datetime64[ns]',
        # Abstract
        'Abstract': 'string',
        # Palabras clave del artículo
        'Palabras clave': 'string',
        # Trabajos de otros autores mencionados en la publicación que podrían
        #    ser útiles para ampliar el tema
        'Referencias a otros artículos': 'string',
        # Aspectos metodológicos o conceptuales angulares para la investigación
        'Fortalezas': 'string',
        # Aspectos que no están bien desarrollados o no resultan claros
        'Debilidades': 'string',
        # Posibles líneas de trabajo para la tesis
        'Oportunidades': 'string'
    }

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

        print(self._cfg_dict)
        return __success_flag

    # TODO: Migrar logging acá?
