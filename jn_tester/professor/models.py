# -*- encoding: utf-8 -*-

import timeit
import functools
from memory_profiler import memory_usage
import dill as pickle
from types import FunctionType
import warnings
import os


RESULTS_EXT = 'result'


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


def get_result_file_name(test_name, path='./'):
    return os.path.join(path, '{name}.{ext}'.format(name=test_name, ext=RESULTS_EXT))


class ResultScanner(object):

    def __getitem__(self, item):
        return self.result_sets[item]

    def __iter__(self):
        for results in self.result_sets:
            yield results

    def __init__(self, test_name):
        self.test_name = test_name
        self.result_sets = []

    def scan_dir(self, directory='./', clean_cache=True):
        if clean_cache:
            self.result_sets = []

        file_name = "{name}.{ext}".format(name=self.test_name, ext=RESULTS_EXT)
        for root, _, files in os.walk(directory):
            for file in files:
                if file == file_name:
                    self.result_sets.append(ResultSet(self.test_name, directory=root))
                    break   # no more files here

        return self.result_sets


class ResultSet(object):

    def __getitem__(self, item):
        return self.results[item]

    def __iter__(self):
        for result in self.results:
            yield result

    def __init__(self, test_name, directory='./'):
        self.test_name = test_name
        self.file_name = get_result_file_name(self.test_name, directory)
        self.results = []
        self.created = self.__load__()

    def add_result(self, user_name, function_name, scores, times, **kwargs):
        result = {'user': user_name,
                  'function': function_name,
                  'scores': scores,
                  'times': times,
                  }
        for key, value in kwargs.items():
            result[key] = value

        self.results.append(result)

    def save(self):
        with open(self.file_name, 'wb') as file:
            pickle.dump({
                'test_name': self.test_name,
                'results': self.results,
            }, file)

    def __load__(self):
        try:
            with open(self.file_name, 'rb') as file:
                data = pickle.load(file)
                self.test_name = data['test_name']
                self.results = data['results']
        except FileNotFoundError:
            return False
