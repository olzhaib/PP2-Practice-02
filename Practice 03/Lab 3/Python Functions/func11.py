def palindrome(word):
    return word == word[::-1]


word = input()

print(palindrome(word))