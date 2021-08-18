from random import randint, choice
from collections import Counter

res = []

# for i in range(10000):
#     res.append(randint(0, 5))
#
# print(Counter(res))
horses = [11, 22, 33, 0, 43]
suffer_house = choice(
    list(filter(lambda x: x != -1, map(lambda x: -1 if x[1] == 0 else x[0], enumerate(horses)))))

# print(list(map(lambda x: -1 if x[1] == 0 else x[0], enumerate(horses))))
print(suffer_house)