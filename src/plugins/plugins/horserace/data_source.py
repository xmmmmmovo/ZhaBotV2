from dataclasses import dataclass
from typing import List, Dict

from nonebot import require

op_sql = require("mysql").op_sql
select_one = require("mysql").select_one
select_all = require("mysql").select_all
insert_many = require("mysql").insert_many


@dataclass
class Record:
    tool: List
    horses: List
    slides: List
    user_list: Dict[str, List]
    rank: Dict[int, int]
    is_start: bool


start_head = """赛马(beta0.1)
押这只马人数<=押其他马人数+1时：
奖励=赔率x下注金额
押这只马人数>押其他马人数+1时：
奖励=[100%+(赔率-100%)x（押其它马的人数/押马总人数）]x下注金额
"""

start_end = """输入 押马 x,y（x为数字，y为押金，如：押马 1,2）来选择您觉得会胜出的马，一人只能押一只
输入 开始赛马 开始比赛
注意：开始比赛后不能再选马
注意：只有前三只到达终点的马会根据名次获得获胜奖励（排名并列的情况下可能超过三只）
"""


async def reset_help_count(count) -> bool:
    return op_sql("update house_race_player_table set help_count=%s",
                  (count))
