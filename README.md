# jn_tester
Jupyter notebook code grading system.

## Installation:

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
from jn_tester.professor.models import TestSet

def equal(x, y):
    return 1.0 if x == y else 0.0

def double(b):
    return 2 * b

# Simple test
test = TestSet()
test.add_test(2, 4, assert_function=lambda x, y: 1.0 if x == y else 0.0)
test.add_test({'n': 6}, 12, assert_function=equal)
test.add_test({'n': 4}, 8, assert_function=equal)

print('1:', test.evaluate(lambda n: 2**n), 'wrong')       # wrong
print('2:', test.evaluate(double), 'correct')
print('3:', test.evaluate(lambda n: n**2), 'wrong')      # wrong

test.save('dobro.test')
 ```

 - After the submission of the solutions, it is possible to show the table with sort options.
 
 ```python
 import os
 from jn_tester.professor.tables import view_complete_table
 
 # Keep in mind that you may need to pass the base path to look for all students files
 base_path = '/'.join(os.getcwd().split('/')[:-1]) + '/**/'
 
 sort = [('time', False), ('rank', True)]
 view_complete_table('dobro', base_path=base_path, sort_by=sort)
 ```
 
 - After the visualization, it is possible to export the results to .csv, .pkl and .html
 
 ```python
 
 import os
 from jn_tester.professor.tables import export_complete_table

 base_path = '/'.join(os.getcwd().split('/')[:-1]) + '/**/'
 sort = [('time', False), ('rank', True)]

 export_complete_table('dobro', base_path, sort_by=sort)
 export_complete_table('dobro', base_path, export_format='pkl')
 export_complete_table('dobro', base_path, export_format='html') 
 ```
 

### Students usage:

To run the tests created by the professor, import the test file, run tests and finally submit the tests for the professor.

```python
# -*- encoding: utf-8 -*-

from jn_tester.student.test import run_test, submit_test


if __name__ == '__main__':
    run_test('dobro', fnc=lambda n: 2 ** n)
    run_test('dobro', fnc=lambda n: 3 * n)
    submit_test('dobro', fnc=lambda n: 3 * n, presentation_mode='table')
```
