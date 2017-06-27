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


def submit_test(test_set_name, function):
    """"""
    test_set = TestSet()
    test_set.load(test_set_name)

    results = test_set.evaluate(function)
    score = sum(results) / float(len(results))

    for result in results:
        msg = '[{}/1.0]'.format(result)
        if result >= test_set.min_score:
            print(msg, ' OK')
        else:
            print(msg, ' FAIL')

    print("Final score: {:.2f}".format(score))
    if score >= test_set.min_score:
        print("Passed the test!")
    else:
        print("Failed the test!")


