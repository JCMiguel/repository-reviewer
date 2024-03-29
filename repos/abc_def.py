#!/usr/bin/python3
# -*- coding: utf8

import requests
import logging
import logging.config
import pandas as pd
from historic.report import Report
from datetime import datetime
from abc import ABC, abstractmethod


RESULT_SEPARATOR = '^'

# Clase abstracta que define las características básicas de un repositorio
class repo(ABC):
    """
        Abstract class for repository definition.
    """

    def __init__(self, repo_params: dict, config_params: dict, debug: bool = False):
        self.url = repo_params['url']
        self.apikey = repo_params['apikey']
        self.dictionary = {}
        self.query_params = {}
        self.config_params = {'validate-certificate': True} | config_params  # Mezcla de diccionarios
        self.debug = debug
        self.build_dictionary()
        self.validate_dictionary()
        self.add_query_param(self.apikey, 'apikey')
        self.add_query_param('25', 'max_records_per_page')
        self.articles_dataframe = repo.init_dataframe(self.config_params)

        # Config de Logs
        logging.config.dictConfig(self.config_params['logs'])
        if "logger" in repo_params:
            self.logger = logging.getLogger(repo_params['logger'])
        else:
            self.logger = logging.getLogger('root')

    @classmethod
    def init_dataframe(self, config_params: dict = None):
        order_of_columns = ['title', 'repo', 'year', 'abstract', 'pub_type', 'authors', 'doi']
        # Renombro la columna, si es que existe
        for column in config_params['results_format']:
            if column.get('key') is not None and column.get('key') != '' and \
                    column.get('column_name') is not None:
                order_of_columns[order_of_columns.index(column['key'])] = column['column_name']
        return pd.DataFrame(columns=order_of_columns)

    @abstractmethod
    def build_dictionary(self):
        """
            This function builds a dictionary to translate the script params into query
            params for each repo.
        """
        pass

    def validate_dictionary(self):
        """
            Esta función sirve solo para desarrollar nuevas clases de repositorios.
            Realiza una validación de que estén todos los parámetros necesarios definidos en
            la clase particular de Repo
        """
        __base_src_fields_def = ["content", "title", "abstract", "keyword", "from_year",
                                 "to_year", "max_records_per_page", "query"]
        for elem in __base_src_fields_def:
            if elem not in self.dictionary:
                raise ValueError(f"Missing field '{elem}' in {type(self).__name__}'s dictionary!")
        return True

    @abstractmethod
    def parse_query(self, query: str) -> str:
        pass

    def load_query(self, query: str) -> None:
        """
            Load a full query as a dictionary
        """
        # TODO: Esto me quedo valido solo para IEEE, tengo que cambiarlo

        self.query_params[self.dictionary['query']] = self.parse_query(query)

    def add_query_param(self, value: str, value_type: str) -> None:
        """
            This pretends to do a conversion between args and api params

            Type could be:
                - default for all metadata in database.
                - abstract
                - title
        """
        if value is not None:
            self.query_params[self.dictionary[value_type]] = value

    def get_config_param(self, name: str):
        """
        """
        # print(self.config_params)
        if name in self.config_params.keys():
            return self.config_params[name]
        else:
            return ''

    @abstractmethod
    def search(self) -> Report:
        pass

    def debug_enabled(self):
        self.logger.debug(str(self.debug))
        return self.debug

    def add_to_dataframe(self, title: str = "", year: str = "", abstract: str = "",
                         pub_type: str = "", authors: str = "", doi: str = ""):
        # init_dataframe -> order_of_columns = ['title', 'repo', 'year', 'abstract', 'pub_type', 'authors', 'doi']
        self.articles_dataframe.loc[len(self.articles_dataframe)] = [title, type(self).__name__, year, abstract,
                                                                     pub_type, authors, doi]
        pass

    def say_hello(self):
        self.logger.debug("Hola! Soy " + type(self).__name__)

    @classmethod
    def export_csv(self, source_df:pd.DataFrame, filename:str):
        source_df.to_csv(filename, encoding='utf-8', index_label='ID', sep=RESULT_SEPARATOR)
        if hasattr(self, 'logger'):
            self.logger.info("{} articles exported".format(len(source_df)))

    def concat_to_dataframe(self, main_df:pd.DataFrame) -> pd.DataFrame:
        if main_df is None:
            return self.articles_dataframe
        self.logger.info("{} articles added".format(len(self.articles_dataframe)))
        return pd.concat( [main_df, self.articles_dataframe], ignore_index=True, verify_integrity=False )

    def export_dataframe(self=None):
        return repo.articles_df

    def build_report(self, publication_dates_array) -> Report:
        time_span = None
        if publication_dates_array is None:
            method = self.__class__.__name__ +".build_report( )"
            raise ValueError("On "+method+": publication_dates_array parameter must be a non-empty array")
        from_year = self.query_params.get( self.dictionary['from_year'] )
        if from_year is not None:
            to_year = self.query_params.get( self.dictionary['to_year'] )
            if to_year is None:
                to_year = datetime.now().strftime('%Y-%m-%d')
            time_span = ( from_year, to_year )
        r = Report(self.__class__.__name__, self.logger)
        r.process_dates( publication_dates_array, time_span)
        return r
