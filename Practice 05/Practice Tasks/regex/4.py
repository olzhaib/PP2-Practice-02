import re

text = "Hello World apple Python"

result = re.findall(r"[A-Z][a-z]+", text)

print(result)