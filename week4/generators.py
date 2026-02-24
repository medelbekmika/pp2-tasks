#1
n=int(input())
def squares(n):
    for i in range(n+1):
        yield i**2

for sq in squares(n):
    print(sq)

#2
n=int(input())
def even_numbers(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

print(",".join(str(num) for num in even_numbers(n)))

#3
n=int(input())
def div_numbers(n):
    for i in range(n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for num in div_numbers(n+1):
    print(num)

#4
a,b=map(int,input().split())

def square_numbers(a , b):
    for i in range(a,b+1):
        yield i**2

for num in square_numbers(a,b):
    print(num)

#5
n=int(input())

def down_numbers(n):
    for i in range(n,-1,-1):
        yield i

for num in down_numbers(n):
    print(num)
