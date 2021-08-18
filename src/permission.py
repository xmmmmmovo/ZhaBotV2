from nonebot.log import logger
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent, Message, MessageSegment
from nonebot.adapters.cqhttp.permission import Permission

from src.db import admin_collection, plugin_collection
from src.model.plugin import find_plugin_model


def Admin() -> Permission:
    async def __permission(bot: Bot, event: Event) -> bool:
        if not isinstance(event, GroupMessageEvent):
            return False
        group = await admin_collection.find_one({"group_id": event.group_id})
        if group is None:
            return False
        if str(event.sender.user_id) in group["qqlist"]:
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
