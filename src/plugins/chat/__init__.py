from nonebot import get_driver, on_command, Bot
from nonebot.adapters.cqhttp import Event
from nonebot.permission import Permission
from nonebot.rule import to_me

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

chat = on_command("", rule=to_me(), permission=Permission(), priority=12)


@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if not args:
        await chat.finish("昂，怎么了吗")
