# 1
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof!")

# 2
class Vehicle:
    def move(self):
        print("Vehicle moving")

class Bike(Vehicle):
    def move(self):
        print("Bike riding")

# 3
class Person:
    def role(self):
        print("Person")

class Teacher(Person):
    def role(self):
        print("Teacher")

# 4
class Shape:
    def draw(self):
        print("Drawing shape")

class Circle(Shape):
    def draw(self):
        print("Drawing circle")

# 5
class Employee:
    def work(self):
        print("Working")

class Developer(Employee):
    def work(self):
        print("Coding")
