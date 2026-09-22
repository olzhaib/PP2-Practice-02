def reverse_words(sentence):
    words = sentence.split()
    words.reverse()
    return " ".join(words)

sentence = input()
print(reverse_words(sentence))