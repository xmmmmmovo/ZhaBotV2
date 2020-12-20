from nonebot import get_driver, on_command, logger, require
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("permission").NOT_ANONYMOUS_GROUP
fetch_user_money_status = require("dao").fetch_user_money_status
insert_user = require("dao").insert_user

my_money = on_command("money", aliases={"我的资产", "我的财产", "余额"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP,
                      priority=97)


@my_money.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    data = await fetch_user_money_status(event.user_id, event.group_id)
    if data == None:
        succ = await insert_user(event.user_id, event.group_id, 0, int(False))
        if not succ:
            await my_money.finish("获取数据失败！请联系管理员！")
        await my_money.finish(MessageSegment.at(event.user_id) + f"您当前的资产为：{0}{config.money_unit}")
    else:
        await my_money.finish(MessageSegment.at(event.user_id) + f"您当前的资产为：{data['money']}{config.money_unit}")
