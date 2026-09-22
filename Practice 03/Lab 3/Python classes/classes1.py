class String:
    def __init__(self):
        self.string = ""
    
    def getString(self):
        self.string = input()

    def printString(self):
        print(self.string.upper())

text = String()
text.getString()
text.printString()