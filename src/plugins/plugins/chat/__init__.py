from nonebot import get_driver, on_command, on_message, logger
from nonebot.adapters.cqhttp import Event, Bot, MessageSegment, Message
from nonebot.permission import Permission
from nonebot.rule import to_me

from .config import Config
from .data_source import call_tencent_api
from src.common.rules import not_to_me, not_to_me_but_keywords

global_config = get_driver().config
config = Config(**global_config.dict())

chat = on_message(rule=not_to_me_but_keywords(config.nickname), permission=Permission(), priority=99)


@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    msgs = event.message
    logger.debug(msgs)
    str_msg = str(msgs).strip()
    if not str_msg:
        await chat.finish("昂，怎么了吗")
    elif str_msg == "在嘛":
        await chat.finish("在的呢亲亲")
    logger.debug(event.sender)
    content = ""
    for msg in msgs:
        if msg.type == "text":
            content += str(msg).strip()
        elif msg.type == "face":
            content += ""
        else:
            content += ""

    resp = await call_tencent_api(event.sender["user_id"], content,
                                  config.app_id, config.app_key)
    if resp is None or resp["ret"] != 0:
        await chat.finish("小扎好像听不懂呢~")
    else:
        smsg = Message()
        if event.sub_type == "normal":
            smsg.append(MessageSegment.at(event.sender.get("user_id")))
        smsg.append(resp['data']['answer'])
        await chat.finish(smsg)
