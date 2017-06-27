# -*- encoding: utf-8 -*-


from .models import Execution
from .presentation import Presenter
from models import Results

# In memory...
execution = Execution()


def run_test(test_set_name, fnc=None):
    """"""
    if execution.already_loaded(test_set_name):
        execution.load(test_set_name, fnc)
    return execution.exec_test()


def submit_test(test_set_name, username, fnc=None, presentation_format='text'):
    """"""
    if execution.already_loaded(test_set_name):
        execution.load(test_set_name, fnc)
    _data = execution.submit_test()

    results = Results(test_set_name, username)
    results.save('.{0}-{1}.score'.format(test_set_name, username))

    presenter = Presenter(_data, presentation_format=presentation_format)
    presenter.show()
