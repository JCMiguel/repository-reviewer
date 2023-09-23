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

    def __read_yaml(self, file_path: str) -> bool:
        __success_flag = True
        try:
            with open(file_path, "r") as f:
                self._cfg_dict = yaml.safe_load(f)
        except EnvironmentError:
            __success_flag = False
        return __success_flag

    """
        Métodos protegidos de la clase BasicEngine
    """
    def _load_config(self, file_path: str) -> bool:
        return self.__read_yaml(file_path)



    # TODO: Migrar logging acá?
