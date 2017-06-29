# -*- encoding: utf-8 -*-
import sys
sys.path.append('..')

from jn_tester.student.test import submit_test
from jn_tester.professor.models import TestCase, TestSet
from jn_tester.student.models import Execution


def equal(x, y):
    return 1.0 if x == y else 0.0


def double(n):
    return 2*n


def problematic_function(n):
    raise Exception('Error...')
    return 2*n


def problematic_function_2(n):
    # Raises exception sometimes
    if n == 2:
        raise Exception('Error...')
    return 2*n


def test_case_tests():
    print("starting to test TestCase...")

    # test with lambda functions
    t = TestCase(2, 4, lambda x, y: 1.0 if x == y else 0.0)
    assert t.evaluate(lambda x: 2*x) == 1.0

    # test with normal functions
    t = TestCase(2, 4, equal)
    assert t.evaluate(double) == 1.0

    # test with lists
    _input = [1, 2, 3]
    _output = [1, 2, 3, 1, 2, 3]
    t = TestCase(_input, _output, equal)
    assert t.evaluate(double) == 1.0

    # test false
    t = TestCase(2, 5, equal)
    assert t.evaluate(double) == 0.0

    # test performance
    perform = t.performance(double)
    assert isinstance(perform, dict)
    assert perform.get('memory', None) is not None
    assert perform.get('time', None) is not None

    # test multiple input
    t = TestCase({'x': 6, 'y': 5}, 11, assert_function=equal)
    assert t.evaluate(lambda x, y: x+y) == 1.0
    assert t.evaluate(lambda x, y: 3) == 0.0
    assert t.evaluate(lambda x, y: x*y) == 0.0
    assert t.evaluate(lambda x, y: 0.0) == 0.0


def test_set_tests():
    print("starting to test TestSet...")

    test = TestSet()
    test.add_new_test_case(TestCase(2, 4, lambda x, y: 1.0 if x == y else 0.0))
    test.add_new_test_case(TestCase({'n': 6}, 12, equal))
    test.add_new_test_case(TestCase({'n': 4}, 8, equal))

    assert test.evaluate(lambda n: 2**n) == [1.0, 0.0, 0.0]       # wrong
    assert test.evaluate(double) == [1.0, 1.0, 1.0]
    assert test.evaluate(lambda n: n**2) == [1.0, 0.0, 0.0]    # wrong
    assert test.evaluate(lambda n: 3) == [0.0, 0.0, 0.0]    # wrong
    
    # test save and load
    test.save('temp.test')
    test.load('temp.test')

    assert test.evaluate(lambda n: 2**n) == [1.0, 0.0, 0.0]       # wrong
    assert test.evaluate(double) == [1.0, 1.0, 1.0]
    assert test.evaluate(lambda n: n**2) == [1.0, 0.0, 0.0]    # wrong
    assert test.evaluate(lambda n: 3) == [0.0, 0.0, 0.0]    # wrong

    # save anoter test
    test = TestSet()
    test.add_new_test_case(TestCase(2, 6, equal))
    test.add_new_test_case(TestCase({'n': 6}, 18, equal))

    assert test.evaluate(lambda n: 3*n) == [1.0, 1.0]
    assert test.evaluate(lambda n: 4*n) == [0.0, 0.0]

    test.save('temp2')

    # test load previous
    test = TestSet('temp.test')
    assert test.evaluate(lambda n: 2**n) == [1.0, 0.0, 0.0]       # wrong
    assert test.evaluate(double) == [1.0, 1.0, 1.0]
    assert test.evaluate(lambda n: n**2) == [1.0, 0.0, 0.0]    # wrong
    assert test.evaluate(lambda n: 3) == [0.0, 0.0, 0.0]    # wrong

    # test load back
    test = TestSet('temp2.test')
    assert test.evaluate(lambda n: 3*n) == [1.0, 1.0]
    assert test.evaluate(lambda n: 4*n) == [0.0, 0.0]
    
    
def execution_tests():
    print('Starting Execution tests...')
    
    # Testing the behavior of exceptions
    exec = Execution()
    exec.load('temp.test', problematic_function)
    exception_raised = False
    try:
        # Exceptions should be raised in exec_test
        exec.exec_test()
    except:
        exception_raised = True
    assert exception_raised == True
    
    # Scores should be all zero
    results = exec.submit_test()
    assert results['scores'] == [0.0, 0.0, 0.0]
    for perf in results['performance']:
        assert perf == {'time': 0.0, 'memory': 0.0}
        
        
    exec = Execution()
    exec.load('temp.test', problematic_function_2)
    exception_raised = False
    try:
        # Exceptions should be raised in exec_test
        exec.exec_test()
    except:
        exception_raised = True
    assert exception_raised == True
    
    # Scores should be all zero
    results = exec.submit_test()
    assert results['scores'] == [0.0, 1.0, 1.0]
    assert results['performance'][0] == {'time': 0.0, 'memory': 0.0}
    assert results['performance'][1] != {'time': 0.0, 'memory': 0.0}
    assert results['performance'][2] != {'time': 0.0, 'memory': 0.0}


if __name__ == '__main__':
    try:
        test_case_tests()
        print("-- TestCase testes passed! --\n")
        test_set_tests()
        print("-- TestSet testes passed! --\n")
        execution_tests()
        print('-- Execution tests passed! --\n')
        
    except AssertionError:
        print("Error ocurred!")

    """
    submit_test('teste3', 'rdenadai', lambda x, y: x*y)
    print()

    submit_test('teste3', 'rdenadai', lambda x, y: x+y)
    """
