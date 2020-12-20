from nonebot import get_driver, on_command, Bot, require, get_loaded_plugins, logger
from nonebot.adapters.cqhttp import Event
from nonebot.permission import SUPERUSER

from ujson import dumps

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

op_sql = require("mysql").op_sql

restart = on_command("restart", rule=not_to_me(), permission=SUPERUSER, priority=97)
reset_group_status = on_command("reset_group", rule=not_to_me(), permission=SUPERUSER, priority=97)


@restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    await bot.set_restart()
    await restart.finish("已重连")


@reset_group_status.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    plugins = get_loaded_plugins()
    template = dict.fromkeys(map(lambda x: x.name, plugins), False)
    logger.debug(template)
    succ = await op_sql("update `qq_group` set plugin_status = %s", (dumps(template)))
    await reset_group_status.finish("重置成功" if succ else "重置失败")
