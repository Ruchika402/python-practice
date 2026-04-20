# Writing to a file
with open("student.txt","w") as f:
    f.write("ALice,90\n")
    f.write("Bob,85\n")
    f.write("Charlie,92\n")



# Reading a file line by line
with open("student.txt","r") as f:
    for line in f:
        name, score = line.strip().split(",")
        print(f"{name} scored {score}")


# Appending to file
with open("student.txt","a") as f:
    f.write("Diana,88\n")


#reading all lines into a list
with open("student.txt","r") as f:
    lines = f.readlines()
print(f"Total students: {len(lines)}")



#workikng with Json files
import json
data={
    "course":"Djnago full stack",
    "days": 2,
    "topics":["Py","Django","Rest Api","deploy"]
}
with open("course.json","w") as f:
    json.dump(data,f,indent=4)

with open("course.json","r") as f:
    loaded = json.load(f)
    print(loaded["course"])
    print(loaded["topics"][1])




# try/except/else/finally
def read_score(filename):
    try:
        with open(filename,"r") as f:
            content = f.read()
            score = int(content.strip())
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return None
    except ValueError:
        print("Score is not a valid number")
        return None
    else:
        print(f"score read successfully: {score}")

read_score("score.txt")



#raising custom exceptions
class InsufficientFundError(Exception):
    def __init__(self, amount, balance):
        self.amount=amount
        self.balance = balance
        super().__init__(
            f"cannot wothdraw {amount}, balance is only {balance}"
        )
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundError(amount,balance)
    return balance - amount
try:
    result = withdraw(500,800)
except:
    print("None")



# exception chaining
def parse_age(value):
    try:
        return int(value)
    except:
        raise TypeError("age must be whole number")
try:
    parse_age("abc")
except:
    print(None)
    



#custom iterator class
class CountDown:
    def __init__(self,start):
        self.current = start

    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -=1
        return val
for num in CountDown(5):
    print(num,end=", ")
print()




# generator function - memory efficient
def fibonacci_gen(limit):
    a,b = 0,1
    while a<= limit:
        yield a
        a,b = b, a+b
print(list(fibonacci_gen(100)))


# generator expression
square_gen = (x**2 for x in range(1,11))
print(next(square_gen))
print(next(square_gen))
print(sum(square_gen))



#yield from - delegating to sub-generator
def chain(*iterables):
    for it in iterables:
        yield from it
result = list(chain([1,2],[3,4],[5,6]))
print(result)


# infinite generator with send()
def running_avg():
    total, count = 0,0
    while True:
        value = yield total/count if count else 0
        if value is not None:
            total += value
            count += 1
avg = running_avg()
next(avg)
avg.send(10)
avg.send(20)
print(avg.send(30))





import time
import functools

#basic decorator

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start: 4f}s")
        return result
    return wrapper
@timer
def slow_sum(n):
    return sum(range(n))
slow_sum(1_000_000)



# decorator with arguments
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
@repeat(3)
def greet(name):
    print(f"hello,{name}!")
greet("Ruchika")



#stacking multiple decorators
def bold(func):
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

def uppercase(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@bold
@uppercase
def message(text):
    return text
print(message("hello django"))




#class based decorator
class Memorize:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self,func)

    def __call__(self,*args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]
    
@Memorize
def fib(n):
    if n<2:
        return n
    return fib(n-1)+fib(n-2)
print(fib(35))   #instant - cached