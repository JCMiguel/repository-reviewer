#!/usr/bin/python3
# -*- coding: utf8

from historic.report import *

class Search:

    def __init__(self, search_params):
        self._id = "yymmddhhmmss"
        self._results = "???"
        self._search_params = search_params
        self._report_data = None


    def read_search_partial(self, results:Report):
        if (self._report is None):
            self._report_data = results
        else:
            self._report_data.merge_reports( results )


    def report(self) -> Report:
        return str(self._report_data)


    def tag(self, string_tag):
        raise NotImplemented("Debe agregar una etiqueta a este registro de busqueda")
