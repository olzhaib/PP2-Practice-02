for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    with open(letter + ".txt", "w") as file:
        file.write("This is file " + letter)