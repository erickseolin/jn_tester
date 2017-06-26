# -*- encoding: utf-8 -*-


class Execution:
    """Class model that keep in memory user test execution."""

    def __init__(self):
        self.__testSet = None
        self.__fnc = None

    def already_loaded(self):
        return False if self.__testSet is None else True

    def reload_params(self, testSet, fnc):
        if self.__testSet is None and self.__fnc is None:
            self.__testSet = testSet
            self.__fnc = fnc

    def exec_test(self):
        if len(self.__testSet.test_cases) > 0:
            return self.__testSet.evaluate(self.__fnc)
        else:
            raise Exception('Not test cases to execute in this test.')


