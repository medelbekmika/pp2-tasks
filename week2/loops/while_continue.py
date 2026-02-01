#1
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue 
    print(i)
#2
i = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    print(i)
#3
i = 0
while i < 5:
    i += 1
    if i == 2 or i == 4:
        continue
    print(i)
#4
i = int(input())
while i > 0:
  print(i)
  i+=1
#5
i = 0
while i < 10:
    i += 1
    if i == 3:
        continue 
    if i == 6:
        break 
    print(i)

