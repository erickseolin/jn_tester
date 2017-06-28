# -*- encoding: utf-8 -*-

import glob
import os
from itertools import chain
import pandas as pd
from IPython.display import display, HTML
try:
    import dill as pickle
except:
    import pickle
    

def view_complete_table(test_name, base_path='/home/*/'):
    ''' Gathers the results submited by all students and shows them in a table ranked by 
    score and elapsed time.
    A result file is assumed to have the name ".TEST_NAME-STUDENT_ID.score".
    This function will search for result files in all subdirectories of base_path.
    :param test_name: test's name
    :param base_path: base path glob for result files. '''

    pattern = os.path.join(base_path, ".{test_name}-*.score".format(test_name=test_name))
    result_files = glob.glob(pattern)
    
    if len(result_files) == 0:
        raise Exception('Zero result files found.')

    results = []
    for result_file in result_files:
        
        try:
            with open(result_file, 'rb') as file:
                pdata = pickle.load(file)
                # Optional TODO: Check if the data fits in the defined model
                # Expected data: list of dicts with keys (funcname, user, scores and times)
                
            if not isinstance(pdata, list):
                pdata = [pdata]
            
            for data in pdata:
                data['final_score'] = sum(data['scores']) / float(len(data['scores']))
                data['mean_time'] = sum(data['times']) / float(len(data['times'])) 
                results.append(data)

        except Exception as e:
            # Failed to read the file or access data values: ignore
            continue

    # Sorts by descending final score and then ascending by mean execution time
    results = sorted(results, reverse=True, key=lambda r: (r['final_score'], -r['mean_time']))

    # Transform into list with order: ranking, funcname, user, Test[i] Score, Test[i] Time, Mean Time, Final score
    ## Generate column headers:
    columns_headers = ['Function Ranking', 'Function', 'Author', 'Mean Time (ms)', 'Final Score']
    N = len(results[0]['scores']) + 1
    test_headers = list(chain.from_iterable(('Test {}: Score'.format(i), 'Test {}: Time (ms)'.format(i)) for i in range(1,N)))
    columns_headers[3:3] = test_headers

    
    ## Transform the data
    results_list = []

    for rank, r in enumerate(results):
        rlist = list([rank+1, r['funcname'], r['user'], '{0:.2f}'.format(r['mean_time']), '{0:.2f}'.format(r['final_score'])])
        tests_score_time = list(chain.from_iterable(('{0:.2f}'.format(r['scores'][i]), '{0:.2f}'.format(r['times'][i])) for i in range(len(r['scores']))))
        
        # Commented: times and scores as floats instead of strings {0:.2f}
        # rlist = list([rank+1, r['funcname'], r['user'], r['mean_time'], r['final_score']])
        # tests_score_time = list(chain.from_iterable((r['scores'][i], r['times'][i]) for i in range(len(r['scores']))))
        rlist[3:3] = tests_score_time

        results_list.append(rlist)

    df = pd.DataFrame(data=results_list)
    df.columns = columns_headers

    display(HTML(df.to_html(index=False)))