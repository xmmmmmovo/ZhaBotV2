from nonebot import on_command, logger, export
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.permission import Permission

from src.common.rules import not_to_me
from .data_source import fetch_hitokoto_str

hitokoto = on_command("一言", rule=not_to_me(), permission=Permission(), priority=10)
export().fetch_hitokoto_str = fetch_hitokoto_str


@hitokoto.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    await hitokoto.finish(await fetch_hitokoto_str())
