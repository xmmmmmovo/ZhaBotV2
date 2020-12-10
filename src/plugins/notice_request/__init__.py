from nonebot import get_driver, on_request, on_notice
from nonebot.adapters.cqhttp import Bot, Event

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

request_handler = on_request()


@request_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if config.request_on:
        flag = str(event.id)
        if event.type == "friend":
            await bot.set_friend_add_request(flag=flag, approve=True)
        elif event.type == "group":
            await bot.set_group_add_request(flag=flag, sub_type=event.sub_type, approve=True)
