# jn_tester
Jupyter notebook code grading system.

## Intalation:

Clone this repository and run the setup.py:
```
git clone https://github.com/erickseolin/jn_tester.git
cd jn_tester
python setup.py install
```

## Usage:

### Professor usage:

 - Create a new TestSet model.
 - Add some TestCases.
 - Save the model.
 
 ```python
from jn_tester.professor.models import TestCase, TestSet

def equal(x, y):
    return 1.0 if x == y else 0.0

def double(b):
    return 2 * b

# Simple test
test = TestSet()
test.add_new_test_case(TestCase(2, 4, assert_function=lambda x, y: 1.0 if x == y else 0.0))
test.add_new_test_case(TestCase({'n': 6}, 12, assert_function=equal))
test.add_new_test_case(TestCase({'n': 4}, 8, assert_function=equal))

print('1:', test.evaluate(lambda n: 2**n), 'wrong')       # wrong
print('2:', test.evaluate(double), 'correct')
print('3:', test.evaluate(lambda n: n**2), 'wrong')      # wrong
print()

test.save('dobro.test')
 ```

 - After the users executed their tests and submit the solution you could run the table.
 ```python
 from jn_tester.professor.tables import view_complete_table
 
 # Keep in mind that you may need to pass the base path to look for all students files
 view_complete_table('dobro.test')
 ```
 

### Students usage:

To run the tests create by the professor import the test file, run tests and finally 
submit the tests for the professor.

```python
# -*- encoding: utf-8 -*-

from jn_tester.student.test import run_test, submit_test


if __name__ == '__main__':
    print(run_test('dobro.test', fnc=lambda n: 2 ** n))
    print(run_test('dobro.test', fnc=lambda n: 3 * n))
    submit_test('dobro.test', 'rdenadai', fnc=lambda n: 3 * n)
```
