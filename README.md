# jn_tester
Jupyter notebook code grading system.

## Installation:

Clone this repository and run the setup.py:
```
git clone https://github.com/erickseolin/jn_tester.git
cd jn_tester
python setup.py install
# or
# `pip install .`
# for environment install
```

## Usage:

### Professor usage:

 - Create a new TestSet model.
 - Add some open and closed test cases.
 - Save the TestSet.
 - Share the created file with the students.
 
 ```python
from jn_tester.professor.models import TestSet

def equal(x, y):
    return 1.0 if x == y else 0.0

def double(b):
    return 2 * b

# Create TestSet and add test cases
test = TestSet()
test.add_test(2, 4, assert_function=equal)
test.add_test({'n': 6}, 12, assert_function=equal)
test.closed_test({'n': 4}, 8, assert_function=equal)  # closed test

# save the tests
test.save('double.test')
 ```

### Students usage:

To see input and output for the open tests

```python
tests = load_test_set('double')

for test in tests:
    print('input:', test.input)
    print('output:', test.output, '\n')
    
# ------- OR ----------------

print('input 0:', tests[0].input)
print('output 0:', tests[0].output)
```

To run the tests created by the professor and submit for evaluation.

```python
from jn_tester.student.test import run_test, submit_test

def my_double(n):
    return 2 * n

def my_double2(n):
    return n ** 2

# Run the tests without submit
run_test('double', fnc=my_double)
run_test('double', fnc=my_double2)

# submit the tests for evaluation
submit_test('double', fnc=my_double, presentation_mode='table')
```

### Results visualization:

 After the submission of the solutions by the students, it is possible to show a table with the results with sort options.
 
 ```python
 import os
 from jn_tester.professor.tables import view_complete_table
 
 # Keep in mind that you may need to pass the base path to look for all students files
 base_path = '/path_to_base_directory/**/'
 
 sort = [('time', True), ('rank', True)]
 view_complete_table('double', base_path=base_path, sort_by=sort)
 ```
 
 It is possible to export the results to .csv, .pkl and .html
 
 ```python
 from jn_tester.professor.tables import export_complete_table

 export_complete_table('double', base_path, sort_by=sort)
 export_complete_table('double', base_path, export_format='pkl')
 export_complete_table('double', base_path, export_format='html') 
 ```
