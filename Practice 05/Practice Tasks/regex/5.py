import re

text = "a12345b"

result = re.fullmatch(r"a.*b", text)

print(result)