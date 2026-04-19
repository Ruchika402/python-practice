#for loop with range
for i in range(1,6):
    print(f"Count:{i}")

# while loop
n=10
while n > 0:
    print(n, end =" ")
    n -= 2
print()

# loop with else
for i in range (3):
    print(f"Try {i}")
else:
    print("Loop finished")

#nested loop
for i in range (1,4):
    for j in range(1,4):
        print(f"{i}x{j}={i*j}", end =", ")
    print()

# list comprehension
squares = [x**2 for x in range(1,11)]
print("Squares:", squares)


# dict comprehension
word_lengths = {word: len(word) for word in ["python", "djnago", "flask"]}
print(word_lengths)


#basic function
def greet(name):
    return f"Hello, {name}"
print(greet("djnago dev ruchika"))


# default arguments
def power(base, exp=2):
    return base ** exp
print(power(3))
print(power(2, 10))


# *arg - variable positional args
def total(*nums):
    return sum(nums)
print(total(1,2,3,4,5,6))


#**kwargs - variable keyword args
def profile(**info):
    for key, val in info.items():
        print(f" {key}: {val}")
profile(name="Ruchika", role = "Developer", city="Rishra")


#Lambda function
double = lambda x: x*2
print(list(map(double,[1,2,3,4])))

#recursive function
def factorial(n):
    if n == 0:
        return 1
    return n*factorial(n-1)

print(factorial(5))



#first class function passing function
def apply(func, value):
    return func(value)
print(apply(lambda x: x+100,42))


#class dfinition + __init__
class Animal:

    species = "Unknown" 

    def __init__(self,name,sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"
    
    def __str__(self):
        return f"Animal({self.name})"
    
cat = Animal("Whiskers", "Meow")
dog = Animal("Buddy", "Woof")
print(cat.speak())  
print(dog.speak())
print(cat)
print(dog)



#Inheritence
class Dog(Animal):

    def __init__(self, name, breed):
        super().__init__(name, "Woof")
        self.breed = breed

    def fetch(self):
        return f"{self.name} is fetching the ball!"
    
    def speak(self):
        return f"{self.name} barks loudly!"
    
buddy = Dog("Buddy", "Labrador")
print(buddy.speak())
print(buddy.fetch())
print(isinstance(buddy, Animal))


# Encapsulation - private attribute
class BannkAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0 :
            self.__balance += amount
            return f"Deposited {amount}. New balance: {self.__balance}"

    def withdraw(self, amount):
        if amount > self.__balance:
            return "Insufficient funds"
        self.__balance -= amount
        return f"Withdrew {amount}. New balance: {self.__balance}"
    def get_balance(self):
        return self.__balance
    def __repr__(self):
        return f"BankAccount({self.owner}, ₹{self.__balance})"
    
account = BannkAccount("Ruchika", 1000)
print(account.deposit(500)) 
print(account.withdraw(200))
print(account.get_balance())
print(account)

#class methos and static method
class MathHelper:
    pi = 3.141592654
    @classmethod
    def circle_area(cls, radius):
        return cls.pi * radius ** 2
    @staticmethod
    def add(a,b):
        return a + b

print(MathHelper.circle_area(5))
print(MathHelper.add(10, 20))


#Polymorphism
class Shape:
    def area(self):
        raise NotImplementedError
class Circle(Shape):
    def __init__(self, r): 
        self.radius = r

    def area(self):
        return MathHelper.pi * self.radius ** 2
class Rectangle(Shape):
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def area(self):
        return self.width * self.height
    
shapes = [Circle(3), Rectangle(4,5)]
for shape in shapes:
    print(f"Area: {shape.area()}")



#Exception handling
def safe_divided(a,b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError:
        return "Invalid input type"
    else:
        return result
    finally:
        print("Division attempt completed")

print(safe_divided(10,2))
print(safe_divided(10,0))


#list , dict, set operations
fruits = ["apple", "banana", "cherry"]
unique = set(fruits)
print(f"Unique fruits: {unique}")

#generator function
def fibinacci(n):
    a,b = 0,1
    for _ in range(n):
        yield a
        a,b = b, a+b
print(list(fibinacci(10)))


#decorator
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper
@logger
def multiply(x,y):
    return x*y
print(multiply(5,7))