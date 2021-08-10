from typing import Iterable
from nonebot import Bot
from nonebot.adapters.cqhttp import Event
from nonebot.rule import Rule
from nonebot.adapters.cqhttp.event import GroupMessageEvent, PrivateMessageEvent


def not_to_me() -> Rule:
    async def _not_to_me(bot: Bot, event: Event, state: dict) -> bool:
        return isinstance(event, GroupMessageEvent) and event.sub_type == "normal"

    return Rule(_not_to_me)


def allow_all() -> Rule:
    async def _allow_all(bot: Bot, event: Event, state: dict) -> bool:
        return True
    return Rule(_allow_all)

def private_call() -> Rule:
    async def _private_call(bot: Bot, event: Event, state: dict) -> bool:
        return isinstance(event, PrivateMessageEvent)
    return Rule(_private_call)