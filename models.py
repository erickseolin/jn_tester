# -*- encoding: utf-8 -*-

import timeit
import functools
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
                # timeit.Timer(functools.partial(function, **self.input)).timeit(number=3)
                evaluation = self.assert_function(function(**self.input), self.output)
            except TypeError:
                _input = [val for _, val in self.input.items()]
                # timeit.Timer(functools.partial(func, *input)).timeit(number=3)
                evaluation = self.assert_function(function(*_input), self.output)
                warnings.warn("Function '{func_name}' have different arguments than those defined in "
                              "TestCase. Using them as *args."
                              .format(func_name=function.__name__),
                              stacklevel=4)
        else:
            # timeit.Timer(functools.partial(function, self.input)).timeit(number=3)
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
        with open(file_name, 'rb') as file:
            self.test_cases = pickle.load(file)

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.test_cases, file)
            
import pickle as pkl

class model(dict):
    def __init__( self ):
        pass

    def addFuntion( self, id): 
        self[id] = []

    def deleteFunction( self, id ):   
        del self[id]

    def saveDict( self ): 
        print (type(self))
        pkl.dump( dict(self), open( "model.dict", "wb" ) )

    def loadDict( self ): 
        print ('Before upacking model.dic, self ==',type(self))
        self = pkl.load( open( "model.dict", "rb" ) ) 
        print ('After upacking model.dic, self ==',type(self))
        
    def appendInput( self, id, val):
        self[id].append(val)
        
    def updateAllInput( self, id, val):
        self.update({id:val})
    
    def updateInput( self, id, id_input, val):
        self[id][id_input]=val

#if __name__ == '__main__':
#    model = model()
#    #uncomment after first run
#    model.load()
#    print(model)
#    #comment after first run
#    model.add( 'South Park', 'Comedy Central1' )
#    model.save()

