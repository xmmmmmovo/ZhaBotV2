from nonebot import get_driver, on_request, on_notice
from nonebot.adapters.cqhttp import Bot, Event

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

request_handler = on_request()
notice_handler = on_notice()


@request_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if config.request_on:
        pass
    pass


@notice_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if config.notice_on:
        pass
    pass
