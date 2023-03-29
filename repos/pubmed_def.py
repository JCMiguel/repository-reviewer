import requests
import pandas as pd
from . import abc_def
from datetime import datetime as dt

def date_format( pubmed_style_date:str ) -> str:
    for i, format in enumerate(['%Y %b %d', '%Y %b', '%Y']):
        try:
            date = dt.strptime( pubmed_style_date, format )
            return dt.strftime( date, '%Y-%m-%d' )
        except: # TODO: Debatir como solucionar estas excepciones.
            print('ERROR : ({}) can not convert format from {} to YYYY-MM-DD'.format(i, pubmed_style_date))
    return pubmed_style_date

# Clase dedicada a búsquedas en la base de datos Pubmed del NCBI
class pubmed(abc_def.repo):

    _method_eSearch = '/esearch.fcgi'
    _method_eSummary = '/esummary.fcgi'
    _p_search_ids = 'idlist'
    _p_summary_ids = 'uids'
    _p_usehistory = 'usehistory'
    _p_query_key_search = 'querykey'
    _p_query_key_summary = 'query_key'
    _p_WebEnv_search = 'webenv'
    _p_WebEnv_summary = 'WebEnv'
    _f_ans_result = 'result'
    _f_fail_result = 'esummaryresult'

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
        #self.add_query_param(total_records_count,'retmax')
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
        print("DEBUG: " + str(self.query_params))
        
        idxs_dict = None
        if self.debug_enabled():
            #records_per_page = int(self.query_params[self.dictionary['max_records_per_page']])
            records_per_page = 3 # HACK
            idxs_dict = {
                'retstart': '0',
                'retmax': records_per_page
            }            
        results = self.__exec_eSearch( idxs_dict, use_history=True )
        
        if self.debug_enabled():
            print("Limitando cantidad de registros")
            print("DEBUG: :\n Cant de registros encontrados:", results['count'] )
            #total_records_count = records_per_page*3
        else:
            total_records_count = results['count']

        summ = self.__exec_Summary( results, idxs_dict, use_history=True )
        print("DEBUG: results... ", results )

        articles = summ[pubmed._p_summary_ids]
        for art in articles:
            self.add_to_dataframe( summ[art]['title'], date_format(summ[art]['pubdate']) )
        self.export_csv()


    def __exec_eSearch(self, index_constraint:dict=None, use_history=False, db='pubmed') -> dict:
        specific_params = {pubmed._p_usehistory: 'n', 'db': db}
        if use_history:
            specific_params[pubmed._p_usehistory] = 'y'
        if index_constraint:
            specific_params |= index_constraint

        ans = requests.get( self.url+pubmed._method_eSearch, params=self.query_params|specific_params, verify=self.get_config_param('validate-certificate'))
        if not ans.ok:
            print('ERROR: on __exec_eSearch: not ans.ok. REASON:', ans.reason )
        else:
            print('DEBUG: eSearch url', ans.url )
        return ans.json()['esearchresult']


    def __exec_Summary(self, eSearch_results:dict, index_constraint:dict=None, use_history=False, db='pubmed') -> dict:
        specific_params = {pubmed._p_usehistory: 'n', 'db': db}
        if use_history:
            specific_params[pubmed._p_usehistory] = 'y'
            specific_params[pubmed._p_WebEnv_summary] = eSearch_results[pubmed._p_WebEnv_search]
            specific_params[pubmed._p_query_key_summary] = eSearch_results[pubmed._p_query_key_search]
        else:
            if index_constraint:
                begin = index_constraint['retstart']
                end = min(index_constraint['retmax'], eSearch_results['count'])
                specific_params['id'] = eSearch_results[pubmed._p_search_ids][begin:end]
            else:
                specific_params['id'] = eSearch_results[pubmed._p_search_ids]
            raise NotImplemented("Hay que cargar la lista de IDs del eSearch_results en el nuevo GET cuando usehistory=False")

        ans = requests.get( self.url+pubmed._method_eSummary, params=self.query_params|specific_params, verify=self.get_config_param('validate-certificate'))
        if not ans.ok:
            print('ERROR: on __exec_eSummary: not ans.ok. REASON:', ans.reason )
        else:
            print('DEBUG: eSummary url:\n', ans.url )
        try:
            result = ans.json()[pubmed._f_ans_result]
        except Exception as exc:
            result = ans.json()[pubmed._f_fail_result]
            print('ERROR: returning\n', result )
            print('DEBUG: ans.text', ans.text)
            print( exc )
            return None
        return result
