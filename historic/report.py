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

    def __init__(self):
        pass 
                 
                 
    def process_dates(self, publication_dates):
        time_span = get_min_and_max(publication_dates)
        self._occurrences = len(publication_dates)
        self._time_div_cont = self._process_dates_distribution(publication_dates, time_span)

 
    def calculate_percentages(self):
        self._time_div_perc = []
        for cont in self._time_div_cont:
            self._time_div_perc.append( 100*cont/self._occurrences )


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
