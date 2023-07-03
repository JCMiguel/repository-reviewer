import urllib.parse
import requests
import json
import pandas as pd
from . import abc_def

# Clase dedicada a búsquedas en Scopus
class scopus(abc_def.repo):
    def __init__(self, repo_params: dict, config_params: dict, debug: bool = False):
        super().__init__(repo_params, config_params, debug)
        self.logger.debug(self.url)

    def build_dictionary(self):
        self.dictionary['content'] = 'TITLE-ABS-KEY'
        self.dictionary['apikey'] = 'apikey'
        self.dictionary['title'] = 'TITLE'
        self.dictionary['abstract'] = 'ABS'
        self.dictionary['keyword'] = 'KEY'
        self.dictionary['from_year'] = 'date'
        self.dictionary['to_year'] = 'end_year'
        self.dictionary['max_records_per_page'] = 'count'
        self.dictionary['first_index'] = 'start'
        self.dictionary['query'] = 'query'

    def parse_query(self, query: str) -> str:
        """
            TODO: Documentar esta función
        """
        self.logger.debug(query)
        # query = '{ \"keyword\": [ \"histology\", \"histology\" ], \"title\": \"xai\"}'
        query_dict = json.loads(query)  # Esta función me convierte el string en dictionary
        self.logger.debug(f"query_dict={query_dict}")
        # * * * SOME MAGIC HAPPENS HERE * * *
        parsed_query = '('
        for element in query_dict.items():
            parsed_query += '('
            self.logger.debug(f"{element[0]}:{element[1]}")
            if isinstance(element[1],list):
                for sub_elem in range(0,len(element[1])):
                    parsed_query += f'({str(self.dictionary[element[0]])}({str(element[1][sub_elem])}))'
                parsed_query = parsed_query.replace(')(', ') OR (')
            else:
                parsed_query += f'{str(self.dictionary[element[0]])}({str(element[1])})'
            parsed_query += ')'
        parsed_query = parsed_query.replace(')(', ') AND (')
        parsed_query += ')'
        self.logger.debug(parsed_query)
        # query= '((KEY(histology)OR(KEY(histology))) AND (TITLE(xai)))'
        # query= '((TITLE(xai) OR TITLE(ai)) AND (TITLE-ABS-KEY(histopathology)))'
        return parsed_query

    def build_scopus_query(self):
        """
            Esta función pretende mover los campos TITLE, TITLE-ABS-KEY y ABS adentro del parámetro query
            Esto es porque la API de Scopus espera recibirlos en dicho parámetro.

            Ejemplo:
                'query=KEY(histology)%20and%20TITLE(xai)'
        """
        self.logger.debug("TODO: PENDIENTE HACER ESTA FUNCIÓN")
        raise ValueError(f"Function build_scopus_query not implemented in {type(self).__name__}! Use --query")
        pass

    def search(self):
        """
            Búsqueda e
        """
        self.logger.info("Do real searching in repo...")
        self.logger.debug(str(self.query_params))
        if 'query' not in self.query_params:
            self.logger.debug("Estoy buscando por parámetros y puedo reciclar el campo query")
            self.build_scopus_query()
        params = urllib.parse.urlencode(self.query_params, quote_via=urllib.parse.quote)
        ans = requests.get(self.url, params=params, verify=self.get_config_param('validate-certificate'))
        # ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
        self.logger.debug(ans.url)
        records_per_page = int(self.query_params[self.dictionary['max_records_per_page']])

        if self.debug_enabled():
            self.logger.warning("Debug activado: Limitando cantidad de registros")
            total_records_count = records_per_page*3
        else:
            # TODO: contemplar que pasa si la busqueda no produce resultados o si se alcanza el limite diario
            total_records_count = ans.json()['search-results']['opensearch:totalResults']

        pub_year_array = []
        for art in range(int(total_records_count)):
            if art and art%records_per_page == 0:
                self.add_query_param(str(art), 'first_index')
                ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
                self.logger.debug(ans.url)
            # print("Debug:" + str(art) + " of " + str(ans.json()['total_records']))
            # print(' - ' + ans.json()['articles'][art%records_per_page]['title'])
            pub_year = ans.json()['search-results']['entry'][art%records_per_page]['prism:coverDate']
            self.add_to_dataframe(ans.json()['search-results']['entry'][art%records_per_page]['dc:title'], pub_year)
            pub_year_array.append( pub_year )
        self.export_csv()
        return self.build_report(pub_year_array)
