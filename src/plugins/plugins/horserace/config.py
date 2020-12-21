from typing import Dict, Tuple, Set

from pydantic import BaseSettings


class Config(BaseSettings):
    horse_num: int = 5
    slide_length: int = 15
    horse_char: str = "🐎"
    odd: Dict[int, float] = {1: 1.5, 2: 0.3, 3: 0.15}
    help_count: int = 6
    help_money: int = 20
    slide: str = "Ξ"
    stud_list: Set[str] = {"梭哈", "全压了"}
    money_unit: str = "$"

    class Config:
        extra = "ignore"
