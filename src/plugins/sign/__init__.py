from nonebot import get_driver, on_command, logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import GROUP

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

check_in = on_command("签到", rule=not_to_me(), permission=GROUP, priority=3)


@check_in.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    str_msg = str(event.message).strip()
    if str_msg:
        await check_in.finish()
    logger.info(event)
