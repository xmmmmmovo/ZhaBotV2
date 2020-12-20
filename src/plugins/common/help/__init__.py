from nonebot import get_driver, on_command, get_loaded_plugins
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER

from src.common.rules import not_to_me
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

help = on_command("help", aliases={"帮助"}, rule=not_to_me(), permission=SUPERUSER, priority=98)

__name__ = "帮助"


@help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    plugins = get_loaded_plugins()
    await help.finish('\n'.join(f"{k + 1}: {v.name}" for k, v in enumerate(plugins)))
