from nonebot import get_driver, export
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import Permission
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


def GROUP(*groups: int, perm: Permission = Permission()):
    """
    :说明:

      在白名单内且满足 perm

    :参数:

      * ``*groups: int``: 白名单
      * ``perm: Permission``: 需要同时满足的权限
    """

    async def _group(bot: Bot, event: Event) -> bool:
        return event.type == "message" and event.group_id in groups and await perm(
            bot, event)

    return Permission(_group)


async def _not_anonymous_group(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "group" and
            event.sub_type == "normal")


NOT_ANONYMOUS_GROUP = Permission(_not_anonymous_group)

export().GROUP = GROUP
export().NOT_ANONYMOUS_GROUP = NOT_ANONYMOUS_GROUP
