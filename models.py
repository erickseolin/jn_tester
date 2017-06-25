ASSERT_EQUAL = 'equal'
ASSERT_SIMILAR = 'similar'

class MalformedTestCase(Exception):
    def __init__(self, message):
        super(MalformedTestCase, self).__init__(message)


class TestCase(object):

    def __init__(self, _input, _output, assert_function=None, assert_type=None):
        self.input = _input
        self.output = _output

        if assert_type is None and assert_function is None:
            raise MalformedTestCase('assert_type or assert_function can not be both None')

        if assert_function is not None:
            self.assert_function = assert_function
        else:
            self.assert_type = assert_type

    def evaluate(self, function):
        pass


class TestSet(object):

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

    def load(self, file):
        pass

    def save(self, file):
        pass

