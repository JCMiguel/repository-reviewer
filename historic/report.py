#!/usr/bin/python3
# -*- coding: utf8
import logging


def to_year_fraction(date:str, round_to:int=2) -> float:
    if isinstance( date, str ) == False:
        return date
    # Parsing date string to compute months and days as fraction
    year_fraction = 0
    for idx, time in reversed(list(enumerate(date.split('-')))):
        year_fraction += int(time)
        if   idx == 2:  year_fraction /= 30
        elif idx == 1:  year_fraction /= 12
    return round( year_fraction, round_to )

def fraction_to_year(date:float) -> str:
    year = int(date)
    list_date = [str(year)]
    residual = round( date - year, 4 )
    if residual:
        residual *= 12
        months = int(residual)
        list_date.append( str(months) )
        residual = round( residual - months, 4 )
        if residual:
            days = int(residual * 30)
            if days > 0:
                list_date.append( str(days) )
    return "-".join(list_date)


def get_min_and_max(array) -> tuple:
    min = max = to_year_fraction( array[0] )
    for item in array:
        if type(item) is not int:
            item = to_year_fraction( item )
        if (min > item):
            min = item
        if (max < item):
            max = item
    return (min, max)

TIME_DIVISIONS = 3


class Report:

    separator = ';'
    __logger = logging.getLogger('root')

    def __init__(self, name, logger:logging.Logger=None):
        if logger is not None: Report.__logger = logger
        self._name = name
        self._occurrences = 0
        self._time_period = None
        self._time_div_cont = []
        self._time_div_perc = []


    def Import(report_items:dict, name=None):
        r = Report('imported_report')
        r.__dict__ = report_items
        if name: r._name = name
        return r


    def get_name_str(self) -> str:
        return self._name


    def process_dates(self, publication_dates, time_span:tuple=None):
        """Get an array of all article publication years to count the number of results and get time statistics.
        It is optional but important to inform the time span of the search period to get accuracy statistics."""
        self._occurrences = len(publication_dates)
        if self._occurrences == 0:
            # FIXME: Si las ocurrencias son cero, entonces nunca setea el time_span --> self._time_period
            Report.__logger.warning("No articles found: "+ str(publication_dates)+" on span:"+ str(time_span))
            self._time_div_cont = [0] * TIME_DIVISIONS
        else:
            if (time_span is None):
                time_span = get_min_and_max(publication_dates)
            self._time_period = ( to_year_fraction( time_span[0] ),
                                  to_year_fraction( time_span[1] ) )
            Report.__logger.debug("Reporting on years: "+ str(publication_dates)+" on span:"+ str(time_span))
            self._time_div_cont = self._process_dates_distribution(publication_dates, self._time_period)
        return self


    def calculate_percentages(self):
        occur = self._occurrences
        total = occur if type(occur) == int else occur[0]
        for cont in self._time_div_cont:
            self._time_div_perc.append( 0 if (total == 0) else (100*cont/total) )
        return self


    def merge_reports(self, other):
        compound = {}
        self.__logger.debug( "Merging reports:\n\t"+ str(self.__dict__) +"\n..with:\t" + str(other.__dict__) )
         # if the other is the same type (a simple one in this case)
        if type(other) is Report:
            # a simple merge can be performed
            for item in self.__dict__:
                # string items: appended on a list
                result = self._merge_when_anyone_null( other, item )
                if result:
                    compound[item] = result
                elif item == '_name':
                    compound[item] = self._merge_str(other, item)
                # numeric item like _ocurrences: first a totalizator, then individuals
                elif item == '_occurrences':
                    compound[item] = self._merge_int(other, item)
                # merge a list: add values by index
                elif item.startswith('_time'):
                    compound[item] = self._merge_list_or_tuple(other, item)
        else:
            # if not, the other class must know how to merge complex ones
            return other.merge_reports( self )
        return Compound_Report.Import( compound )





#   Representation methods

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self) -> str:
        return self._export_to_csv_header() + \
               self._export_to_csv_line()
    
    def at(self, item_name):
        return self.__dict__[item_name]


#   Private methods

    def _merge_when_anyone_null(self, other, item):
        result = None
        if self.at(item) is None:   # if own is None
            result = other.at(item) #       result = their
        if other.at(item) is None:  # if their is None
            result = self.at(item)  #       result = own
        return result


    def _merge_list_or_tuple(self, other, item):
        target = self.at(item)
        if isinstance( target, tuple):
            return self._merge_tuple( other, item )
        merging_list = []
        for idx in range(len(target)):
            merging_list.append( self.at(item)[idx] + other.at(item)[idx] )
        return merging_list


    def _merge_tuple(self, other, item):
        merging_tuple = ( min( self.at(item)[0], other.at(item)[0] ) ,
                          max( self.at(item)[1], other.at(item)[1] ) )
        return merging_tuple


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
        div_limits, div_counts = self._get_periods_arrays(span)
        # Distribute all the items in each division by making a recount.
        for y in years:
            y = to_year_fraction( y )
            for i in range(TIME_DIVISIONS):
                if y <= div_limits[i]:
                    div_counts[i] += 1
                    break
        Report.__logger.debug("On _process_dates_distribution, div_limits: "+ str(div_limits) )
        return div_counts


    def _export_to_csv_line(self) -> str:
        out_str = ending_str = ""
        for item in self.__dict__:
            value = self.at(item)

            if item == '_name':
                continue
            elif item == '_time_period':
                value = fraction_to_year(value[0]) +":"+ fraction_to_year(value[1])
            elif item == '_time_div_cont':
                ending_str = " ({:g}%)"
            elif item == '_time_div_perc':
                if len(value) == 0:
                    self.calculate_percentages()
                    value = self.at(item)
                out_str = out_str.format(*value)
                continue

            if type(value) is list:
                for element in value:
                    out_str += str(element) + ending_str + Report.separator
            else:
                out_str += str(value) + ending_str + Report.separator
            ending_str = ""
        return out_str[:-len(Report.separator)] + "\n"


    def _export_to_csv_header(self) -> str:
        out_str = ""
        for item in self.__dict__:
            if item == '_name':
                out_str += self.get_name_str() + Report.separator
            elif item in ['_occurrences', '_time_div_perc']:
                continue
            elif item == '_time_div_cont':
                for i in range(TIME_DIVISIONS):
                    out_str += 'DistT'+str(i) + Report.separator
            else:
                out_str += item[1:].replace('_',' ').title() + Report.separator
        return  out_str[:-len(Report.separator)] + "\n"


    def _get_periods_arrays(self, span:tuple):
        """This method divide the span N times and return the limits of each part
        and an array to count occurrences on those parts."""
        div_span = (span[1] - span[0]) / TIME_DIVISIONS
        limits = [span[0] + div_span]
        counts = [0]
        # Sets the upper limits of each time division.
        for i in range(1,TIME_DIVISIONS):
            limits.append( limits[-1] + div_span )
            counts.append( 0 )
        return limits, counts


class Compound_Report(Report):

    def Import(report_items:dict, name=None):
        r = Compound_Report('imported_report')
        r.__dict__ = report_items
        if name: r._name = name
        return r
    
    def get_name_str(self) -> str:
        out_str = ""
        for title in self._name:
            out_str += title + Report.separator
        return out_str[:-len( Report.separator )]

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
