#1
import os
os.remove("demofile.txt")
#2
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")
#3
import os
os.rmdir("myfolder")
#4
import shutil
shutil.copy("source.txt", "backup/source.txt")
#5
import shutil
shutil.copy2("source.txt", "destination.txt")
