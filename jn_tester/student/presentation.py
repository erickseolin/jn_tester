# -*- encoding: utf-8 -*-

from pandas import DataFrame
from IPython.display import display


class ViewPresenter:
    """Presentation class. It renders information about the results returned by tests."""

    def __init__(self, data, presentation_mode='text'):
        if type(data) is not dict:
            raise Exception("Presenter data must be a dictionary.")
        if presentation_mode not in ['text', 'table']:
            raise Exception("Valid formats for presenter are text / table.")
        self.__data = data
        self.__presentation_mode = presentation_mode

    def show(self):
        """Show the results in the choosen format, default is text."""
        if self.__presentation_mode is 'text':
            self.__show_results_in_text()
        else:
            self.__show_results_in_table()

    def __show_results_in_text(self):
        """Internal method to parse and show the results in text format."""
        print('\nShowing results:', self.__data.get('function'))
        print('-' * 20)
        print('Final score: ', self.__data.get('final_score'))
        size = len(self.__data.get('results'))
        if size > 0:
            for i in range(size):
                result = self.__data.get('results')[i]
                perf = self.__data.get('performance')[i]
                print(i + 1, ': ', result)
                print(' - time: ', perf.get('time'), ' ms')
                print(' - memory: ', perf.get('memory'), ' Mb')
        else:
            raise Exception("No results to visualize.")

    def __show_results_in_table(self):
        """Internal method to parse and show the results in table (pandas dataframe) format."""
        print('\nShowing results:', self.__data.get('function'))
        print('-' * 20)
        print('Final score: ', self.__data.get('final_score'))
        size = len(self.__data.get('results'))
        if size > 0:
            _data, _index, _columns = self.__prepare_data_to_dataframe()
            dt = DataFrame(data=_data, index=_index, columns=_columns)
            display(dt)
        else:
            raise Exception("No results to visualize.")

    def __prepare_data_to_dataframe(self):
        """Prepare the data to be displayed in a pandas DataFrame."""
        _data, _index, _columns = [], [], ['Score', 'Time', 'Memory']
        _dapp, _iapp = _data.append, _index.append
        size = len(self.__data.get('results'))
        if size > 0:
            for i in range(size):
                # fnc = self.__data.get('function')
                score = '{0}%'.format(round(self.__data.get('scores')[i] * 100))
                perf = self.__data.get('performance')[i]
                _iapp('Test {0}'.format(i+1))
                _dapp([
                    score,
                    '{0} ms'.format(perf.get('time')),
                    '{0} Mb'.format(perf.get('memory'))
                ])
        return _data, _index, _columns
