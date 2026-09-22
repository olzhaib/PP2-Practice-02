import math

def volume(radius):
    return (4 / 3) * math.pi * radius ** 3

radius = float(input())
print(volume(radius))