# -*- encoding: utf-8 -*-

import glob
import os
import warnings
from itertools import chain
from IPython.display import display, HTML
import pandas as pd
import dill as pickle
from .models import ResultScanner


def view_complete_table(test_name, base_path='./'):
    ''' Gathers the results submited by all students and shows them in a table ranked by 
    score and elapsed time.
    A result file is assumed to have the name ".TEST_NAME-STUDENT_ID.score".
    This function will search for result files in all subdirectories of base_path.
    :param test_name: test's name
    :param base_path: base path glob for result files. '''

    # pattern = os.path.join(base_path, ".{test_name}-*.score".format(test_name=test_name))
    # result_files = glob.glob(pattern)
    result_sets = ResultScanner(test_name).scan_dir(base_path)

    # if len(result_files) == 0:
    #    raise Exception('Zero result files found.')

    # results = []
    # print(result_files)
    # for result_file in result_files:
        
    #    try:
    #        with open(result_file, 'rb') as file:
    #            pdata = pickle.load(file)
                # Optional TODO: Check if the data fits in the defined model
                # Expected data: list of dicts with keys (funcname, user, scores and times)
                
    #        if not isinstance(pdata, list):
    #            pdata = [pdata]

    results = []

    for result_set in result_sets:
        for res in result_set:
            res['final_score'] = sum(res['scores']) / float(len(res['scores']))
            res['mean_time'] = sum(res['times']) / float(len(res['times']))
            results.append(res)


    #for result in results:
    #    for data in pdata:
    #        data['final_score'] = sum(data['score']) / float(len(data['score']))
    #        data['mean_time'] = sum(data['time']) / float(len(data['time']))
    #        results.append(data)

    #    except Exception as err:
            # Failed to read the file or access data values: ignore
    #        cls_err = err.__class__.__name__
    #        warnings.warn("Exception happen {0} - {1}".format(cls_err, err))
    #        continue

    if results:
        # Sorts by descending final score and then ascending by mean execution time
        results = sorted(results, reverse=True, key=lambda re: (re['final_score'], -re['mean_time']))

        # Transform into list with order: ranking, funcname, user, Test[i] Score, Test[i] Time, Mean Time, Final score
        ## Generate column headers:
        columns_headers = ['Function Ranking', 'Function', 'Author', 'Mean Time (ms)', 'Final Score']
        N = len(results[0]['scores']) + 1
        test_headers = list(chain.from_iterable(('Test {}: Score'.format(i), 'Test {}: Time (ms)'.format(i)) for i in range(1,N)))
        columns_headers[3:3] = test_headers

        ## Transform the data
        results_list = []

        for rank, r in enumerate(results):
            rlist = list([rank+1, r['function'], r['user'], '{0:.2f}'.format(r['mean_time']), '{0:.2f}'.format(r['final_score'])])
            tests_score_time = list(chain.from_iterable(('{0:.2f}'.format(r['scores'][i]), '{0:.2f}'.format(r['times'][i])) for i in range(len(r['scores']))))

            # Commented: times and scores as floats instead of strings {0:.2f}
            # rlist = list([rank+1, r['funcname'], r['user'], r['mean_time'], r['final_score']])
            # tests_score_time = list(chain.from_iterable((r['scores'][i], r['times'][i]) for i in range(len(r['scores']))))
            rlist[3:3] = tests_score_time

            results_list.append(rlist)

        df = pd.DataFrame(data=results_list)
        df.columns = columns_headers

        display(HTML(df.to_html(index=False)))
    else:
        print("No results found.")