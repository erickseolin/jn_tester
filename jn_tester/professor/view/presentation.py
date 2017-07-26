# -*- encoding: utf-8 -*-


from IPython.display import display
from .common import CommonPresenter


class ViewPresenter(CommonPresenter):
    """Presentation class. It renders information about the results returned by tests."""

    def __init__(self, test_name, base_path='./', sort_by=None, presentation_format='table'):
        super().__init__(test_name, base_path, sort_by)
        if presentation_format not in ['text', 'table']:
            raise Exception("Valid formats for presenter are text / table.")
        self.__presentation_format = presentation_format

    def show(self):
        """Show the results in the choosen format, default is text."""
        if self.__presentation_format is 'table':
            self.__show_results_in_table()
        else:
            self.__show_results_in_text()

    def __show_results_in_text(self):
        """Show results in a text format."""
        # TODO: Implement...
        pass

    def __show_results_in_table(self):
        """Show results in pandas DataFrame format."""
        df = super(ViewPresenter, self)._prepare_dataframe()
        if df is not None:
            display(df)
