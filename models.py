# -*- encoding: utf-8 -*-

import dill as pickle
from types import FunctionType
import warnings


class MalformedTestCase(Exception):
    def __init__(self, message):
        super(MalformedTestCase, self).__init__(message)


class TestCase(object):
    """TestCase."""

    def __init__(self, _input, _output, assert_function):
        self.input = _input
        self.output = _output

        if type(assert_function) is not FunctionType:
            raise MalformedTestCase('assert_function must be of FunctionType.')

        self.assert_function = assert_function

    def evaluate(self, function):
        if isinstance(self.input, dict):
            try:
                evaluation = self.assert_function(function(**self.input), self.output)
            except TypeError:
                _input = [val for _, val in self.input.items()]
                evaluation = self.assert_function(function(*_input), self.output)
                warnings.warn("Function '{func_name}' have different arguments than those defined in "
                              "TestCase. Using them as *args."
                              .format(func_name=function.__name__),
                              stacklevel=4)
        else:
            evaluation = self.assert_function(function(self.input), self.output)

        return evaluation


class TestSet(object):
    """TestSet."""

    def __init__(self):
        self.test_cases = []

    def __getitem__(self, item):
        return self.test_cases[item]

    def __iter__(self):
        for test in self.test_cases:
            yield test

    def evaluate(self, function):
        """
        Evaluates function using all test cases in the test set
        :param function: function to be evaluates
        :return: list with the evaluated results for each test case
        """
        return [test.evaluate(function) for test in self]

    def add_new_test_case(self, test_case):
        self.test_cases.append(test_case)

    def load(self, file_name):
        if not file_name.endswith('.test'):
            warnings.warn('TestSet.load error: file must be .test file format.')
        try:
            with open(file_name, 'rb') as file:
                self.test_cases = pickle.load(file)
        except Exception as err:
            cls_err = err.__class__.__name__
            warnings.warn('TestSet.load {0} error: {1}'.format(cls_err, err))

    def save(self, file_name):
        if not file_name.endswith('.test'):
            warnings.warn('TestSet.save error: file must be .test file format.')
        try:
            with open(file_name, 'wb') as file:
                pickle.dump(self.test_cases, file)
        except Exception as err:
            cls_err = err.__class__.__name__
            warnings.warn('TestSet.save {0} error: {1}'.format(cls_err, err))
