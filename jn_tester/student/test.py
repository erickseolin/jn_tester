# -*- encoding: utf-8 -*-

from .models import Execution
from .presentation import Presenter


# In memory...
execution = Execution()


def run_test(test_set_name, fnc=None, presentation_mode='text'):
    """Execute a function in the TestCases that the TestSet has."""
    if not execution.loaded(test_set_name, fnc):
        execution.load(test_set_name, fnc)
    _data = execution.exec_test()
    # Present the data for the student
    presenter = Presenter(_data, presentation_mode=presentation_mode)
    presenter.show()


def submit_test(test_set_name, fnc=None, presentation_mode='text'):
    """Submit the results and show tables / text of results."""
    if not execution.loaded(test_set_name, fnc):
        execution.load(test_set_name, fnc)
    # Get the data
    _data = execution.submit_test()
    # Parse the path
    test_set_name = test_set_name.split('/')[-1]
    test_set_folder = test_set_name.split('/')[:-1]
    # Record the data
    execution.record_test_results(test_set_name, test_set_folder)
    # Present the data for the student
    presenter = Presenter(_data, presentation_mode=presentation_mode)
    presenter.show()
