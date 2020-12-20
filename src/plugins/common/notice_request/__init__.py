from nonebot import get_driver, on_request, on_notice, get_loaded_plugins
from nonebot.adapters.cqhttp import Bot, Event

from .config import Config
from .data_source import insert_qq_group, delete_qq_group

global_config = get_driver().config
config = Config(**global_config.dict())

request_handler = on_request()
notice_handler = on_notice()


@request_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if config.request_on:
        flag = str(event.id)
        if event.type == "friend":
            await bot.set_friend_add_request(flag=flag, approve=True)
        elif event.type == "group":
            plugins = get_loaded_plugins()
            template = dict.fromkeys(map(lambda x: x.name, plugins), False)
            succ = await insert_qq_group(event.group_id, template)
            await bot.set_group_add_request(flag=flag, sub_type=event.sub_type, approve=succ)


@notice_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if event.type == "group_decrease" and \
            (event.type == "kick_me" or event.type == "leave"):
        succ = await delete_qq_group(event.group_id)
