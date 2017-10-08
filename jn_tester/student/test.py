# -*- encoding: utf-8 -*-

from .models import Execution
from .presentation import ViewPresenter


# In memory...
execution = Execution()


def run_test(test_set_name, fnc=None, presentation_format='table'):
    """"""
    if execution.already_loaded(test_set_name, fnc):
        execution.load(test_set_name, fnc)
    # Get the data
    _data = execution.exec_test()
    # Present the data for the student
    presenter = ViewPresenter(_data, presentation_mode=presentation_format)
    presenter.show()
    return _data


def submit_test(test_set_name, fnc=None, presentation_format='table'):
    """"""
    if execution.already_loaded(test_set_name, fnc):
        execution.load(test_set_name, fnc)
    # Get the data
    _data = execution.submit_test()
    # Record the data
    execution.record_test_results(test_set_name)
    # Present the data for the student
    presenter = ViewPresenter(_data, presentation_mode=presentation_format)
    presenter.show()
