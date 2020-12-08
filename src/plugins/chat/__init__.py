from nonebot import get_driver, on_command
from nonebot.permission import Permission
from nonebot.rule import to_me

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

echo = on_command("", rule=to_me(), permission=Permission(), priority=12)

