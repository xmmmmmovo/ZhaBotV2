from random import randint
from collections import Counter

res = []

for i in range(10000):
    res.append(randint(0, 5))

print(Counter(res))
