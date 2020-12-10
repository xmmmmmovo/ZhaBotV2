from nonebot import get_driver, on_command, logger, require
from nonebot.adapters.cqhttp import Bot, Event

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("src.plugins.permission").NOT_ANONYMOUS_GROUP
select_one = require("src.plugins.mysql").select_one
op_sql = require("src.plugins.mysql").op_sql

check_in = on_command("签到", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=3)


@check_in.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    str_msg = str(event.message).strip()
    if str_msg:
        await check_in.finish()
    if await select_one():
        pass
    else:
        pass
