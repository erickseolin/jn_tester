# -*- encoding: utf-8 -*-

import timeit
import functools
from memory_profiler import memory_usage
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

    def performance(self, function, runs=5):
        """
        Execute performance tests of time of execution and memory usage
        :param function: function to be evaluates
        :param runs: how many times the performance check should happen. default 5
        :return: dict that contains information about this execution
        """
        perf = {
            'time': 0.,
            'memory': 0.
        }

        if isinstance(self.input, dict):
            try:
                time_param = functools.partial(function, **self.input)
                mem_param = (function, (), self.input)
            except TypeError:
                _input = [val for _, val in self.input.items()]
                time_param = functools.partial(function, *_input)
                mem_param = (function, _input, {})
                warnings.warn("Function '{func_name}' have different arguments than those defined in "
                              "TestCase. Using them as *args."
                              .format(func_name=function.__name__),
                              stacklevel=4)
        else:
            time_param = functools.partial(function, self.input)
            mem_param = (function, (self.input,), {})

        # Convert to milliseconds
        perf['time'] = round(timeit.Timer(time_param).timeit(number=runs) * 1000, 8)
        perf['memory'] = round(memory_usage(proc=mem_param, max_usage=True)[0], 2)
        return perf


class TestSet(object):
    """TestSet."""

    def __init__(self, file_name=None, min_score=1.0):
        self.min_score = min_score
        self.test_cases = []

        if file_name:
            self.load(file_name)

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
        results = [test.evaluate(function) for test in self]
        return results

    def performance(self, function, runs=5):
        """
        Runs performance validation of the function in each TestCase for n times (default 5)
        :param function: function to be evaluates
        :param runs: how many times the performance check should happen. default 5
        :return: list containing dict with the values of execution. list[dict, dict...]
        """
        return [test.performance(function, runs) for test in self]

    def add_new_test_case(self, test_case):
        self.test_cases.append(test_case)

    def load(self, file_name):
        if '.' not in file_name:
            file_name += '.test'

        with open(file_name, 'rb') as file:
            self.test_cases = pickle.load(file)

    def save(self, file_name):
        if '.' not in file_name:
            file_name += '.test'

        with open(file_name, 'wb') as file:
            pickle.dump(self.test_cases, file)


class Results(object):

    def __init__(self, test_name, user_name=None, scores=None, times=None):
        self.test_name = test_name
        self.user_name = user_name
        self.scores = scores
        self.times = times

    def _generate_file_name(self, path):
        return '{path}/{name}.result'.format(path=path.strip('/'), name=self.test_name)

    def save(self, file_name=None, path='./'):
        if not file_name:
            file_name = self._generate_file_name(path)

        with open(file_name, 'wb') as file:
            pickle.dump({
                'test_name': self.test_name,
                'user': self.user_name,
                'score': self.scores,
                'time': self.times
            }, file)

    def load(self, file_name=None, path='./'):
        if not file_name:
            file_name = self._generate_file_name(path)

        with open(file_name, 'rb') as file:
            data = pickle.load(file)
            self.test_name = data['test_name']
            self.user_name = data['user']
            self.scores = data['score']
            self.times = data['time']