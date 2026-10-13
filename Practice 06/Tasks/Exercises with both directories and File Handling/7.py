with open("source.txt", "r") as source:
    content = source.read()

with open("destination.txt", "w") as destination:
    destination.write(content)