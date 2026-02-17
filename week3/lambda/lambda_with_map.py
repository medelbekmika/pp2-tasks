# 1
numbers = [1, 2, 3, 4]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)

# 2
names = ["anna", "ivan", "petr"]
upper_names = list(map(lambda x: x.upper(), names))
print(upper_names)

# 3
numbers = [1, 2, 3]
plus_ten = list(map(lambda x: x + 10, numbers))
print(plus_ten)

# 4
words = ["hi", "hello", "bye"]
lengths = list(map(lambda x: len(x), words))
print(lengths)

# 5
nums1 = [1, 2, 3]
nums2 = [4, 5, 6]
sum_lists = list(map(lambda x, y: x + y, nums1, nums2))
print(sum_lists)
