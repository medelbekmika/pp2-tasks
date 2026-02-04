#1
def my_function():
  print("Hello World")
#2
def my_function():
  print("Hello World")

my_function()
#3
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)
#4
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))
#5
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)
