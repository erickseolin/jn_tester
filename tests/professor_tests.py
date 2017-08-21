import unittest
import os.path
import os

from jn_tester.professor.models import TestCase, TestSet, load_test_set, MalformedTestCase


def equal(x, y):
    return 1.0 if x == y else 0.0


def double(n):
    return 2*n


def sum_f(x, y):
    return x + y


def sub_f(a, b):
    return a - b


def triple(n):
    return 3*n


class TestTestCaseMethods(unittest.TestCase):

    def test_malformed_test_case(self):
        with self.assertRaises(MalformedTestCase):
            TestCase(0, 0, 0)

        with self.assertRaises(MalformedTestCase):
            TestCase(0, 0, 'text')

    def test_evaluate(self):
        tc = TestCase(1, 2, equal)
        # test functions
        self.assertEqual(tc.evaluate(double), equal(2, 2))  # right
        self.assertEqual(tc.evaluate(triple), equal(2, 3))  # wrong

        # test lambda functions
        self.assertEqual(tc.evaluate(lambda x: 2*x), equal(2, 2))  # right
        self.assertEqual(tc.evaluate(lambda x: 3*x), equal(2, 3))  # wrong

    def test_performance(self):
        tc = TestCase(1, 2, equal)

        perform = tc.performance(double)
        self.assertIsInstance(perform, dict)
        self.assertIsNotNone(perform.get('memory', None))
        self.assertIsNotNone(perform.get('time', None))

    def test_dict_inputs(self):
        tc = TestCase({'x': 6, 'y': 5}, 11, assert_function=equal)

        self.assertEqual(tc.evaluate(lambda x, y: x + y), equal(11, 11))
        self.assertEqual(tc.evaluate(lambda x, y: 3), equal(3, 11))
        # Normal function
        self.assertEqual(tc.evaluate(sum_f), equal(11, 11))

    def test_dict_warning(self):
        import warnings

        tc = TestCase({'x': 6, 'y': 5}, 11, assert_function=equal)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            # raise warning for lambda function
            self.assertEqual(tc.evaluate(lambda a, b: a + b), equal(11, 11))

            self.assertEqual(w[-1].category, UserWarning)
            self.assertRegexpMatches(str(w[-1].message), "Function '\S+' have different arguments")

            # raise warning for normal function
            self.assertEqual(tc.evaluate(sub_f), equal(1, 11))
            self.assertEqual(w[-1].category, UserWarning)
            self.assertRegexpMatches(str(w[-1].message), "Function '\S+' have different arguments")


class TestTestSetMethods(unittest.TestCase):

    def setUp(self):
        test = TestSet()
        test.add_test(2, 4, lambda x, y: 1.0 if x == y else 0.0)
        test.add_test({'n': 6}, 12, equal)
        test.add_test({'n': 4}, 8, equal)

        test.add_closed_test(1000, 2000, equal)
        test.save('temp_test')

        if os.path.isfile('temp_save.test'):
            os.remove('temp_save.test')
        if os.path.isfile('temp_save.tst'):
            os.remove('temp_save.tst')

    def tearDown(self):
        os.remove('temp_test.test')

    def test_add_tests(self):
        test = TestSet()
        test.add_test(2, 4, lambda x, y: 1.0 if x == y else 0.0)
        test.add_test({'n': 6}, 12, equal)
        test.add_test({'n': 4}, 8, equal)
        test.add_closed_test(1000, 2000, equal)

        self.assertEqual(len(test.test_cases), 3)
        self.assertEqual(test.closed_tests_count(), 1)

    def test_save(self):
        test = TestSet()

        self.assertFalse(os.path.isfile('temp_save.test'))
        test.save('temp_save')
        self.assertTrue(os.path.isfile('temp_save.test'))
        os.remove('temp_save.test')

    def test_save_different_extension(self):
        test = TestSet()

        self.assertFalse(os.path.isfile('temp_save.tst'))
        test.save('temp_save.tst')
        self.assertTrue(os.path.isfile('temp_save.tst'))
        os.remove('temp_save.tst')

    def test_load(self):
        test = load_test_set('temp_test')

        self.assertEqual(len(test.test_cases), 3)
        self.assertEqual(test.closed_tests_count(), 1)

    def test_evaluate(self):
        test = load_test_set('temp_test')

        evaluation1 = test.evaluate(double)
        self.assertEqual(len(evaluation1), 4)
        evaluation2 = test.evaluate(lambda n: n*2)
        self.assertEqual(len(evaluation2), 4)
        evaluation3 = test.evaluate(lambda n: n**2)
        self.assertEqual(len(evaluation3), 4)

        self.assertEqual(evaluation1, evaluation2)
        self.assertNotEqual(evaluation2, evaluation3)

    def test_performance(self):
        test = load_test_set('temp_test')

        performance = test.evaluate(double)
        self.assertEqual(len(performance), 4)
        performance = test.evaluate(lambda n: n * 2)
        self.assertEqual(len(performance), 4)
        performance = test.evaluate(lambda n: n ** 2)
        self.assertEqual(len(performance), 4)

    def test_fail_to_get_closed_tests(self):
        test = load_test_set('temp_test')

        with self.assertRaises(AttributeError):
            _ = test.__closed_tests

    def test_get_input_and_output_from_tests(self):
        test = load_test_set('temp_test')

        self.assertEqual(test[0].input, 2)
        self.assertEqual(test[0].output, 4)

        self.assertDictEqual(test[1].input, {'n': 6})
        self.assertEqual(test[1].output, 12)

    def test_only_open_tests_in_iteration_and_indexation(self):
        test = load_test_set('temp_test')

        with self.assertRaises(IndexError):
            _ = test[3].input

        count = 0
        for _ in test:
            count += 1

        self.assertEqual(count, 3)

if __name__ == '__main__':
    unittest.main()
