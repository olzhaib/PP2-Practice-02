with open("sample.txt", "a") as file:
    file.write("\nNew line added.")

with open("sample.txt", "r") as file:
    print(file.read())