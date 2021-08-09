from typing import Iterable

from nonebot import logger

from src.db import plugin_collection


async def find_plugin_model(group_id):
    return await plugin_collection.find_one({
        "group_id": int(group_id)
    })


async def update_plugin_model(group_id: int, plugins: Iterable[str], status: bool):
    return await plugin_collection.update_one({
        "group_id": int(group_id)
    }, {
        "$set": {
            key: status for key in plugins
        }
    },upsert=True)
