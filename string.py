'''
a = "University"
for ch in str(a):
    print(ch, end=" \n") 
'''
'''
x = "exam"
print("x" in x)    
'''
'''
a = "Data"
b = "Structure"
print(a + " "+b)
'''
'''
n = "HI!"
print((n+" ")*5)

print(ord('Z'))
print(chr(100))
'''
'''
a = "python"
print(a[2:])
b = " University"
print(b[::-1])
c = "DataStructure"
print(c[::2])
d = "HelloWorld"
print(d[-5:])
x = "zebra"
print(len(x),min(x),max(x))
print(ord('Z'),chr(120))
'''
'''
a = "exam preparation"
print(a.upper())
b = "Data Structure"
print(b.startswith("Data"))
c = "I like pyhton"
print(c.replace("pyhton","Java"))
d = "banana"
print(d.count("a"))
e = "A,B,C,D".split(",")
print(e)
print(" ".join(e))
f = "   Hello World   "
print(f.strip())
n = "12345"
print(n.isdigit())
m = "PyThoN"
print(m.swapcase())
'''
'''
def add (a,b):
    return a+b
print(add(3,5))

def swap(a,b):
    return b,a
a,b = swap(2,30)
print(a,b)

def divide(x,y):
    q = x//y
    r = x%y
    return q,r
print(divide(13,6))

def is_even(n):
    if n%2==0:
        return True
    else:
        return False
print(is_even(10))

def max_of_three(a,b,c):
        for i in (a,b,c):
            if i>=a and i>=b and i>=c:
                return i
print(max_of_three(10,5,8))
'''
'''
def multiply(a,b=2):
    return a*b
print(multiply(3))

def greet (name, msg="Welcome!"):
    print("Hello!",name+" you are",msg)
greet(name="John")
greet("Alice")

def sum_all(*args):
    Sum = 0
    for i in args:
        Sum += i
    return Sum
print(sum_all(1,2,3,4,5))

def info(**kwargs):
    print(kwargs)
info(name="John", age=25, city="New York")
info(course="Python", duration="3 months")

#local variable
def func():
    x = 10
    print("Inside func:",x)
func()
#global variable
x=10
def func():
  print(x)
func()    
'''
'''
def fact(n):
    if n==0 or n==1:
        return 1
    else:
        return n*fact(n-1)
print(fact(5))

def fib(n):
    if n<=1:
        return n
    else:
        return fib(n-1)+fib(n-2)
print(fib(7))

even = lambda x: x%2==0
print(even(4))

nums=[1,2,3,4,5,6]
cubes = list(map(lambda x: x**3, nums))
print(cubes)

nums = [5,10,15,20,25]
x = list(filter(lambda a: a>10, nums))
print(x)

from functools import reduce
nums =[1,2,3,4,5]
sum = reduce(lambda a,b: a+b, nums)
print(sum)
'''
'''
# reverse without slicing
s = "PythonProgramming"
rev = ""
for ch in s:
    rev = ch + rev  
print(rev)


def area_circle(r):
    import math
    return math.pi * r * r
print(area_circle(5))

def calc(x,y):
    sum = x+y
    pro = x*y
    return sum,pro
print(calc(3,4))

def intro(name, age=19):
    print("My name is",name," and I am am ",age," years old.")
intro("Alice")
intro("Bob",25)

def multiply_all(*nums):
    result = 1
    for n in nums:
        result *= n
    return result
print(multiply_all(2,3,4))

def sum(n):
    if n==0:
        return 0
    else:
        return n+sum(n-1)
print(sum(5))

def fib(n):
    if n<1:
        return n
    else:
        return fib(n-1)+fib(n-2)
print(fib(6))

nums= [1,2,3,4,5]
x = list(map(lambda a:a**2, nums))
print(x)

words = ["apple", "mango", "banana", "kiwi", "pear"]
x = list(filter(lambda a: len(a)>4, words))
print(x)

from functools import reduce
nums = [12, 7, 19, 3, 25, 8]
max_num = reduce (lambda a, b: a if a>b else b, nums)
print(max_num)

# fibonacci with loop
def fib(n):
    seq = []
    a,b = 0,1
    for _ in range(n):
        seq.append(a)
        a,b = b, a+b
    return seq
print(fib(7))
'''
'''
students=[]
students.append(["Alice",20])
students.append(["Bob",22])
print(students)
print(list("hello"))
nums=[10,20,30,40,50]
print(nums[0])
print(nums[-1])
n = [0,1,2,3,4,5,6]
print(n[2:4])
'''
'''
a =[5,10,15]
a.insert(1,20)
a.append(25)
a.extend([30,35])
print(a)
b = [1,2,3,2,4,2,5]
b.remove(2)
print(b)
b.pop()
print(b)
b.clear()
print(b)
list = [3,5,7,9,7,11]
print(list.index(7))
print(list.count(7))
list1 =[50,10,40,20,30]
list1.sort()# ascending
print(list1)
list1.sort(reverse=True)# descending
print(list1)
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4]
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)   # [1, 2, 3]
print(b)   # [1, 2, 3, 4]
'''
'''
nums =[5,10,15]
for i,v in enumerate(nums):
    print(i,v)

c = [x**3 for x in range(1,6)]
print(c)

words = ["python","java","c","perl"]
a_words =[w for w in words if len(w)>3]
print(a_words)

mat = [[1,2,3],[4,5,6],[7,8,9]]
print(mat[1][2])

for row in mat:
    for val in row:
        print(val,end=" ")
    print()
'''

t = (1,2,3,4,5)
print(len(t))
t1 = (10,20,30,40,50)
print(t1[1:4])
t2=(1,2,3,2,4,2,5)
print(t2.count(2))
print(t2.index(4))
t3 = (1,2,3)
t4 = (4,5,6)
t5 = (t3 + t4)
t6 = t5*2
print(t5)
print(t6)
t7 = 100,200,300
x,y,z = t7
print(x,y,z)