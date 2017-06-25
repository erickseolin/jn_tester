import dill as pickle

# Assert types
ASSERT_EQUAL = 'equal'
ASSERT_CLOSE = 'close'

# Constants
EPSILON = 10**-6


class MalformedTestCase(Exception):
    def __init__(self, message):
        super(MalformedTestCase, self).__init__(message)


class TestCase(object):

    def __init__(self, _input, _output, assert_function=None, assert_type=None):
        self.input = _input
        self.output = _output

        if assert_type is None and assert_function is None:
            raise MalformedTestCase('assert_type or assert_function can not be both None.')

        if assert_type and not assert_type in [ASSERT_EQUAL, ASSERT_CLOSE]:
            raise MalformedTestCase('assert_type is not correctly defined.')

        self.assert_function = assert_function
        self.assert_type = assert_type

    def evaluate(self, function):
        if self.assert_function is not None:
            return self.assert_function(function(self.input), self.output)

        elif self.assert_type == ASSERT_EQUAL:
            return 1.0 if function(self.input) == self.output else 0.0

        elif self.assert_type == ASSERT_CLOSE:
            return 1.0 if function(self.input) - self.output < EPSILON else 0.0


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

