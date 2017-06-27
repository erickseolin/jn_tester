from models import TestCase, TestSet, model


def equal(x, y):
    return 1.0 if x == y else 0.0


def double(b):
    return 2*b



# Simple test
test = TestSet()
test.add_new_test_case(TestCase(2, 4, assert_function=lambda x, y: 1.0 if x == y else 0.0))
test.add_new_test_case(TestCase({'n': 6}, 12, assert_function=equal))
test.add_new_test_case(TestCase({'n': 4}, 8, assert_function=equal))

print('1:', test.evaluate(lambda n: 2**n), 'wrong')       # wrong
print('2:', test.evaluate(double), 'correct')
print('3:', test.evaluate(lambda n: n**2), 'wrong')      # wrong
print()

test.save('dobro.test')

# Load test
test2 = TestSet()
test2.load('dobro.test')

print('1:', test2.evaluate(lambda n: 2**n), 'wrong')       # wrong
print('2:', test2.evaluate(lambda n: 2*n), 'correct')
print('3:', test2.evaluate(lambda n: n**2), 'wrong')      # wrong
print()

# 2 parameter input test

test3 = TestSet()
test3.add_new_test_case(TestCase({'x': 2, 'y': 2}, 4, assert_function=equal))
test3.add_new_test_case(TestCase({'x': 2, 'y': 3}, 5, assert_function=equal))
test3.add_new_test_case(TestCase({'x': 10, 'y': 10}, 20, assert_function=equal))
test3.add_new_test_case(TestCase({'x': 100, 'y': 101}, 201, assert_function=equal))

print('1:', test3.evaluate(lambda x, y: x*y), 'wrong')       # wrong
print('2:', test3.evaluate(lambda x, y: x+y), 'correct')
print('3:', test3.evaluate(lambda x, y: x-y), 'wrong')      # wrong



#

model = model()
model.addFuntion('1')
model.appendInput('1',3)
model.appendInput('1',[4,5])
model.updateAllInput('1',[1,[2,3]])
model.updateInput('1',0,2)
model.saveDict()
model.loadDict()
model.addFuntion('2')
model.appendInput('2',2)
model.appendInput('2',[3,4])
model.updateAllInput('2',[0,[1,2]])
print(model['1'][0])
