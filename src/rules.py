from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent, PokeNotifyEvent
from nonebot.typing import T_State


def not_to_me() -> Rule:
    async def _not_to_me(bot: Bot, event: Event, state: T_State) -> bool:
        return isinstance(event, GroupMessageEvent) and event.sub_type == "normal"

    return Rule(_not_to_me)


def allow_all() -> Rule:
    async def _allow_all(bot: Bot, event: Event, state: T_State) -> bool:
        return True
    return Rule(_allow_all)


def private_call() -> Rule:
    async def _private_call(bot: Bot, event: Event, state: T_State) -> bool:
        return isinstance(event, PrivateMessageEvent)
    return Rule(_private_call)


def poke():
    async def _poke(bot: Bot, event: Event, state: T_State) -> bool:
        return (isinstance(event, PrivateMessageEvent) and
                event.sub_type == "friend" and event.message[0].type == "poke")
    return Rule(_poke)


def group_poke():
    async def _group_poke(bot: Bot, event: Event, state: T_State) -> bool:
        return isinstance(event, PokeNotifyEvent) and event.is_tome()
    return Rule(_group_poke)
