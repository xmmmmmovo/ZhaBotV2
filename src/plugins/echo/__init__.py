from nonebot import on_command, logger
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.permission import Permission

from src.common.rules import not_to_me

echo = on_command("echo", rule=not_to_me(), permission=Permission(), priority=4)


@echo.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    logger.debug(event.message)
    await echo.finish(event.message)
