from dataclasses import dataclass
from random import shuffle
from typing import Dict, List

from nonebot import get_driver, on_command, require, logger
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.permission import GROUP

from src.common.rules import not_to_me
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


@dataclass
class Record:
    idx: int
    bullet: List[bool]


record: Dict[int, Record] = {}

NOT_ANONYMOUS_GROUP = require("permission").NOT_ANONYMOUS_GROUP
fetch_user_money_status = require("economic").fetch_user_money_status
increase_user_money = require("economic").increase_user_money
insert_user = require("dao").insert_user

start = on_command("gun", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=8)
slot = on_command("ping", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=8)


@start.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    st = record.get(event.group_id)
    if st is None:
        lst = [True, False, False, False, False, False]
        shuffle(lst)
        record[event.group_id] = Record(0, lst)
        logger.debug(record[event.group_id])
        await start.finish("已开始俄罗斯轮盘~")


@slot.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    st: Record = record.get(event.group_id)
    if st:
        if st.bullet[st.idx]:
            record.pop(event.group_id)
            await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
            await slot.finish("pong！" + str(MessageSegment.face(169)))
        st.idx += 1
        money = await fetch_user_money_status(event.user_id, event.group_id)
        if money is None:
            await insert_user(event.user_id, event.group_id, 0, int(False))
            money = 0
        else:
            money = float(money["money"])
        await increase_user_money(event.user_id, event.group_id, money + 10)
        await slot.finish("pa~ 金钱+10~")
    else:
        await slot.finish("本轮已结束，请'。gun'重新开始")
