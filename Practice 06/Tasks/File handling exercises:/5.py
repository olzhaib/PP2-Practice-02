import os

if os.path.exists("sample.txt") and os.path.isfile("sample.txt"):
    os.remove("sample.txt")
    print("File deleted")
else:
    print("File does not exist")