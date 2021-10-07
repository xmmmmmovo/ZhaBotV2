from typing import List


def swap(a: List[int]):
    a[0], a[1] = a[1], a[0]

aa = [1, 2, 3]

print(aa)
swap(aa)
print(aa)