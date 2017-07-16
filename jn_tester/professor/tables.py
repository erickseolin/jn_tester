# -*- encoding: utf-8 -*-

from .presentation import Presenter


def view_complete_table(test_name, base_path='./', sort_by=None):
    """Gathers the results submited by all students and shows them in a table ranked by
    score and elapsed time.
    A result file is assumed to have the name '.TEST_NAME-STUDENT_ID.score'.
    This function will search for result files in all subdirectories of base_path.
    :param test_name: test's name
    :param base_path: base path glob for result files.
    :param sort_by: list containing columns to be sorted."""

    presenter = Presenter(test_name, base_path, sort_by)
    presenter.show()


def export_complete_table(test_name, base_path='./'):
    pass