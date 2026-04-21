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