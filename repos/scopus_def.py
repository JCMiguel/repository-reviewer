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

    def add_query_param(self, value: str, value_type: str) -> None:
        allowed_items = ["content", "title", "abstract", "keyword", "from_year"]
        previous_content = ""
        if value_type in allowed_items:
            if self.dictionary['query'] in self.query_params:
                previous_content = self.query_params[self.dictionary['query']]
            if value is not None and value != "":
                if value_type != "from_year":
                    current_param = f'{self.dictionary[value_type]}({value})'
                else:
                    current_param = f'{self.dictionary[value_type]}={value}'
                if previous_content != "":
                    previous_content += f' {current_param}'
                else:
                    previous_content = current_param
                print(current_param)
            self.query_params[self.dictionary['query']] = previous_content
            print(previous_content)
            print(self.query_params)
        else:
            super().add_query_param(value, value_type)

    def search(self):
        """
            Búsqueda e
        """
        self.logger.info("Do real searching in repo...")
        self.logger.debug(str(self.query_params))

        params = urllib.parse.urlencode(self.query_params, quote_via=urllib.parse.quote, safe='()')
        ans = requests.get(self.url, params=params, verify=self.get_config_param('validate-certificate'))
        # ans = requests.get(self.url,params=self.query_params, verify=self.get_config_param('validate-certificate'))
        self.logger.debug(ans.url)
        records_per_page = int(self.query_params[self.dictionary['max_records_per_page']])
        total_records_count = ans.json()['search-results']['opensearch:totalResults']

        if self.debug_enabled():
            self.logger.warning("Debug activado: Limitando cantidad de registros")
            # total_records_count = records_per_page*3
            total_records_count = min(records_per_page * 3,
                                      int(ans.json()['search-results']['opensearch:totalResults']))
        # else:
        #     # TODO: contemplar que pasa si la busqueda no produce resultados o si se alcanza el limite diario
        #     total_records_count = ans.json()['search-results']['opensearch:totalResults']

        pub_year_array = []
        for art in range(int(total_records_count)):
            if art and art % records_per_page == 0:
                self.add_query_param(str(art), 'first_index')
                ans = requests.get(self.url, params=self.query_params,
                                   verify=self.get_config_param('validate-certificate'))
                self.logger.debug(ans.url)

            article = ans.json()['search-results']['entry'][art % records_per_page]

            error = article.get('error')
            if error:
                self.logger.error('This search has encountered a problem:' + str(ans.json()['search-results']) )
                break

            pub_year = article.get('prism:coverDate')
            if pub_year is None:
                self.logger.warning('This article has no publication date:' + str(article))
                pub_year = ""

            self.add_to_dataframe(title=article.get('dc:title', "Error getting title"), year=pub_year)
            pub_year_array.append(pub_year)
        return self.build_report(pub_year_array)
