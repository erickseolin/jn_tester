# -*- encoding: utf-8 -*-

from types import FunctionType
from .models import Execution
from models import TestSet, MalformedTestCase

# In memory...
execution = Execution()


def run_test(test_name='main_test', fnc=None):
    """"""
    if type(fnc) is not FunctionType:
        raise MalformedTestCase('assert_function must be of FunctionType.')

    test = None
    if not execution.already_loaded():
        test = TestSet()
        test.load(test_name)
    execution.reload_params(test, fnc)
    return execution.exec_test()


def submit_test():
    """"""
    pass
