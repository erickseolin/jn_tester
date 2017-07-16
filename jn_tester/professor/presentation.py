# -*- encoding: utf-8 -*-

import glob
import os
import warnings
from itertools import chain
from IPython.display import display
import pandas as pd
from enum import Enum
from .models import ResultScanner


class Sorting(Enum):
    """Util class, to choose what type of sorting should be used."""
    ASCENDING = True
    DESCENDING = False


class Presenter:
    """Presentation class. It renders information about the results returned by tests."""

    def __init__(self, test_name, base_path='./', sort_by=None, presentation_format='table'):
        if presentation_format not in ['text', 'table']:
            raise Exception("Valid formats for presenter are text / table.")
        self.__test_name = test_name
        self.__base_path = base_path
        self.__presentation_format = presentation_format
        self.__create_sort_by(sort_by)

    def show(self):
        """Show the results in the choosen format, default is text."""
        if self.__presentation_format is 'text':
            self.__show_results_in_text()
        else:
            self.__show_results_in_table()

    def __show_results_in_text(self):
        """"""
        # TODO: Implement...
        pass

    def __show_results_in_table(self):
        """"""
        _data, _columns = self.__prepare_data_to_dataframe(ResultScanner(self.__test_name).scan_dir(self.__base_path))
        if _data:
            df = pd.DataFrame(data=_data, columns=_columns)
            if self.__sort_by and self.__ascending_by:
                df.sort_values(by=self.__sort_by, ascending=self.__ascending_by, inplace=True)
            display(df)
        else:
            raise Exception("No results to visualize.")

    def __create_sort_by(self, sort_by):
        if sort_by:
            if type(sort_by) is not list:
                raise Exception("Sorting parameter should be a list.")
            _sort, self.__ascending_by = zip(*(self.__unpack_sort(sort_m) for sort_m in sort_by))
            if len(_sort) != len(self.__ascending_by):
                raise Exception("Sorting values and ordering must have the same size.")
            self.__sort_by = []
            if 'rank' in _sort:
                self.__sort_by.append('Function Ranking')
            if 'author' in _sort:
                self.__sort_by.append('Author')
            if 'time' in _sort:
                self.__sort_by.append('Mean Time (ms)')
            if 'final_score' in _sort:
                self.__sort_by.append('Final Score')
        else:
            self.__sort_by = ['Mean Time (ms)']
            self.__ascending_by = [Sorting.ASCENDING]

    def __unpack_sort(self, sort):
        """Simple way to unpack the sort values."""
        return sort[0], sort[1]

    def __prepare_data_to_dataframe(self, data):
        """Prepare the data to be displayed in a pandas DataFrame."""
        results = []
        rappend = results.append  # faster way to add items to a list
        for result_set in data:
            for res in result_set:
                res['final_score'] = sum(res['scores']) / float(len(res['scores']))
                res['mean_time'] = sum(res['times']) / float(len(res['times']))
                rappend(res)
        if results:
            # Sorts by descending final score and then ascending by mean execution time
            results = sorted(results, reverse=True, key=lambda re: (re['final_score'], -re['mean_time']))

            # Transform into list with order: ranking, funcname, user, Test[i] Score, Test[i] Time, Mean Time, Final score
            ## Generate column headers:
            columns_headers = ['Function Ranking', 'Function', 'Author', 'Mean Time (ms)', 'Final Score']
            N = len(results[0]['scores']) + 1
            test_headers = list(
                chain.from_iterable(('Test {}: Score'.format(i), 'Test {}: Time (ms)'.format(i)) for i in range(1, N)))
            columns_headers[3:3] = test_headers

            ## Transform the data
            results_list = []
            rlappend = results_list.append  # faster way to add items to a list
            for rank, r in enumerate(results):
                rlist = list([rank + 1, r['function'], r['user'], '{0:.2f}'.format(r['mean_time']),
                              '{0:.2f}'.format(r['final_score'])])
                tests_score_time = list(chain.from_iterable(
                    ('{0:.2f}'.format(r['scores'][i]), '{0:.2f}'.format(r['times'][i])) for i in
                    range(len(r['scores']))))
                rlist[3:3] = tests_score_time
                rlappend(rlist)
            return results_list, columns_headers
        return None
