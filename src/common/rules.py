from typing import Iterable

from nonebot import Bot
from nonebot.adapters.cqhttp import Event
from nonebot.rule import Rule


def not_to_me() -> Rule:
    async def _not_to_me(bot: Bot, event: Event, state: dict) -> bool:
        return True

    return Rule(_not_to_me)


def not_to_me_but_keywords(keywords: Iterable[str]) -> Rule:
    async def _not_to_me_but_keywords(bot: Bot, event: Event, state: dict) -> bool:
        str_msg = str(event.message).strip()
        return bool(event.to_me) or any(name in str_msg for name in keywords)

    return Rule(_not_to_me_but_keywords)
