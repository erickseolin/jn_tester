import models
from models import TestCase, TestSet

tc = TestCase(2, 4, assert_type=models.ASSERT_EQUAL)

print('1:', tc.evaluate(lambda n: 1*n))       # wrong
print('1:', tc.evaluate(lambda n: 2*n))
print('1:', tc.evaluate(lambda n: 3*n))       # wrong
print()

tc = TestCase(2, 8, assert_function=lambda x, y: 1.0 if x == y else 0.0)

print('1:', tc.evaluate(lambda n: 1*n))       # wrong
print('2:', tc.evaluate(lambda n: 2*n))       # wrong
print('3:', tc.evaluate(lambda n: n**3))
print()


def equal(x, y):
    return 1.0 if x == y else 0.0

tc = TestCase(2, 8, assert_function=equal)

print('1:', tc.evaluate(lambda n: 1*n))       # wrong
print('2:', tc.evaluate(lambda n: 2*n))       # wrong
print('3:', tc.evaluate(lambda n: n**3))
print()
