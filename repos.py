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
    def __init__(self, basePath:str, apikey:str, debug:bool=False):
        self.basePath = basePath
        self.apikey = apikey
        self.url = basePath
        self.dictionary = {}
        self.params = {}
        self.debug = debug
        self.build_dictionary()
        self.validate_dictionary()
        self.add_query_param(apikey,'apikey')
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
        self.params[self.dictionary[type]] = value
        pass

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



# Clase dedicada a búsquedas en IEEEXplore
class ieee(repo):
    '''This is a docstring. I have created a new class'''
    def __init__(self, basePath:str, apikey:str, debug:bool=False):
        super().__init__(basePath, apikey, debug)
        print(self.url)

    def build_dictionary(self):
        self.dictionary['default'] = 'meta_data'
        self.dictionary['apikey'] = 'apikey'
        self.dictionary['title'] = 'title'
        self.dictionary['from_year'] = 'start_year'
        self.dictionary['end_year'] = 'end_year'
        self.dictionary['max_records_per_page'] = 'max_records'
        self.dictionary['first_index'] = 'start_record'

    def search(self):
        '''Búsqueda e'''
        print("Do real searching in repo...")
        print("DEBUG: " + str(self.params))
        ans = requests.get(self.url,params=self.params)
        print("DEBUG: " + ans.url)
        records_per_page = int(self.params[self.dictionary['max_records_per_page']])
        
        if self.debug_enabled():
            print("Limitando cantidad de registros")
            total_records_count = records_per_page*3
        else:
            total_records_count = ans.json()['total_records']

        for art in range(int(total_records_count)):
            if art and art%records_per_page == 0:
                self.add_query_param(str(art),'first_index')
                ans = requests.get(self.url,params=self.params)
                print("DEBUG: " + ans.url)
            #print("Debug:" + str(art) + " of " + str(ans.json()['total_records']))
            #print(' - ' + ans.json()['articles'][art%records_per_page]['title'])
            self.add_to_dataframe(ans.json()['articles'][art%records_per_page]['title'], ans.json()['articles'][art%records_per_page]['publication_year'])
        self.export_csv()




# Clase dedicada a búsquedas en Scopus
class scopus(repo):
    def __init__(self, basePath: str, apikey: str, debug:bool=False):
        super().__init__(basePath, apikey, debug)
        print(self.url)

    def build_dictionary(self):
        self.dictionary['default'] = 'query'
        self.dictionary['apikey'] = 'apikey'
        self.dictionary['title'] = 'title'
        self.dictionary['from_year'] = 'date'
        self.dictionary['end_year'] = 'end_year'
        self.dictionary['max_records_per_page'] = 'count'
        self.dictionary['first_index'] = 'start'

    def search(self):
        '''Búsqueda e'''
        print("Do real searching in repo...")
        print("DEBUG: " + str(self.params))
        ans = requests.get(self.url,params=self.params)
        print("DEBUG: " + ans.url)
        records_per_page = int(self.params[self.dictionary['max_records_per_page']])

        if self.debug_enabled():
            print("Limitando cantidad de registros")
            total_records_count = records_per_page*3
        else:
            total_records_count = ans.json()['search-results']['opensearch:totalResults']

        for art in range(int(total_records_count)):
            if art and art%records_per_page == 0:
                self.add_query_param(str(art),'first_index')
                ans = requests.get(self.url,params=self.params)
                print("DEBUG: " + ans.url)
            #print("Debug:" + str(art) + " of " + str(ans.json()['total_records']))
            #print(' - ' + ans.json()['articles'][art%records_per_page]['title'])
            self.add_to_dataframe(ans.json()['search-results']['entry'][art%records_per_page]['dc:title'],
                                  ans.json()['search-results']['entry'][art%records_per_page]['prism:coverDate'])
        self.export_csv()