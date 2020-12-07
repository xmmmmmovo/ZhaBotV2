from nonebot import on_command, Bot
from nonebot.adapters.cqhttp import Event
from nonebot.permission import Permission

from src.common.rules import not_to_me

echo = on_command("echo", rule=not_to_me(), permission=Permission(), priority=5)


@echo.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    echo.finish(event.message)
