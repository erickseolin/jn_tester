# -*- encoding: utf-8 -*-

import glob
import os
import logging
from itertools import chain
from IPython.display import display, HTML
import pandas as pd
import dill as pickle


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def view_complete_table(test_name, base_path='/home/*/'):
    ''' Gathers the results submited by all students and shows them in a table ranked by 
    score and elapsed time.
    A result file is assumed to have the name ".TEST_NAME-STUDENT_ID.score".
    This function will search for result files in all subdirectories of base_path.
    :param test_name: test's name
    :param base_path: base path glob for result files. '''

    if '/**/' not in base_path:
        logging.debug("If you want a recursive scan, please add /**/ to the end of your chosen path.")

    pattern = os.path.join(base_path, ".{test_name}-*.score".format(test_name=test_name))
    result_files = glob.glob(pattern, recursive=True)

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
                data['final_score'] = sum(data['score']) / float(len(data['score']))
                data['mean_time'] = sum(data['time']) / float(len(data['time']))
                results.append(data)
        except Exception as err:
            # Failed to read the file or access data values: ignore
            cls_err = err.__class__.__name__
            logging.debug("Exception happen {0} - {1}".format(cls_err, err))
            continue

    # Sorts by descending final score and then ascending by mean execution time
    results = sorted(results, reverse=True, key=lambda r: (r['final_score'], -r['mean_time']))

    # Transform into list with order: ranking, funcname, user, Test[i] Score, Test[i] Time, Mean Time, Final score
    ## Generate column headers:
    columns_headers = ['Function Ranking', 'Function', 'Author', 'Mean Time (ms)', 'Final Score']
    N = len(results[0]['score']) + 1
    test_headers = list(chain.from_iterable(('Test {}: Score'.format(i), 'Test {}: Time (ms)'.format(i)) for i in range(1,N)))
    columns_headers[3:3] = test_headers

    
    ## Transform the data
    results_list = []

    for rank, r in enumerate(results):
        rlist = list([rank+1, r['funcname'], r['user'], '{0:.2f}'.format(r['mean_time']), '{0:.2f}'.format(r['final_score'])])
        tests_score_time = list(chain.from_iterable(('{0:.2f}'.format(r['score'][i]), '{0:.2f}'.format(r['time'][i])) for i in range(len(r['score']))))
        
        # Commented: times and scores as floats instead of strings {0:.2f}
        # rlist = list([rank+1, r['funcname'], r['user'], r['mean_time'], r['final_score']])
        # tests_score_time = list(chain.from_iterable((r['scores'][i], r['times'][i]) for i in range(len(r['scores']))))
        rlist[3:3] = tests_score_time

        results_list.append(rlist)

    df = pd.DataFrame(data=results_list, columns=columns_headers)
    display(HTML(df.to_html(index=False)))