import models
from models import TestCase, TestSet

tc1 = TestCase(2, 4, assert_function=lambda x, y: 1.0 if x == y else 0.0)

print('1:', tc1.evaluate(lambda n: 1*n))       # wrong
print('1:', tc1.evaluate(lambda n: 2*n))
print('1:', tc1.evaluate(lambda n: 3*n))       # wrong
print()

tc2 = TestCase(6, 12, assert_function=lambda x, y: 1.0 if x == y else 0.0)

print('1:', tc2.evaluate(lambda n: 1*n))       # wrong
print('2:', tc2.evaluate(lambda n: 2*n))       # wrong
print('3:', tc2.evaluate(lambda n: n**3))
print()


def equal(x, y):
    return 1.0 if x == y else 0.0

tc3 = TestCase(4, 8, assert_function=equal)

print('1:', tc3.evaluate(lambda n: 1*n))       # wrong
print('2:', tc3.evaluate(lambda n: 2*n))
print('3:', tc3.evaluate(lambda n: n**2))      # wrong
print()


test = TestSet()
test.add_new_test_case(tc1)
test.add_new_test_case(tc2)
test.add_new_test_case(tc3)

print('1:', test.evaluate(lambda n: 1*n))       # wrong
print('2:', test.evaluate(lambda n: 2*n))
print('3:', test.evaluate(lambda n: n**2))      # wrong
print()

test.save('dobro.test')

test2 = TestSet()
test2.load('dobro.test')

print('1:', test2.evaluate(lambda n: 1*n))       # wrong
print('2:', test2.evaluate(lambda n: 2*n))
print('3:', test2.evaluate(lambda n: n**2))      # wrong

