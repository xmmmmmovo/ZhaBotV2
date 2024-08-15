# import nonebot
from src.imports import *
from src.utils.msgutils import message_to_text
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

__plugin_meta__ = PluginMetadata(
    name="chat",
    description="聊天插件",
    usage="没什么用",
    type="application",
    config=Config,
    extra={},
)

auth = Auth("chat")
simple = auth.auth_permission()

chat = on_message(rule=to_me(), permission=simple, priority=15)

@chat.handle()
async def handle_first_receive(event: GroupMessageEvent):
    message = message_to_text(event.get_message())

    if not message:
        await chat.finish("昂，怎么了嘛")
    elif message in {"在嘛", "在吗"}:
        await chat.finish("在的呢")

    return
