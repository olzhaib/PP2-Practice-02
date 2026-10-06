import re

text = "abbb"

result = re.fullmatch(r"ab*", text)

print(result)