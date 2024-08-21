"""
信息添加中间件
"""
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.message import run_preprocessor
from nonebot.matcher import Matcher
from src.db import user_collection, group_collection
from src.db.model.user import find_user_model, new_user_model
from src.db.model.group import find_group_model, new_group_model

@run_preprocessor
async def model_ensurance(matcher: Matcher, event: Event):
    if isinstance(event, GroupMessageEvent):
        res = await user_collection.find_one(find_user_model(event.user_id, event.group_id))
        if res is None:
            res = new_user_model(
                event.user_id, event.group_id, float(0.0), False, 0)
            await user_collection.insert_one(res)
        matcher.set_arg("user", res)

        res = await group_collection.find_one(find_group_model(event.group_id))
        if res is None:
            res = new_group_model(event.group_id)
            await group_collection.insert_one(res)
        matcher.set_arg("group", res)
    return
