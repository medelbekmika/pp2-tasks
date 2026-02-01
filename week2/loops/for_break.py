#1
for i in range(1, 10):
    if i == 4:
        print("Loop stopped at", i)
        break
    print(i)
#2
numbers = [1, 3, 5, 7, 9]
for num in numbers:
    if num == 5:
        print("Found 7, stopping loop")
        break
    print(num)
#3
for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            break  # stops inner loop
        print(i, j)
#4
for i in range(1, 6):
    if i == 3:
        break
    print(i)
#5
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
