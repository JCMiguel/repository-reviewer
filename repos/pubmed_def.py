import requests
import pandas as pd
from . import abc_def
from datetime import datetime as dt

def date_format( pubmed_styled_date:str ) -> str:
    for i, format in enumerate(['%Y %b %d', '%Y %b', '%Y']):
        try:
            date = dt.strptime( pubmed_styled_date, format )
            return dt.strftime( date, '%Y-%m-%d' )
        except:
            error_msg = 'ERROR : ({}) can not convert from {} to YYYY-MM-DD format'.format(i, pubmed_styled_date)
    print( error_msg )
    return pubmed_styled_date

# Clase dedicada a búsquedas en la base de datos Pubmed del NCBI
class pubmed(abc_def.repo):

    _method_eSearch = '/esearch.fcgi'
    _method_eSummary = '/esummary.fcgi'
    _p_ids_search = 'idlist'
    _p_ids_summary = 'uids'
    _p_usehistory = 'usehistory'
    _p_query_key_search = 'querykey'
    _p_query_key_summary = 'query_key'
    _p_WebEnv_search = 'webenv'
    _p_WebEnv_summary = 'WebEnv'
    _f_search_result = 'esearchresult'
    _f_summary_result = 'result' #'esummaryresult'

    '''
    Class to excecute searches in the NCBI (National Center for Biotechnology Information) PubMed database.
    Extends a generic abstract interface definition called abd_ref.repo to handle any API repository'''
    def __init__(self, repo_params:dict, config_params:dict, debug:bool=False):
        super().__init__(repo_params, config_params, debug)
        self.extend_dictionary(config_params)



    def extend_dictionary(self, config_params):
        self.dictionary['tool'] = 'tool'
        self.dictionary['email'] = 'email'
        self.dictionary['format'] = 'retmode'
        self.add_query_param(config_params['tool-name'], 'tool')
        self.add_query_param(config_params['email'], 'email')
        self.add_query_param("json", 'format')
        # La busqueda en pubmed no es paginada, devuelve una lista de hasta 10000 IDs.
        # Reemplazo el valor 25 para max_records_per_page que setea el init de abc_def.py
        self.add_query_param('10000', 'max_records_per_page')


    def build_dictionary(self):
        self.dictionary['default'] = 'term'
        self.dictionary['apikey'] = 'api_key'
        self.dictionary['from_year'] = 'mindate'
        self.dictionary['end_year'] = 'maxdate'
        self.dictionary['max_records_per_page'] = 'retmax'
        self.dictionary['first_index'] = 'retstart'
        # Complex terms:
        self.dictionary['abstract'] = ':[Abstract]->term'
        self.dictionary['keyword'] = ':[Other Term]->term'
        self.dictionary['title'] = ':[Title]->term'
        self.dictionary['query'] = ':->term'


    def search(self):
        '''Specific method for querying the database.
        For more information see https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch'''
        self.logger.info("Do real searching in repo...")
        self.logger.debug("Un processed query_params :" + str(self.query_params))
        
        idxs_dict = None
        if self.debug_enabled():
            self.logger.warning("Debug activado: Limitando cantidad de registros")
            records_per_page = 5 #int(self.query_params[self.dictionary['max_records_per_page']])
            idxs_dict = {
                'retstart': '0',
                'retmax': records_per_page
            }            
        
        pub_years_array = []
        self._map_params_into_terms()
        results = self.__exec_eSearch( idxs_dict, use_history=True )
        self.logger.debug("Search results: "+ str(results))

        if results and results.get('count'):
            self.logger.info("Number of articles found: "+ results['count'] )

            summ = self.__exec_Summary( results, idxs_dict, use_history=True )
            self.logger.debug("Summary results: "+ str(summ))

            articles = summ[pubmed._p_ids_summary]
            for art in articles:
                pub_year = date_format(summ[art]['pubdate'])
                self.add_to_dataframe( summ[art]['title'], pub_year )
                pub_years_array.append( pub_year )
        return #self.build_report(pub_years_array)


    def parse_query(self, query: str) -> str:
        self.logger.warning( "\n CUIDADO QUE pubmed.parse_query( ) NO ESTA IMPLEMENTADO pero si en [HACK] !\n")


    def __exec_eSearch(self, index_constraint:dict=None, use_history=False, db='pubmed') -> dict:
        specific_params = {pubmed._p_usehistory: 'n', 'db': db}
        if use_history:
            specific_params[pubmed._p_usehistory] = 'y'
        if index_constraint:
            specific_params |= index_constraint

        ans = requests.get( self.url+pubmed._method_eSearch, params=self.query_params|specific_params, verify=self.get_config_param('validate-certificate'))
        return self.__validate_pubmed_answer( ans, pubmed._f_search_result )


    def __exec_Summary(self, eSearch_results:dict, index_constraint:dict=None, use_history=False, db='pubmed') -> dict:
        specific_params = {pubmed._p_usehistory: 'n', 'db': db}
        if use_history:
            specific_params[pubmed._p_usehistory] = 'y'
            specific_params[pubmed._p_WebEnv_summary] = eSearch_results[pubmed._p_WebEnv_search]
            specific_params[pubmed._p_query_key_summary] = eSearch_results[pubmed._p_query_key_search]
            if index_constraint:
                specific_params |= index_constraint
        else:
            if index_constraint:
                begin = index_constraint['retstart']
                end = min(index_constraint['retmax'], eSearch_results['count'])
                specific_params['id'] = eSearch_results[pubmed._p_ids_search][begin:end]
            else:
                specific_params['id'] = eSearch_results[pubmed._p_ids_search]
            raise NotImplemented("Escenario no probado: Debe cargar la lista de IDs del eSearch_results en el nuevo GET cuando usehistory=False")

        ans = requests.get( self.url+pubmed._method_eSummary, params=self.query_params|specific_params, verify=self.get_config_param('validate-certificate'))
        return self.__validate_pubmed_answer( ans, pubmed._f_summary_result )


    def __validate_pubmed_answer(self, ans, method_result_field:str) -> dict:
        error = res = None
        if not ans.ok: # Request level error ?
            error = ans.reason
        else:          # Search engine level error ?
            error = ans.json().get( method_result_field ).get('ERROR', False)
        if error:
            self.logger.error('on {}: REASON {{{}}}'.format(method_result_field, error) )
        else:
            self.logger.debug(method_result_field +' url:'+ str(ans.url) )
            res = ans.json().get( method_result_field )
        return res


    def _map_params_into_terms(self) -> dict:
        """
        PUBMED only has one field to upload the search-string, called "term".
        This method iterate on the query params that can be mapped and unify them on the
        required term. If for example the input query_params are:
            --content 'something' --title "star" --abstract "\"especific words\""
        With this definition of the mapping dictionary:
            self.dictionary {'content': 'term', 'title': ':[Title]->term', 'abstract': ':[Abstract]->term'}
        The resulting query_params will have this content on param 'term':
            query_params { ..., 'term': 'something AND star[Title] AND "especific words"[Abstract]
        """
        pop_list = []
        # Init a dict to save any change on the terms. The key will be the term destination.
        # The value will be a list grouping the new term with their tag, ie: new term[tag]
        term_params_mapper = dict()
        # Search for the params that have to be mapped in other term
        for mapping_param in self.query_params:
            if mapping_param.startswith(':'):
                # Cut the indicator ':' and get the search tag and the term where it has to be mapped
                tag, dest_term = mapping_param[1:].split('->')
                if dest_term not in term_params_mapper:
                    # Init the mapper for this term starting with the original content (if exist)
                    term_params_mapper[dest_term] = list()
                    original_term = self.query_params.get(dest_term)
                    if original_term:
                        term_params_mapper[dest_term].append(original_term)
                # Append the required term to map for this destination term
                term_params_mapper[dest_term].append( self.query_params.get(mapping_param) + tag )
                self.logger.info('Mapping {{{}}} tagged term in \"{}\"'.
                                 format(term_params_mapper[dest_term][-1], dest_term) )
                pop_list.append( mapping_param )
        # Delete those terms already mapped in others
        for param in pop_list:
            self.query_params.pop( param )
        # Override or add the mapped terms
        for mapped_term in term_params_mapper:
            self.query_params[mapped_term] = ' AND '.join( term_params_mapper.get(mapped_term) )
        #self.logger.info("\nQuery_params: " + str(self.query_params) + "\n")
