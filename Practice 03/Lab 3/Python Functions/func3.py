#// x + y =35
#// x + 2y = 47
#// 35 - y = 47 -2y
#// 2y - y = 47 - 35
#// y = 12  y= 94/2 - 35

def solve(numheads, numlegs):
    rabbits = numlegs/2 - numheads
    chickens = numheads - rabbits
    return ("Chickens: ", chickens, "Rabbits: ", rabbits)

numheads = int(input())
numlegs = int(input())
print(solve(numheads, numlegs))