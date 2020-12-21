from typing import Dict

from nonebot.adapters.cqhttp import MessageSegment
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    house_num = 5
    slide_length = 15
    house_char = "🐎"
    odd: Dict[int, float] = {1: 1.5, 2: 0.3, 3: 0.15}
    help_count = 6
    help_money = 20
    slide = "Ξ"
    stud_list = {"梭哈", "全压了"}
    money_unit = ""

    class Config:
        extra = "ignore"
