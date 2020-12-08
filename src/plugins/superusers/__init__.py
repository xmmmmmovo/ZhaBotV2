from nonebot import get_driver, on_command, get_bots, logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

superuser = on_command("test", rule=not_to_me(), permission=SUPERUSER, priority=98)


@superuser.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    logger.debug(get_bots())
    pass
