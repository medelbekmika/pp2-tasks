#1
f = open("demofile.txt")
print(f.read())
#2
f = open("D:\\myfiles\welcome.txt")
print(f.read())
#3
f = open("demofile.txt")
print(f.readline())
f.close()
#4
with open("demofile.txt") as f:
  print(f.read(5))
#5
with open("demofile.txt") as f:
  print(f.readline())
  
