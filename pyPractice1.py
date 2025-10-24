
# lambda functions
squareDef = lambda x:x*x
#[print(squareDef(i)) for i in range(10)]

# Dunder methods __funName__ eg, init, next, self (always has double underscroe)
if __name__ == '__main__':
    print("hello world")

# generator functons
nums = [1,2,3,4,5]
it = iter(nums)

"""
print(type(it))
print(next(it))
print(next(it))"""

# user defined generator
class Counter():
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= self.end:
            value = self.current
            self.current += 1
            return value
        else:
            return StopIteration
        
# Generator Function
# using yield instead of return produces values lazily

def counter(start, end):
    while start <= end:
        yield start
        start += 1
for num in counter(1,5):
    print(num)

# iterator vs generator
# iterator is eager / generators are lazy

# generators are newer, have lazy code
# yield is lazy
# generators internally use iterators
# major advantage is memory useage and also automatic Stop Iteration

# spark includes lazy evaluation

# Higher Order functions
# takes another function as an argument or returns a function
#some examples: map() (1 to 1 function)

numbers = [1,2,3,4,5,6]
squares = list(map(lambda x:x**2, numbers))
print("squares:", squares)

# filter HOF
even_nums = list(filter(lambda x: x % 2 == 0, numbers))
print("even_nums:", even_nums)

from functools import reduce

# reduce M to 1 - aggregation HOF
# reduce gives the aggregation from previous calculations as an element in the next function calculation
product = reduce(lambda x, y: x*y, numbers)
print("product:",product)


# Custom HOFs
def apply(func, value):
    return func(value)

def tenmult(num):
    return num*10

print(apply, 10)

# Closure Function
# a special type of nested function
# can predefine an arg using this

def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier
# the outer return makes it a clusure function (different from a nested function)

times3 = make_multiplier(3)
print(type(times3))
print(times3(5))
print(times3.__closure__)
print(times3.__closure__[0].cell_contents)

"""
| **Feature**                      | **Nested Function** | **Closure** |
| -------------------------------- | ------------------- | ----------- |
| Defined inside another function  | Y                   | Y           |
| Accesses outer variable          | Y                   | Y           |
| Returned by outer function       | N                   | Y           |
| Remembers state after outer ends | N                   | Y           |


| **Use Case**           | **Description**                                                    |
| ---------------------- | ------------------------------------------------------------------ |
| **Data Hiding**        | Variables inside the closure are not accessible directly.          |
| **State Retention**    | Keeps state between function calls without using global variables. |
| **Function Factories** | Dynamically create functions with preset configurations.           |
| **Decorator Building** | Most decorators rely on closures to wrap functions.                |

"""

# Decorator functions

def logger(func):
    def wrapper():
        print(f'Running {func.__name__}()')

# slicing
print(list1)
print(list1[-1:0:-1])