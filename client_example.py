# -*- encoding: utf-8 -*-

from client.test import run_test


if __name__ == '__main__':
    print(run_test('dobro', fnc=lambda n: 2 ** n))