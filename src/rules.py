from nonebot import Bot
from nonebot.adapters.cqhttp import Event
from nonebot.rule import Rule
from nonebot.adapters.cqhttp.event import GroupMessageEvent


def not_to_me() -> Rule:
    async def _not_to_me(bot: Bot, event: Event, state: dict) -> bool:
        return isinstance(event, GroupMessageEvent) and event.sub_type == "normal"

    return Rule(_not_to_me)
