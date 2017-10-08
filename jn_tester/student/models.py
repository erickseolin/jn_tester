# -*- encoding: utf-8 -*-

import getpass
import os
import re
import warnings
from types import FunctionType

from jn_tester.professor.models import MalformedTestCase, ResultSet, load_test_set


class Execution:
    """Class model that keep in memory user test execution."""

    def __init__(self):
        self.__test_set_name = None
        self.__test_set = None
        self.__fnc = None
        self.__data = None

    def __load_username(self):
        """Loads the username that is executing the tests."""
        self.__username = getpass.getuser()
        # Bellow is a platform specific... please, comment the bellow line if need it
        _user_login = 'adessowiki'
        # The try bellow is a bug correction for jupyter notebooks
        try:
            _user_login = os.getlogin()
        except OSError as err:
            warnings.warn("OSError... {0}".format(err))
        # Let's get the user folder to see if its running inside his own folder
        # We are forcing this anyway... if os.getlogin gives error
        if _user_login == 'adessowiki':
            _user_folder = os.getcwd()
            _matched = re.match(r'.*(\/{0}\/).*'.format(self.__username), _user_folder)
            if not _matched:
                raise Exception('You can\'t submit function from another user')

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
        self.__test_set = load_test_set(test_set_name)

    def exec_test(self):
        """Execute the Test itself."""
        if len(self.__test_set.test_cases) > 0:
            return self.submit_test()
        else:
            raise Exception('No test cases to execute in this test.')

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
            raise Exception('No test cases to execute in this test.')

    def record_test_results(self, test_set_name):
        self.__load_username()
        scores = self.__data.get('scores')
        # We are not sending memory usage yet to the professor results.
        times = [perf['time'] for perf in self.__data.get('performance')]
        memory = [perf['memory'] for perf in self.__data.get('performance')]
        results = ResultSet(test_set_name)
        results.add_result(self.__username, self.__fnc.__name__, scores, times, memory=memory)
        results.save()
