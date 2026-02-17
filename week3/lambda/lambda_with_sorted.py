# 1
numbers = [5, 2, 9, 1]
sorted_numbers = sorted(numbers, key=lambda x: x)
print(sorted_numbers)

# 2
words = ["banana", "apple", "kiwi"]
sorted_by_length = sorted(words, key=lambda x: len(x))
print(sorted_by_length)

# 3
students = [("Anna", 85), ("Ivan", 92), ("Petr", 78)]
sorted_by_score = sorted(students, key=lambda x: x[1])
print(sorted_by_score)

# 4
numbers = [-10, 5, -3, 2]
sorted_by_absolute = sorted(numbers, key=lambda x: abs(x))
print(sorted_by_absolute)

# 5
people = [{"name": "Anna", "age": 25}, {"name": "Ivan", "age": 20}]
sorted_by_age = sorted(people, key=lambda x: x["age"])
print(sorted_by_age)
