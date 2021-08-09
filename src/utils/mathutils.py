from typing import Union


def rfloat(num: Union[float, int], d: int = 2):
    return round(float(num), d)
