#1
with open("demofile.txt", "a") as file:
  file.write("Now the file has more content!")
with open("demofile.txt") as file:
  print(file.read())
#2
with open("demofile.txt", "w") as file:
  file.write("Woops! I have deleted the content!")
with open("demofile.txt") as file:
  print(file.read())
#3
with open("example.txt", "w") as file:
    file.write("Hello, world!\n")
    file.write("This is a test file.")
#4
with open("example.txt", "a") as file:
    file.write("\nThis line is appended.")
#5
lines = ["First line\n", "Second line\n", "Third line\n"]
with open("example.txt", "w") as file:
    file.writelines(lines)
  
