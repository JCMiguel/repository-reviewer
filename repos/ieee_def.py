import urllib.parse
import requests
import json
import pandas as pd
from . import abc_def

# Clase dedicada a búsquedas en IEEEXplore
class ieee(abc_def.repo):
    '''This is a docstring. I have created a new class'''
    def __init__(self, repo_params:dict, config_params:dict, debug:bool=False):
        super().__init__(repo_params, config_params, debug)
        self.logger.debug(self.url)

    def build_dictionary(self):
        self.dictionary['apikey'] = 'apikey'
        self.dictionary['content'] = 'metadata'
        self.dictionary['title'] = 'article_title'
        self.dictionary['abstract'] = 'abstract'
        self.dictionary['keyword'] = 'index_terms'
        self.dictionary['from_year'] = 'start_year'
        self.dictionary['to_year'] = 'end_year'
        self.dictionary['max_records_per_page'] = 'max_records'
        self.dictionary['first_index'] = 'start_record'
        self.dictionary['query'] = 'querytext'

    def parse_query(self, query: str) -> str:
        # TODO: Resolver parseo de Query completa
        # Quiero llegar a esto:
        # INPUT:
        #   querier --query='("title":"xai") AND ("abstract":"histopathology")'
        # OUTPUT (IEEE):
        #   querytext=((%0A%22Document%20Title%22:%22xai%22%0A)%0AAND%0A(%0A%22Full%20Text%20Only%22:%22histopathology%22%0A)%0A)
        # Nota: Buscar por query invalidaría todos los otros argumentos para que no entren en conflicto.
        convert_dict = dict.fromkeys(self.dictionary)
        convert_dict['content'] = 'Full Text Only'
        convert_dict['title'] = 'Document Title'
        convert_dict['abstract'] = 'Abstract'
        print(query)
        # query = '{ \"title\": [ \"xai\", \"ai\" ], \"content\": \"histopathology\"}'
        query_dict = json.loads(query)  # Esta función me convierte el string en dictionary
        #print(query_dict)
        # * * * SOME MAGIC HAPPENS HERE * * *
        parsed_query = '('
        for element in query_dict.items():
            parsed_query += '('
            #print(element[1])
            if isinstance(element[1],list):
                for sub_elem in range(0,len(element[1])):
                    parsed_query += f'("{str(convert_dict[element[0]])}":"{str(element[1][sub_elem])}")'
                parsed_query = parsed_query.replace(')(', ') OR (')
            else:
                parsed_query += f'"{str(convert_dict[element[0]])}":"{str(element[1])}"'
            parsed_query += ')'
        parsed_query = parsed_query.replace(')(', ') AND (')
        parsed_query += ')'
        #print(parsed_query)
        #query = '(("Document Title":xai) AND ("Full Text Only":histopathology))'
        return parsed_query

    def search(self):
        '''Búsqueda e'''
        self.logger.info("Do real searching in repo...")
        self.logger.debug(str(self.query_params))
        params = urllib.parse.urlencode(self.query_params, quote_via=urllib.parse.quote)
        ans = requests.get(self.url,params=params, verify=self.get_config_param('validate-certificate'))
        self.logger.debug(ans.url)
        records_per_page = int(self.query_params[self.dictionary['max_records_per_page']])
        total_records_count = ans.json()['total_records']

        if self.debug_enabled():
            self.logger.warning("Debug activado: Limitando cantidad de registros")
            total_records_count = min( records_per_page*3, ans.json()['total_records'] )

        pub_year_array = []
        for art in range(int(total_records_count)):
            if art and art%records_per_page == 0:
                self.add_query_param(str(art),'first_index')
                ans = requests.get(self.url, params=self.query_params,
                                   verify=self.get_config_param('validate-certificate'))
                self.logger.debug(ans.url)
            #print("Debug:" + str(art) + " of " + str(total_records_count) + "/" + str(ans.json()['total_records']) + " -- index: " + str(art%records_per_page) )
            #print(' - ' + ans.json()['articles'][art%records_per_page]['title'])
            pub_year = ans.json()['articles'][art%records_per_page]['publication_year']
            self.add_to_dataframe(ans.json()['articles'][art%records_per_page]['title'], pub_year)
            pub_year_array.append( pub_year )
        return self.build_report(pub_year_array)
