#1
import shutil
source = "path/to/source/file.txt"
destination = "path/to/destination/file.txt"
shutil.move(source, destination)
#2
import shutil
shutil.move("file.txt", "folder/")
#3
import shutil
import os
files = ["a.txt", "b.txt", "c.txt"]
for file in files:
    shutil.move(file, "destination_folder/")
#4
import shutil
import os
source_dir = "source_folder"
dest_dir = "destination_folder"
for filename in os.listdir(source_dir):
    full_path = os.path.join(source_dir, filename)
    if os.path.isfile(full_path):
        shutil.move(full_path, dest_dir)
#5
import os
import shutil

os.makedirs("destination_folder", exist_ok=True)
shutil.move("file.txt", "destination_folder/")
