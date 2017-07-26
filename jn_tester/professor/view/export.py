# -*- encoding: utf-8 -*-


from .common import CommonPresenter


class ExportPresenter(CommonPresenter):

    def __init__(self, test_name, base_path='./', sort_by=None, export_format='csv'):
        super().__init__(test_name, base_path, sort_by)
        self.__export_format = export_format

    def export(self):
        """Export the values to a csv (default) or other format."""
        df = super(ExportPresenter, self)._prepare_dataframe()
        if df is not None:
            filename = '{0}/{1}-export'.format(self._base_path, self._test_name)
            if self.__export_format is 'html':
                filename = '{0}.html'.format(filename)
                df.to_html(filename)
            elif self.__export_format in ['pkl', 'pickle']:
                filename = '{0}.pkl'.format(filename)
                df.to_pickle(filename)
            else:
                filename = '{0}.csv'.format(filename)
                df.to_csv(filename, sep=';', encoding='utf-8')
        else:
            print("Not data could be export... please visualize the DataFrame to see if results are ok.")

