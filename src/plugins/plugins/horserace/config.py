from typing import Dict

from nonebot.adapters.cqhttp import MessageSegment
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    house_num = 5
    slide_length = 15
    house_char = "[CQ:emoji,id=128014]"
    odd: Dict[int, float] = {1: 1.5, 2: 0.3, 3: 0.15}
    help_count = 8

    class Config:
        extra = "ignore"
