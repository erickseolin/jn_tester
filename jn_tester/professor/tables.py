# -*- encoding: utf-8 -*-

from jn_tester.professor.view import ExportPresenter
from jn_tester.professor.view import ViewPresenter


def view_complete_table(test_name, base_path='./', sort_by=None, presentation_format='table'):
    """Gathers the results submited by all students and shows them in a table ranked by
    score and elapsed time.
    This function will search for result files in all subdirectories of base_path.
    :param test_name: test's name
    :param base_path: base path glob for result files.
    :param sort_by: list containing columns to be sorted.
    :param presentation_format: string of format presentation: table | text.
    :param export_format: string of format to export: csv | text."""
    presenter = ViewPresenter(test_name, base_path, sort_by, presentation_format)
    presenter.show()


def export_complete_table(test_name, base_path='./', sort_by=None, export_format='csv'):
    """Export the values of results submited by all students and export the values to a file
    This function will search for result files in all subdirectories of base_path.
    :param test_name: test's name
    :param base_path: base path glob for result files.
    :param sort_by: list containing columns to be sorted.
    :param presentation_format: string of format presentation: table | text.
    :param export_format: string of format to export: csv | text."""
    presenter = ExportPresenter(test_name, base_path, sort_by, export_format=export_format)
    presenter.export()
