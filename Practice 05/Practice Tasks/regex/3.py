import re

text = "hello_world test_text Hello_world"

result = re.findall(r"[a-z]+_[a-z]+", text)

print(result)