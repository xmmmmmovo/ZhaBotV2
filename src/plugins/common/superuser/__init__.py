from nonebot import get_driver, on_command, Bot
from nonebot.adapters.cqhttp import Event
from nonebot.permission import SUPERUSER

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

restart = on_command("restart", rule=not_to_me(), permission=SUPERUSER, priority=2)


@restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    bot.set_restart()
