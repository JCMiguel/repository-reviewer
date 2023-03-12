import requests
import pandas as pd
from . import abc_def

# Clase dedicada a búsquedas en la base de datos Pubmed del NCBI
class pubmed(abc_def.repo):
    '''
    Class to excecute searches in the NCBI (National Center for Biotechnology Information) PubMed database.
    Extends a generic abstract interface definition called abd_ref.repo to handle any API repository'''
    def __init__(self, repo_params:dict, config_params:dict, debug:bool=False):
        super().__init__(repo_params, config_params, debug)
        self.dictionary['tool'] = 'tool'
        self.dictionary['email'] = 'email'
        self.dictionary['format'] = 'retmode'
        self.add_query_param("repository-reviewer", 'tool')         # TODO: Obtener este valor del config.yaml params
        self.add_query_param("mlbassi@frba.utn.edu.ar", 'email')    # TODO: Obtener este valor del config.yaml params
        self.add_query_param("json", 'format')    # TODO: Obtener este valor del config.yaml params
        #self.add_query_param("total_records_count",'retmax')
        print(self.url)

    def build_dictionary(self):
        self.dictionary['default'] = 'term'
        self.dictionary['apikey'] = 'api_key'
        self.dictionary['title'] = 'title'
        self.dictionary['from_year'] = 'mindate'
        self.dictionary['end_year'] = 'maxdate'
        self.dictionary['max_records_per_page'] = 'retmax'
        self.dictionary['first_index'] = 'retstart'
        

    def search(self):
        '''Specific method for querying the database.
        For more information see https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch'''
        print("Do real searching in repo...")
        print("DEBUG: " + str(self.query_params))
        ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
        print("DEBUG: " + ans.url)
        records_per_page = int(self.query_params[self.dictionary['max_records_per_page']])
        
        if self.debug_enabled():
            print("Limitando cantidad de registros")
            print("DEBUG: ans:\n", ans.json() )
            exit()

            total_records_count = records_per_page*3
        else:
            total_records_count = ans.json()['total_records']

        for art in range(int(total_records_count)):
            if art and art%records_per_page == 0:
                self.add_query_param(str(art),'first_index')
                ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
                print("DEBUG: " + ans.url)
                print("Debug:" + str(art) + " of " + str(ans.json()['total_records']))
            #print(' - ' + ans.json()['articles'][art%records_per_page]['title'])
            self.add_to_dataframe(ans.json()['articles'][art%records_per_page]['title'], ans.json()['articles'][art%records_per_page]['publication_year'])
        self.export_csv()


    def __exec_eSearch(self) -> dict:
        pass


    def __exec_Summary(self, search_results:dict):
        pass