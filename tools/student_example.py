# -*- encoding: utf-8 -*-

from jn_tester.student.test import run_test, submit_test


def vezes_2(n):
    return 2 * n

if __name__ == '__main__':
    print(run_test('dobro', fnc=lambda n: 2 ** n))
    print(run_test('dobro', fnc=lambda n: 3 * n))
    submit_test('dobro', fnc=vezes_2, presentation_format='table')