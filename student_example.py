# -*- encoding: utf-8 -*-

from student.test import run_test, submit_test


if __name__ == '__main__':
    print(run_test('dobro.test', fnc=lambda n: 2 ** n))
    print(run_test('dobro.test', fnc=lambda n: 3 * n))
    submit_test('dobro.test', 'rdenadai', fnc=lambda n: 3 * n)