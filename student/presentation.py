# -*- encoding: utf-8 -*-

from pandas import DataFrame


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
        size = len(self.__data.get('results'))
        if size > 0:
            for i in range(size):
                result = self.__data.get('performance')[i]
                perf = self.__data.get('performance')[i]
                print(i + 1, ': ', result)
                print(' - time: ', perf.get('time'), ' ms')
                print(' - memory: ', perf.get('memory'), ' Mb')
        else:
            raise Exception("No results to visualize.")

    def __show_results_in_table(self):
        """Internal method to parse and show the results in table (pandas dataframe) format."""
        print('\nShowing results:')
        print('-' * 20)
        print('Final score: ', self.__data.get('final_score'))
        _data, _index = self.__prepare_data_to_dataframe()
        dt = DataFrame(data=_data, index=_index)

    def __prepare_data_to_dataframe(self):
        _data = {}
        _index = {}
        size = len(self.__data.get('results'))
        if size > 0:
            for i in range(size):
                # TODO: Organize the data
                # _data['Test{0}'.format(i)]
                results = self.__data.get('performance')[i]
                perf = self.__data.get('performance')[i]
        return _data, _index
