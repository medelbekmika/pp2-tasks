#1
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("Names:", names)
print("Scores:", scores)
print("\nUsing enumerate:")

for index, name in enumerate(names):
    print(index, name)
print("\nEnumerate starting from 1:")
for index, name in enumerate(names, start=1):
    print(index, name)
#2
print("\nUsing zip:")

for name, score in zip(names, scores):
    print(name, score)
#3
student_dict = dict(zip(names, scores))
print("\nDictionary:", student_dict)
#4
print("\nEnumerate + zip:")

for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{i}. {name} scored {score}")
#5
pairs = [("A", 1), ("B", 2), ("C", 3)]
letters, numbers = zip(*pairs)

print("\nUnzipped:")
print("Letters:", letters)
print("Numbers:", numbers)
