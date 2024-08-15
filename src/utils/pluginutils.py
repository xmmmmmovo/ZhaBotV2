from nonebot.adapters.onebot.v11 import Bot

from aiocache import Cache, cached

@cached(ttl=600, cache=Cache.MEMORY)
async def get_group_member_list_cached(bot: Bot, group_id: int):
    return await bot.get_group_member_list(group_id=group_id)
