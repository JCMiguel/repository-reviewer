#!/usr/bin/python3
# -*- coding: utf8
import traceback
import pandas as pd
from os import path
from historic.search import *

class History:

    GLOBAL_RESULTS_FILENAME = 'results\\history.csv'
    __df = None

    def Data( force_loading:bool=False ) -> pd.DataFrame:
        if (History.__df is None) or force_loading:
            History.__df = History.__load_dataframe()
        return History.__df


    def Add(search : DataSearch):
        df_list = [ pd.DataFrame( search.to_dict_format(True) ).set_index('ID') ]
        try:    df_list.append( History.Data() )
        except: pass
        df = pd.concat( df_list )
        try:# to compute the sum of occurreces in each repo after receiving the last
            reorder = False
            cols = df.columns.to_list()
            if 'Total' not in cols:
                cols.insert( 0, 'Total' )
                reorder = True
            adding_df = df[ cols[ 1 : cols.index('Time Period') ] ]
            df['Total'] = adding_df.fillna( 0 ).astype( int ).sum( axis=1 ).astype( int )
            if reorder: df = df.loc[ :, cols ]
        except: pass
        df.to_csv( History.GLOBAL_RESULTS_FILENAME, sep=Report.separator, encoding='utf-8')


    def Get(value=0):
        """This is a common function to call the specific overload one.
        It calls the choosen one by the atribute type or value."""
        if isinstance(value, list):     return History.Get_by_filter( value )
        elif isinstance(value, str):    return History.Get_by_matching( value )
        elif isinstance(value, int):
            if value > 1000:            return History.Get_by_id( value )
            elif value < 0:             return History.Get_by_index( value )
            else:                       return History.Get_previous( value )

    def Get_by_id(id:int) -> pd.Series:
        """This method expects the complete ID of the history record. Format: yymmddHHMMSS
        """
        if not isinstance(id, int):
            raise TypeError('id parameter in Get_by_id must be int type')
        return History.Data().loc[ id ]

    def Get_by_filter(filter:list) -> pd.DataFrame:
        return History.Data()[ filter ]

    def Get_previous(index:int=0) -> pd.Series:
        """Return the historic register that was searched `index` times ago.
        The value of `index` must be greater or equal to 0, lower than 1000"""
        if not isinstance(id, int):
            raise TypeError('index parameter in Get_previous must be int type')
        if index < 0: raise ValueError(
            'The value of `index` must be greater or equal to 0, lower than 1000')
        return History.Data().iloc[ index ]

    def Get_by_index(index:int) -> pd.Series:
        """Return the historic register with the index counting from the beginning.
        The value of `index` must be negative."""
        if not isinstance(id, int):
            raise TypeError('index parameter in Get_by_index must be int type')
        if index >= 0:
            raise ValueError('The value of `index` must be negative')
        return History.Data().iloc[ index ]

    def Get_by_matching(match:str, field_names:list=[]) -> pd.Series:
        """Return the historic register whose fields match with the given argument
        If `field_names` argument is passed it only search on that field/s. If not, the search
        secuence will start by "Tags" and "Search Params" fields, and then others"""
        df = History.Data()
        matching_rows = [False] * df.index.size
        explicit_search = True
        if len(field_names) == 0:
            explicit_search = False
            field_names = ['Tags','Search Params']
        # It first search on the selected field names
        for field in field_names:
            searching_series:pd.Series = df[ field ]
            matching_rows |= searching_series.str.contains( match ).values
        if (True in matching_rows) or (explicit_search == True):
            return History.Get_by_filter( matching_rows )
        # If not match yet, then search on the others fields starting backwards
        for field in reversed( df.columns.drop(field_names) ):
            searching_series:pd.Series = df[ field ]
            try: matching_rows = searching_series.str.contains( match ).values
            except: pass
            if (True in matching_rows):
                break
        return History.Get_by_filter( matching_rows )


    def Filter_date( d_from:str=None, d_to:str=None) -> list:
        df = History.Data()
        filter = [True] * df.index.size
        id_len = len( DataSearch.ID_Format )
        # Verify dates input are not formated
        if d_from:
            filter &= df.index > int( d_from.ljust(id_len,'0') )
        if d_to:
            filter &= df.index < int( d_to.ljust(id_len,'0') )
        return filter


    def Get_by_date(date_range:str, sep=',') -> pd.DataFrame:
        """ Receive a string parameter representing the date period to search in.
        If end date is specified, values must be separated by `sep`
        """
        if not isinstance(date_range, str):
            raise TypeError('date_range parameter in Get_by_date must be str type')
        dates = date_range.split( sep )
        filter = History.Filter_date( *dates  )
        return History.Data()[ filter ]


    def __load_dataframe() -> pd.DataFrame:
        df = pd.read_csv( History.GLOBAL_RESULTS_FILENAME, sep=Report.separator, index_col='ID')
        df = df.fillna('')
        return df

