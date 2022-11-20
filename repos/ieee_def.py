import requests
import pandas as pd
from . import abc_def

# Clase dedicada a búsquedas en IEEEXplore
class ieee(abc_def.repo):
    '''This is a docstring. I have created a new class'''
    def __init__(self, repo_params:dict, config_params:dict, debug:bool=False):
        super().__init__(repo_params, config_params, debug)
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
        print("DEBUG: " + str(self.query_params))
        ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
        print("DEBUG: " + ans.url)
        records_per_page = int(self.query_params[self.dictionary['max_records_per_page']])
        
        if self.debug_enabled():
            print("Limitando cantidad de registros")
            total_records_count = records_per_page*3
        else:
            total_records_count = ans.json()['total_records']

        for art in range(int(total_records_count)):
            if art and art%records_per_page == 0:
                self.add_query_param(str(art),'first_index')
                ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
                print("DEBUG: " + ans.url)
            #print("Debug:" + str(art) + " of " + str(ans.json()['total_records']))
            #print(' - ' + ans.json()['articles'][art%records_per_page]['title'])
            self.add_to_dataframe(ans.json()['articles'][art%records_per_page]['title'], ans.json()['articles'][art%records_per_page]['publication_year'])
        self.export_csv()