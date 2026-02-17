# 1
class A:
    def method_a(self):
        print("Method A")

class B:
    def method_b(self):
        print("Method B")

class C(A, B):
    pass

# 2
class Fly:
    def fly(self):
        print("Flying")

class Swim:
    def swim(self):
        print("Swimming")

class Duck(Fly, Swim):
    pass

# 3
class Writer:
    def write(self):
        print("Writing")

class Speaker:
    def speak(self):
        print("Speaking")

class Author(Writer, Speaker):
    pass

# 4
class Father:
    def skill(self):
        print("Gardening")

class Mother:
    def talent(self):
        print("Cooking")

class Child(Father, Mother):
    pass

# 5
class Engine:
    def start(self):
        print("Engine start")

class Wheels:
    def roll(self):
        print("Rolling")

class Car(Engine, Wheels):
    pass
