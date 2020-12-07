from nonebot import Bot
from nonebot.adapters.cqhttp import Event
from nonebot.rule import Rule


def not_to_me() -> Rule:
    async def _not_to_me(bot: Bot, event: Event, state: dict) -> bool:
        return True

    return Rule(_not_to_me)
