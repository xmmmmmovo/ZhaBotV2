from dataclasses import dataclass
from typing import List, Dict

from nonebot import require

op_sql = require("mysql").op_sql
select_one = require("mysql").select_one
select_all = require("mysql").select_all
insert_many = require("mysql").insert_many


@dataclass
class Record:
    tools: List
    horses: List
    slides: List
    user_list: Dict[str, List]
    rank: Dict[int, int]
    is_start: bool


records: Dict[str, Record] = {}

start_head = """赛马(beta0.1)
押这只马人数<=押其他马人数+1时：
奖励=赔率x下注金额
押这只马人数>押其他马人数+1时：
奖励=[100%+(赔率-100%)x（押其它马的人数/押马总人数）]x下注金额
输入 押马 x,y（x为数字，y为押金，如：押马 1,2）来选择您觉得会胜出的马，一人只能押一只
输入 开始赛马 开始比赛
注意：开始比赛后不能再选马
注意：只有前三只到达终点的马会根据名次获得获胜奖励（排名并列的情况下可能超过三只）
"""


async def reset_help_count(count) -> bool:
    return op_sql("update house_race_player_table set help_count=%s",
                  (count))


async def select_user_order_by_money(group_id):
    return await select_all("select * from user "
                            "where qq_group_id = %s "
                            "order by money desc", (group_id))


async def select_one_help_count_by_qq(qq):
    return await select_one("select help_count from house_race_player_table "
                            "where qq = %s", (qq))


async def insert_help_count(qq, count):
    return await op_sql("insert into house_race_player_table(qq, help_count) "
                        "values (%s, %s)", (qq, count))


async def decrease_help_count(qq):
    return await op_sql("update house_race_player_table set help_count = help_count - 1 "
                        "where qq = %s", (qq))
