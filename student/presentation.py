# -*- encoding: utf-8 -*-


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
        if self.__presentation_format is 'text':
            self.__show_results_in_text()
        else:
            self.__show_results_in_table()

    def __show_results_in_text(self):
        print('\nShowing results:')
        print('-' * 20)
        print('Final score: ', self.__data.get('final_score'))
        for i, result in enumerate(self.__data.get('results')):
            print(i+1, ': ', result)

    def __show_results_in_table(self):
        pass