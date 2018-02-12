a = 5
b = 4.3

c = a / 2      # float
d = a // 2     # force integer
e = int(a / 2) # conversion to integer

# print
print("str", c, d, e) # str 2.5 2 2

# string interpolation
print(f"c: {type(c)} {c}") # c: <class 'float'> 2.5
print(f"d: {type(d)} {d}") # d: <class 'int'> 2
print(f"e: {type(e)} {e}") # e: <class 'int'> 2

# for loop [0;10[
# 0 1 2 3 4 5 6 7 8 9
for i in range(10):
    print(i)
# for loop range(start, stop[, step])
# 2 5 8
for i in range(2, 10, 3):
    print(i)

# if 1
x = 5
if (x % 2 == 1): # parentheses are optionals
    print("impair")
else:
    print("pair")

# if 2
if (x == 5) or (x == 4):
    print("5 or 4")

# function
def add(a, b):
    return a + b

# named args invocation
print(add(a = 4, b = 5)) # 4 + 5 = 9

# lambda 1
def makeIncrementor(n):
    return lambda x: x + n
incrementor = makeIncrementor(5) # x + 5
print(incrementor(3)) # 3 + 5 = 8

# lambda 2
def executeFunction(f): f()
def someFunction(): print("someFunction")
executeFunction(someFunction)
executeFunction(lambda: print("lambda"))
