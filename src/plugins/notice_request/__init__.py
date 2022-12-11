from typing import Union
from src.imports import *
from nonebot.adapters.onebot.v11.event import FriendRequestEvent, GroupRequestEvent

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

request_handler = on_request(block=True)
notice_handler = on_notice(block=True)


@request_handler.handle()
async def handle_first_receive(bot: Bot, event: Union[FriendRequestEvent, GroupRequestEvent]):
    if config.request_on:
        flag = event.flag
        if event.request_type == "friend":
            await event.approve(bot)
        elif event.request_type == "group" and event.sub_type == "invite":
            await event.approve(bot)


@notice_handler.handle()
async def handle_first_receive():
    pass
