# ABC cLASSES
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    @abstractmethod
    def perimeter(self) -> float:
        pass
    def describe(self)-> str:
        return f"{self.__class__.__name__} with area {self.area():.2f} and perimeter {self.perimeter():.2f}"
    
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    def area(self) -> float:
        return 3.14 * self.radius ** 2
    def perimeter(self) -> float:
        return 2 * 3.14 * self.radius
    
class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    def area(self) -> float:
        return self.width * self.height
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
shapes = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    print(shape.describe())


# Protocols and structural subtyping
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        ...     #"..." means abstract like pass, but for Protocols

class Button:
    def __init__(self, radius: float):
        self.radius = radius

class Button:
    def draw(self) -> str:
        return "Drawing Button"

class Icon:
    def draw(self) -> str:
        return "Drawing Icon"

def render(component: Drawable) -> None:
    print(component.draw())

render(Button())   # works — no inheritance needed!
render(Icon())     # duck typing + static type check


#dataclasses
from dataclasses import dataclass,field,asdict
from typing import List

@dataclass
class Student:
    name: str
    age: int
    grades: List[float] = field(default_factory=list)
    roll_no : int = field(default = 0,repr = False)

    def average_grade(self) -> float:
        return sum(self.grades) / len(self.grades) if self.grades else 0.0
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")
student1 = Student(name="Alice", age=20, grades=[85.5, 90.0, 78.0], roll_no=101)
student2 = Student(name="Bob", age=22, grades=[88.0, 92.5], roll_no=102)
print(student1)
print(student1.average_grade())
print(asdict(student2))
print(student1 == student2)  # False, different data




#Mixin reusable behaviour via multiple inheritance
class LogMixin:
    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")

class ValidateMixin:
    def validate(self,value,min_val=0,max_val=100):
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} out of range [{min_val}, {max_val}]")
        return value
    
class SerializeMixin:
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
class BankAccount(LogMixin, ValidateMixin, SerializeMixin):
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float):
        amount = self.validate(amount, min_val=1, max_val=100_000)
        self.balance += amount
        self.log(f"Deposited ₹{amount}. New balance: ₹{self.balance}")

    def withdraw(self, amount: float):
        amount = self.validate(amount, min_val=1, max_val=self.balance)
        self.balance -= amount
        self.log(f"Withdrew ₹{amount}. New balance: ₹{self.balance}")



acc = BankAccount("Ravi", 5000)
acc.deposit(2000)
acc.withdraw(1000)
print(acc.to_dict())  

#MRO resolution order
print(BankAccount.__mro__)



#operator overloading

class Vector:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:              # magnitude
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2)       
print(v1 - v2)    
print(v1 * 3)           
print(abs(v1)) 




#design patterns
#singleton pattern
class databaseConnection:
    _instance = None

    def __new__(cls,*args,**kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connected = False
        return cls._instance
    
    def connect(self, url: str):
        if not self._connected:
            self._url = url
            self._connected = True
            print(f"Connected to {url}")
        else:
            print("Already connected!")
db1 = databaseConnection()
db2 = databaseConnection()  
print(db1 is db2)  # True, both are the same instance
db1.connect("localhost:5432/mydb")
db2.connect("localhost:5432/otherdb")  # Still connected to the first URL





#factory pattern
class Notification(ABC):
    @abstractmethod
    def send(self, message: str):
        pass
class EmailNotification(Notification):
    def __init__(self, email: str):
        self.email = email
    def send(self, message: str):
        print(f"Sending email to {self.email}: {message}")

class SMSNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone
    def send(self, message: str):
        print(f"Sending SMS to {self.phone}: {message}")

class WhatsappNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone
    def send(self, message: str):
        print(f"Sending WhatsApp message to {self.phone}: {message}")
class NotificationFactory:
    _register = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "whatsapp": WhatsappNotification
    }
    @classmethod
    def create(cls, type_: str, contact: str) -> Notification:
        klass = cls._register.get(type_.lower())
        if not klass:
            raise ValueError(f"Unknown notification type: {type_}")
        return klass(contact)

    @classmethod
    def register(cls, type_: str, klass):  # extensible
        cls._registry[type_] = klass

n1 = NotificationFactory.create("email", "dev@example.com")
n2 = NotificationFactory.create("sms", "+91-9999999999")
n3 = NotificationFactory.create("whatsapp", "+91-9999999999")
n1.send("Your OTP is 4821")
n2.send("Your OTP is 4821")




# observer pattern
from typing import Callable

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

class UserService:
    def __init__(self):
        self.events = EventEmitter()

    def register(self, username: str):
        print(f"User '{username}' registered.")
        self.events.emit("user_registered", username=username)

svc = UserService()
svc.events.on("user_registered",
    lambda username: print(f"Sending welcome email to {username}"))
svc.events.on("user_registered",
    lambda username: print(f"Creating profile for {username}"))

svc.register("alice")




#decorator pattern
class Coffee:
    def cost(self): return 50
    def description(self): return "Coffee"

class MilkDecorator:
    def __init__(self, coffee): self._coffee = coffee
    def cost(self): return self._coffee.cost() + 15
    def description(self): return self._coffee.description() + " + Milk"

class SugarDecorator:
    def __init__(self, coffee): self._coffee = coffee
    def cost(self): return self._coffee.cost() + 5
    def description(self): return self._coffee.description() + " + Sugar"

drink = SugarDecorator(MilkDecorator(Coffee()))
print(drink.description())   # Coffee + Milk + Sugar
print(f"₹{drink.cost()}") 





#data structure 
#stack using list

class Stack:
    def __init__(self):
        self._data = []
    def push(self, item):
        self._data.append(item)
    def pop(self):
        if not self._data:
            raise IndexError("Stack is empty")
        return self._data.pop()
    def peek(self):
        if not self._data:
            raise IndexError("Stack is empty")
        return self._data[-1]
    def is_empty(self):
        return len(self._data) == 0
    def __len__(self):
        return len(self._data)
    def __repr__(self):
        return f"Stack({self._data})"

# Stack use-case: balanced parentheses checker
def is_balanced(expr: str) -> bool:
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in expr:
        if ch in '([{':
            stack.push(ch)
        elif ch in ')]}':
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()
print(is_balanced("({[]})"))  # True
print(is_balanced("({[})"))   # False




from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item): self._data.append(item)
    def dequeue(self): return self._data.popleft() if self._data else None
    def front(self): return self._data[0] if self._data else None
    def is_empty(self): return len(self._data) == 0
    def __len__(self): return len(self._data)
    def __repr__(self): return f"Queue({list(self._data)})"

q = Queue()
for task in ["task1", "task2", "task3"]:
    q.enqueue(task)
print(q.dequeue())


#linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        if not self.head: return
        if self.head.data == data:
            self.head = self.head.next
            return
        curr = self.head
        while curr.next and curr.next.data != data:
            curr = curr.next
        if curr.next:
            curr.next = curr.next.next

    def reverse(self):
        prev, curr = None, self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def to_list(self):
        result, curr = [], self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

ll = LinkedList()
for v in [1, 2, 3, 4, 5]:
    ll.append(v)
ll.reverse()
print(ll.to_list())