# -*- encoding: utf-8 -*-

from pandas import DataFrame as dt


class Presenter:
    """Presentation class. It renders information about the results returned by tests."""

    def __init__(self, data, presentation_format='text'):
        if type(data) is not dict:
            raise Exception("Presenter data must be a dictionary.")
        if presentation_format not in ['text', 'table']:
            raise Exception("Valid formats for presenter are text / table.")
        self.__data = data
        self.__presentation_format = presentation_format

    def show(self):
        """Show the results in the choosen format, default is text."""
        if self.__presentation_format is 'text':
            self.__show_results_in_text()
        else:
            self.__show_results_in_table()

    def __show_results_in_text(self):
        """Internal method to parse and show the results in text format."""
        print('\nShowing results:')
        print('-' * 20)
        print('Final score: ', self.__data.get('final_score'))
        for i, result in enumerate(self.__data.get('results')):
            print(i+1, ': ', result)
            perf = self.__data.get('performance')
            print(' - time: ', perf[i].get('time'), ' ms')
            print(' - memory: ', perf[i].get('memory'), ' Mb')

    def __show_results_in_table(self):
        """Internal method to parse and show the results in table (pandas dataframe) format."""
        print('\nShowing results:')
        print('-' * 20)
        print('Final score: ', self.__data.get('final_score'))
        # TODO: show results in pandas DataFrame
