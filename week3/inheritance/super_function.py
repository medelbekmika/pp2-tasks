# 1
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

# 2
class Vehicle:
    def start(self):
        print("Starting vehicle")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car ready")

# 3
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        super().greet()
        print("I am a student")

# 4
class A:
    def method(self):
        print("A method")

class B(A):
    def method(self):
        super().method()
        print("B method")

# 5
class Shape:
    def __init__(self, color):
        self.color = color

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
