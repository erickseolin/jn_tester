# -*- encoding: utf-8 -*-

from types import FunctionType
from models import TestSet, MalformedTestCase


def run_test(test_name='main_test', fnc=None):
    """"""
    if type(fnc) is not FunctionType:
        raise MalformedTestCase('assert_function must be of FunctionType.')
    if not test_name.endswith('.test'):
        test_name = '{}.test'.format(test_name)
    test = TestSet()
    test.load(test_name)
    return test.evaluate(fnc)


def submit_test():
    """"""
    pass
