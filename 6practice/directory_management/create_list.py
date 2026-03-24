#1
with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")
with open("demofile.txt") as f:
  print(f.read())
#2
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
with open("demofile.txt") as f:
  print(f.read())
#3
f = open("myfile.txt", "x")
#4
f = open("book.txt", "r")
#5
with open("book.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
with open("book.txt") as f:
  print(f.read())
