from nonebot.permission import Permission
from nonebot.plugin import Export

from src.permission import Auth


def init_plugin(export: Export, plugin: str, name: str, description: str) -> Auth:
    export.name = name
    export.description = description
    return Auth(plugin)
