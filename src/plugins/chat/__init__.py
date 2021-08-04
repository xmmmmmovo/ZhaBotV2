# import nonebot
import xmlrpc.client
from src.rules import allow_all

from src.imports import *
from src.utils.msgutils import message_to_text
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("chat")
export().name = "聊天"
export().description = "聊天捏"

chat = on_message(rule=to_me(), permission=auth, priority=100)
train = on_message(rule=allow_all(), permission=Permission(), priority=999)

# chat_bot = ChatBot(
#     '小扎',
#     storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
#     logic_adapters=[
#         'chatterbot.logic.BestMatch'
#     ],
#     database_uri=f'{config.mongo_url}/chat'
# )

# trainer = ListTrainer(chat_bot)

server = xmlrpc.client.ServerProxy(config.rpc_url)


@train.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    msg = message_to_text(event.get_message())
    if msg != "":
        server.train(msg)
    await train.finish()


@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    msgs = message_to_text(event.get_message())
    if not msgs:
        await chat.finish("昂，怎么了嘛")
    elif msgs in {"在嘛", "在吗"}:
        await chat.finish("在的呢")

    resp = server.chat(msgs)

    if resp == "":
        await chat.finish("小扎还没学到呢")
    await chat.send(resp)
    server.train(msgs)
    await chat.finish()
