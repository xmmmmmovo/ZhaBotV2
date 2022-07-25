from typing import Dict, Set

from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    horse_num: int = 7
    slide_length: int = 18
    horse_char: str = "🐎"
    odd: Dict[int, float] = {1: 1.5, 2: 0.15, 3: 0}
    slide: str = "Ξ"
    stud_list: Set[str] = {"梭哈", "全压了"}
    money_unit: str = "$"

    class Config:
        extra = "ignore"
