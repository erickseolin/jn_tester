import dill as pickle
from types import FunctionType


class MalformedTestCase(Exception):
    def __init__(self, message):
        super(MalformedTestCase, self).__init__(message)


class TestCase(object):

    def __init__(self, _input, _output, assert_function):
        self.input = _input
        self.output = _output

        if type(assert_function) is not FunctionType:
            raise MalformedTestCase('assert_function must be of FunctionType.')

        self.assert_function = assert_function

    def evaluate(self, function):
        return self.assert_function(function(self.input), self.output)


class TestSet(object):
    test_cases = []

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
        with open(file_name, 'rb') as file:
            self.test_cases = pickle.load(file)

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.test_cases, file)

