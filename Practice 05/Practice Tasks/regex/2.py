import re

text = "abb"

result = re.fullmatch(r"ab{2,3}", text)

print(result)