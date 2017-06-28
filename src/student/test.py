# -*- encoding: utf-8 -*-

from .models import Execution
from .presentation import Presenter
import os
import getpass
current_user_cod = getpass.getuser()
#user_all_name = pwd.getpwnam(user_cod[0])[4]

# In memory...
execution = Execution()


def run_test(test_set_name, fnc=None):
    """"""
    if execution.already_loaded(test_set_name, fnc):
        execution.load(test_set_name, fnc)
    return execution.exec_test()


def submit_test(test_set_name, fnc=None, presentation_format='text'):
    """"""
    local_cod =''
    if os.getlogin()=='adessowiki':
        local_cod = str(os.getcwd()).split('/')[0]
    else:
        local_cod = current_user_cod
 
    if local_cod == current_user_cod:
        username = current_user_cod
        pass
    else:
        print('You can\'t submit function from another user')
        return
                  
    if execution.already_loaded(test_set_name, fnc):
        execution.load(test_set_name, fnc)
    # Get the data
    _data = execution.submit_test()
    # Record the data
    execution.record_test_results(test_set_name)
    # Present the data for the student
    presenter = Presenter(_data, presentation_format=presentation_format)
    presenter.show()
