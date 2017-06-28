# -*- encoding: utf-8 -*-

from types import FunctionType
from models import TestSet, MalformedTestCase, Results


class Execution:
    """Class model that keep in memory user test execution."""

    def __init__(self):
        self.__test_set_name = None
        self.__test_set = None
        self.__fnc = None
        self.__data = None

    def __check_load_test_set(self, test_set_name):
        """Checking if TestSet file name is not the same as before."""
        return test_set_name != self.__test_set_name

    def already_loaded(self, test_set_name, fnc):
        """Verify if the TestSet is already loaded."""
        return \
            self.__test_set is None or \
            self.__check_load_test_set(test_set_name) or \
            self.__fnc != fnc

    def load(self, test_set_name, fnc):
        """Load the TestSet and keep in memory constraints."""
        if type(fnc) is not FunctionType:
            raise MalformedTestCase('assert_function must be of FunctionType.')

        self.__test_set_name = test_set_name
        self.__fnc = fnc
        self.__test_set = TestSet()
        self.__test_set.load(test_set_name)

    def exec_test(self):
        """Execute the Test itself."""
        if len(self.__test_set.test_cases) > 0:
            return {
                'results': self.__test_set.evaluate(self.__fnc),
                'performance': self.__test_set.performance(self.__fnc)
            }
        else:
            raise Exception('Not test cases to execute in this test.')

    def submit_test(self):
        """Execute the Test and return the results."""
        if len(self.__test_set.test_cases) > 0:
            results = self.__test_set.evaluate(self.__fnc)
            score = sum(results) / float(len(results))

            _data = {
                'success': False,
                'function': self.__fnc.__name__,
                'final_score': 0.,
                'results': [],
                'scores': [],
                'performance': []
            }

            for result in results:
                msg = 'FAIL'
                if result >= self.__test_set.min_score:
                    msg = 'OK'
                _data['results'].append('[{0}/1.0] => {1}'.format(result, msg))
                _data['scores'].append(result)

            _data['final_score'] = "{0}%".format(round(score * 100))
            if score >= self.__test_set.min_score:
                _data['success'] = True

            # Let's execute performance tests!
            performance = self.__test_set.performance(self.__fnc)
            for perf in performance:
                _data['performance'].append(perf)

            self.__data = _data
            return _data
        else:
            raise Exception('Not test cases to execute in this test.')

    def record_test_results(self, test_set_name, username):
        scores = self.__data.get('scores')
        times = self.__data.get('performance')
        results = Results(test_set_name, username, scores=scores, times=times)
        results.save('.{0}-{1}.score'.format(test_set_name, username))
