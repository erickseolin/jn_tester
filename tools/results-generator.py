# -*- encoding: utf-8 -*-

''' This script generates random data for fake students. It creates one folder for each student
    in current working directory, where the output files will be written. 
    The files generated are intended to be used to test the complete table with all students' results 
    Shell example: 
    python results-generator.py student1 student2 student3 student4 -t test_one -n 5'''


from argparse import ArgumentParser
import os
import random
try:
    import dill as pickle
except:
    import pickle


parser = ArgumentParser()
parser.add_argument('students', type=str, nargs='+', help='nome dos alunos')
parser.add_argument('-t', '--test_name', type=str, required=True, help="test's name")
parser.add_argument('-n', '--number_of_tests', type=int, default=5, help='number of test cases')
parser.add_argument('--fixed_scores', action='store_true', help='generate random scores in the set {1.0, 0.5 and 0.0}')
parser.add_argument('-N', '--number_of_functions', type=int, default=1, help="Number of functions submited by each student")
parser.add_argument('--skip', action='store_true', help='randomly skip the generation of some functions')
args = parser.parse_args()

students = args.students
test_name = args.test_name
number_of_tests = args.number_of_tests
fixed_scores = args.fixed_scores
number_of_functions = args.number_of_functions
skip = args.skip


for student in students:
    if not os.path.exists(student):
        os.mkdir(student)
    elif os.path.isfile(student):
        print("Path is file. Skipping creation of student's '{}' results.".format(student))
        continue

    entries = []
    
    for i in range(number_of_functions):
        
        # Skip some functions
        if i > 0 and skip:
            if random.random() > 0.5:
                continue
            
        fake_data = {
            'user': student,
            'function': '{}_fnc_{}'.format(test_name, int(random.random()*10)),
        }

        scores = []
        times = []
        memory = []

        for i in range(number_of_tests):
            # Score between 0 and 1
            rnd = random.triangular()
            if fixed_scores:
                scores.append(1.0 if rnd > 0.66 else 0.5 if rnd > 0.33 else 0.)
            else:
                scores.append(rnd)

            # Time between 0 and 500
            times.append(random.triangular(0, 500))
            memory.append(random.triangular(0, 500))

        fake_data.update({'scores': scores})
        fake_data.update({'times': times})
        fake_data.update({'memory': memory})

        print('fake_data: {}'.format(fake_data))
        
        entries.append(fake_data)

    file_path = os.path.join(student, '{}.result'.format(test_name))
    print('Path of the pickle file: {}\n'.format(file_path))

    data = {
        'test_name': test_name,
        'results': entries
    }

    with open(file_path, 'wb') as file:
        pickle.dump(data, file)



