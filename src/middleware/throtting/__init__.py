"""
节流中间件
"""
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.message import run_preprocessor
from nonebot.matcher import Matcher
from nonebot.typing import T_State

@run_preprocessor
async def throtting(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    return
