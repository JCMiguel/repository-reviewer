#!/usr/bin/python3
# -*- coding: utf8

import requests
import logging
import logging.config
import pandas as pd
from abc import ABC, abstractmethod


# Clase abstracta que define las características básicas de un repositorio
class repo(ABC):
    """
        Abstract class for repository definition.
    """
    articles_fn = 'table_articles.csv'
    articles_df = pd.DataFrame(columns=["Title", "Found in", "Year"])

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
        self.articles_dataframe = pd.DataFrame(columns=["Title", "Found in", "Year"])

        # Config de Logs
        logging.config.dictConfig(self.config_params['logs'])
        if "logger" in repo_params:
            self.logger = logging.getLogger(repo_params['logger'])
        else:
            self.logger = logging.getLogger('root')

    @abstractmethod
    def build_dictionary(self):
        """
            This function builds a dictionary to translate the script params into query
            params for each repo.
        """
        pass

    def validate_dictionary(self):
        items = ["content", "title", "abstract", "keyword", "from_year",
                 "to_year", "max_records_per_page", "query"]
        for item in items:
            if item not in self.dictionary:
                raise ValueError(f"Missing field '{item}' in {type(self).__name__}'s dictionary!")
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
        pass

    def add_query_param(self, value: str, value_type: str) -> None:
        """
            This pretends to do a conversion between args and api params

            Type could be:
                - default for all metadata in database.
                - abstract
                - title
        """
        self.query_params[self.dictionary[value_type]] = value
        pass

    def get_config_param(self, name: str):
        """
        """
        # print(self.config_params)
        if name in self.config_params.keys():
            return self.config_params[name]
        else:
            return ''

    # @abstractmethod
    # def validate_params():
    #     pass

    @abstractmethod
    def search(self):
        pass

    def debug_enabled(self):
        self.logger.debug(str(self.debug))
        return self.debug

    def add_to_dataframe(self, title: str = "", year: str = ""):
        self.articles_dataframe.loc[len(self.articles_dataframe)] = [title, type(self).__name__, year]
        pass

    def say_hello(self):
        self.logger.debug("Hola! Soy " + type(self).__name__)

    def export_csv(self):
        # Era un repo mas viejecito (1.3.4) y me olvide como hacer appends...
        # repo.articles_df = repo.articles_df.append( self.articles_dataframe, ignore_index=True, verify_integrity=False)
        # Mejor recurrir a una version mas joven (2.0.0)
        repo.articles_df = pd.concat( [repo.articles_df, self.articles_dataframe], ignore_index=True, verify_integrity=False )
        repo.articles_df.to_csv(repo.articles_fn, encoding='utf-8')
        self.logger.info("{} articles exported".format(len(self.articles_dataframe)))
        # print("Soy " + type(self).__name__+ ", pero aun no se exportar a CSV! Toy chiquito :3")
