#!/usr/bin/python3
# -*- coding: utf8

def get_min_and_max(array) -> tuple:
    min = max = array[0]
    for item in array:
        if (min > item):
            min = item
        if (max < item):
            max = item
    return (min, max)

TIME_DIVISIONS = 3


class Report:

    def __init__(self, name):
        self._name = name
        self._occurrences = 0 
        self._time_div_cont = []
        self._time_div_perc = []


    def Import(report_items:dict, name=None):
        r = Report('imported_report')
        r.__dict__ = report_items
        if name: r._name = name
        return r


    def process_dates(self, publication_dates, time_span:tuple=None):
        """Get an array of all article publication years to count the number of results and get time statistics.
        It is optional but important to inform the time span of the search period to get accuracy statistics."""
        if (time_span is None):
            time_span = get_min_and_max(publication_dates)
        self._occurrences = len(publication_dates)
        self._time_div_cont = self._process_dates_distribution(publication_dates, time_span)
        return self


    def calculate_percentages(self):
        occur = self._occurrences
        total = occur if type(occur) == int else occur[0]
        for cont in self._time_div_cont:
            self._time_div_perc.append( 100*cont/total )
        return self


    def merge_reports(self, other):
        compound = {}
         # if the other is the same type (a simple one in this case)
        if type(other) is Report:
            # a simple merge can be performed
            for item in self.__dict__:
                # string items: appended on a list
                if item == '_name':
                    compound[item] = self._merge_str(other, item)
                # numeric item like _ocurrences: first a totalizator, then individuals
                elif item == '_occurrences':
                    compound[item] = self._merge_int(other, item)
                # merge a list: add values by index
                elif item.startswith('_time_div'):
                    compound[item] = self._merge_list(other, item)
        else:
            # if not, the other class must know how to merge complex ones
            return other.merge_reports( self )
        return Compound_Report.Import( compound )


#   Representation methods

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__repl__())
    
    def at(self, item_name):
        return self.__dict__[item_name]


#   Private methods

    def _merge_list(self, other, item):
        merging_list = []
        for idx in range(len(self.at(item))):
            merging_list.append( self.at(item)[idx] + other.at(item)[idx] )
        return merging_list
    

    def _merge_str(self, other, item):
        merging_names = ['Total']
        merging_names.append( self.at(item) )
        merging_names.append( other.at(item) )
        return merging_names


    def _merge_int(self, other, item):
        merging_ocurr = []
        merging_ocurr.append( self.at(item) + other.at(item) )
        merging_ocurr.append( self.at(item) )
        merging_ocurr.append( other.at(item) )
        return merging_ocurr


    def _process_dates_distribution(self, years, span:tuple):
        div_span = (span[1] - span[0]) / TIME_DIVISIONS
        div_limits = [span[0] + div_span]
        div_counts = [0]
        # Establece los limites superiores de cada division de tiempo
        for i in range(1,TIME_DIVISIONS):
            div_limits.append( div_limits[-1] + div_span )
            div_counts.append( 0 )
        # Reparte todos los articulos en cada division haciendo un recuento
        for y in years:
            for i in range(TIME_DIVISIONS):
                if y < div_limits[i]:
                    div_counts[i] += 1
                    break
        return div_counts



class Compound_Report(Report):

    def Import(report_items:dict, name=None):
        r = Compound_Report('imported_report')
        r.__dict__ = report_items
        if name: r._name = name
        return r
    
    def _merge_str(self, other:Report, item):
        merge_names = self.at(item).copy()
        merge_names.append( other.at(item) )
        return merge_names

    def _merge_int(self, other:Report, item):
        merging_ocurr = []
        merging_ocurr.append( self.at(item)[0] + other.at(item) )
        for value in self.at(item)[1:]:
            merging_ocurr.append( value )            
        merging_ocurr.append( other.at(item) )
        return merging_ocurr
