#!/usr/bin/python3
# -*- coding: utf8

import requests
import pandas as pd
from abc import ABC, abstractmethod

# Clase abstracta que define las características básicas de un repositorio
class repo(ABC):
    '''
        Abstract class for repository definition.
    '''
    def __init__(self, repo_params:dict, config_params:dict, debug:bool=False):
        self.url = repo_params['url']
        self.apikey = repo_params['apikey']
        self.dictionary = {}
        self.query_params = {}
        self.config_params = { 'validate-certificate': True } | config_params # Mezcla de diccionarios
        self.debug = debug
        self.build_dictionary()
        self.validate_dictionary()
        self.add_query_param(self.apikey,'apikey')
        self.add_query_param('25','max_records_per_page')
        self.articles_dataframe = pd.DataFrame(columns=["Title", "Found in", "Year"])
         

    @abstractmethod
    def build_dictionary(self):
        '''
            This function builds a dictionary to translate the script params into query
            params for each repo.
        '''
        pass

    def validate_dictionary(self):
        if "default" not in self.dictionary:
            raise ValueError("Missing field 'default' in " + type(self).__name__ + "'s dictionary!")
        elif "title" not in self.dictionary:
            raise ValueError("Missing field 'title' in " + type(self).__name__ + "'s dictionary!")
        elif "from_year" not in self.dictionary:
            raise ValueError("Missing field 'from_year' in " + type(self).__name__ + "'s dictionary!")
        elif "max_records_per_page" not in self.dictionary:
            raise ValueError("Missing field 'from_year' in " + type(self).__name__ + "'s dictionary!")
        else:
            return True

    def add_query_param(self, value:str, type:str='default') -> None:
        '''This pretends do a conversion between args and api params
        
            Type could be:
                - default for all metadata in data base.
                - abstract
                - title
        '''
        self.query_params[self.dictionary[type]] = value
        pass

    def get_config_param(self, name:str):
        '''
        '''
        #print(self.config_params)
        if name in self.config_params.keys():
            return self.config_params[name]
        else:
            return ''

    #@abstractmethod
    #def validate_params():
    #    pass

    @abstractmethod
    def search(self):
        pass

    def debug_enabled(self):
        print("DEBUG: " + str(self.debug))
        return self.debug

    def add_to_dataframe(self,title:str="", year:str=""):
        self.articles_dataframe.loc[len(self.articles_dataframe)] = [title, type(self).__name__, year]
        pass


    def say_hello(self):
        print("Hola! Soy " + type(self).__name__)

    def export_csv(self):
        self.articles_dataframe.to_csv('table_articles.csv', encoding='utf-8')
        #print("Soy " + type(self).__name__+ ", pero aun no se exportar a CSV! Toy chiquito :3")
