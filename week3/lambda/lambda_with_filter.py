# 1
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

# 2
numbers = [-2, -1, 0, 1, 2]
positives = list(filter(lambda x: x > 0, numbers))
print(positives)

# 3
words = ["apple", "banana", "kiwi"]
long_words = list(filter(lambda x: len(x) > 4, words))
print(long_words)

# 4
names = ["Anna", "", "Ivan", ""]
non_empty = list(filter(lambda x: x != "", names))
print(non_empty)

# 5
numbers = [10, 15, 20, 25]
divisible_by_5 = list(filter(lambda x: x % 5 == 0, numbers))
print(divisible_by_5)
