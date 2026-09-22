from itertools import permutations

def print_permutations(string):
    for p in permutations(string):
        print(''.join(p))

string = input()
print_permutations(string)