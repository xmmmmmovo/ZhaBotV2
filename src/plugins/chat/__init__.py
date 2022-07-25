# import nonebot
import xmlrpc.client
from src.rules import allow_all

from src.imports import *
from src.utils.msgutils import message_to_text
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("chat")
simple = auth.auth_permission()
export().name = "聊天"
export().description = "聊天捏"

chat = on_message(rule=to_me(), permission=simple, priority=100)


@chat.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    msgs = message_to_text(args)
    if not msgs:
        await chat.finish("昂，怎么了嘛")
    elif msgs in {"在嘛", "在吗"}:
        await chat.finish("在的呢")
    await chat.finish()
