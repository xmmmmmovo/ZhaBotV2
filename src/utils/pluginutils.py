from nonebot.adapters.onebot.v11 import Bot
from nonebot.permission import Permission
from nonebot.plugin import Export

from aiocache import Cache, cached

from src.permission import Auth


def init_plugin(export: Export, plugin: str, name: str, description: str) -> Auth:
    export.name = name
    export.description = description
    return Auth(plugin)


@cached(ttl=600, cache=Cache.MEMORY)
async def get_group_member_list_cached(bot: Bot, group_id: int):
    return await bot.get_group_member_list(group_id=group_id)
