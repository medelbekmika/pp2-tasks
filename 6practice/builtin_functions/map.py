#1
nums = [1, 2, 3, 4]
result = list(map(lambda x: x * 2, nums))
print(result)
#2
nums = [1, 2, 3, 4, 5, 6]
result = list(filter(lambda x: x % 2 != 0, nums))
print(result) 
#3
from functools import reduce
nums = [1, 2, 3, 4]
result = reduce(lambda x, y: x * y, nums)
print(result) 
#4
names = ["alice", "bob", "charlie"]
result = list(map(str.upper, names))
print(result) 
#5
from functools import reduce
nums = [-2, 3, -1, 5, 4]
result = reduce(
    lambda x, y: x + y,
    filter(lambda x: x > 0, nums)
)
print(result) 
