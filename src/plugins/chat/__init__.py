# import nonebot
from src.rules import allow_all

from src.imports import *
from src.utils.msgutils import message_to_text
from .config import Config

from asyncer import asyncify
from revChatGPT.revChatGPT import Chatbot, generate_uuid

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("chat")
simple = auth.auth_permission()
export().name = "聊天"
export().description = "聊天捏"

c = {
    "Authorization": config.openai_api_key,
    "session_token": config.openai_session_token,
    "email": config.openai_email,
    "password": config.openai_password
}

chat = on_message(rule=to_me(), permission=simple, priority=15)
chatbot = Chatbot(c, conversation_id=None)
# chatbot.refresh_session()  # You need to log in on the first run

# https://neuhub.jd.com/market/api/483
# https://ai.baidu.com/unit/home#/home


class ChatSession:
    def __init__(self):
        self.reset_conversation()

    def reset_conversation(self):
        self.conversation_id = None
        self.parent_id = generate_uuid()

    def get_chat_response(self, message, output="text"):
        try:
            chatbot.conversation_id = self.conversation_id
            chatbot.parent_id = self.parent_id
            return chatbot.get_chat_response(message, output=output)
        finally:
            self.conversation_id = chatbot.conversation_id
            self.parent_id = chatbot.parent_id


sessions = {}


def to_message(group_id, msg):
    session = None

    if group_id not in sessions:
        session = ChatSession()
        sessions[group_id] = session
    else:
        session = sessions[group_id]

    if msg == "重置会话":
        session.reset_conversation()
        return "重置成功！"

    try:
        resp = chatbot.get_chat_response(msg)
    except Exception as e:
        chatbot.refresh_session()
        return "出现故障 正在重置！重复出现请使用'小扎重置会话'"
    return resp["message"]


@chat.handle()
async def handle_first_receive(event: GroupMessageEvent):
    message = message_to_text(event.get_message())

    if not message:
        await chat.finish("昂，怎么了嘛")
    elif message in {"在嘛", "在吗"}:
        await chat.finish("在的呢")

    reply = await asyncify(to_message)(group_id=event.group_id, msg=message)
    await chat.finish(reply)
