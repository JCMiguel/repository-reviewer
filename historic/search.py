#!/usr/bin/python3
# -*- coding: utf8

from os import path
from historic.report import *
from datetime import datetime


class Search:

    RESULTS_BASE_FILENAME = 'results\\articles_table.csv'
    ID_Format = "%y%m%d%H%M%S"

    def __init__(self, search_params:dict):
        self._id = datetime.now().strftime( Search.ID_Format )
        self._report_data = None
        self._tags = []
        self._search_params = search_params
        self._fn = None


    def get_result_filename(self) -> str:
        """If filename has already been set, return it. If not, takes the base filename,
        insert the time id before the extension and check if the file exist to return it.
        Returns None if the file does not exist"""
        if self._fn:
            return self._fn
        fn = Search.RESULTS_BASE_FILENAME.split(sep='.')
        fn.insert( 1, "_"+ self._id +"." )
        fn = ''.join(fn)
        if path.isfile( fn ):
            self._fn = fn
        return self._fn


    def append_partial_res(self, results:Report):
        if (self._report_data is None):
            self._report_data = results
        else:
            self._report_data = self._report_data.merge_reports( results )


    def report(self) -> Report:
        return str(self._report_data)


    def tag(self, string_tag):
        self._tags.append(string_tag)


    def __repr__(self) -> str:
        representacion_interpretable = '{self.__class__.__name__}({self.__dict__})'.format(self=self)
        return representacion_interpretable


    def __str__(self) -> str:
        return '\n'.join( self.to_csv_lines(with_header=True) )


    def to_csv_lines(self, with_header:bool=False) -> list:
        line = self._id + Report.separator
        if self.report() is None: return ''
        head_with_data = str(self.report()).split(sep='\n')
        line += head_with_data[1] + Report.separator
        for tag in self._tags:
            line += " #"+ tag
        else: line += Report.separator
        line += str(self._search_params) + Report.separator

        result = []
        if with_header:
            header = 'ID' + Report.separator + head_with_data[0] + Report.separator
            header+= 'Tags' + Report.separator
            header+= 'Search Params' + Report.separator
            result.append( header[:-len(Report.separator)] )
        result.append( line[:-len(Report.separator)] )
        return result

    def to_dict_format(self, for_dataFrame:bool=False) -> dict:
        if self.report() is None:
            return ''
        di = dict()
        h_and_d = self.to_csv_lines(with_header=True)
        header_l = h_and_d[0].split(';')
        data_list = h_and_d[1].split(';')
        if for_dataFrame:
            for (title, value) in zip( header_l, data_list ):
                di[title] = [value]
        else:
            for (title, value) in zip( header_l, data_list ):
                di[title] = value
        return di
