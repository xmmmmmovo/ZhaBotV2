from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
    Message,
    MessageSegment,
    message,
)
from nonebot.permission import Permission

from src.db import admin_collection, plugin_collection
from src.db.model.plugin import find_plugin_model


# deprecated
def Admin() -> Permission:
    async def __permission(bot: Bot, event: Event) -> bool:
        if not isinstance(event, GroupMessageEvent):
            return False
        group = await admin_collection.find_one({"group_id": event.group_id})
        if group is None:
            return False
        if str(event.sender.user_id) in group["qqlist"] or event.sender.role in {
            "owner",
            "admin",
        }:
            return True
        return False

    return Permission(__permission)


class Auth:
    plugin_name = ""

    def __init__(self, plugin_name) -> None:
        self.plugin_name = plugin_name
        return

    def auth_permission(self, perm: Permission = Permission()) -> Permission:
        plugin_name = self.plugin_name

        async def __permission(bot: Bot, event: Event) -> bool:
            if not isinstance(event, GroupMessageEvent):
                return await perm(bot, event)
            group_id = event.group_id

            plugins = await find_plugin_model(group_id)
            if plugins is not None and bool(plugins.get(plugin_name)):
                return await perm(bot, event)
            return False

        return Permission(__permission)

    def admin_auth_permission(self, perm: Permission = Admin()):
        plugin_name = self.plugin_name

        async def __permission(bot: Bot, event: Event) -> bool:
            if not isinstance(event, GroupMessageEvent):
                return await perm(bot, event)
            group_id = event.group_id

            plugins = await find_plugin_model(group_id)
            if plugins is not None and bool(plugins.get(plugin_name)):
                return await perm(bot, event)
            return False

        return Permission(__permission)
