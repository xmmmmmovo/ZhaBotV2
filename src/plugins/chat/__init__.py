# import nonebot
from src.imports import *
from src.utils.msgutils import message_to_text
from .config import Config
from openai import AsyncOpenAI

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

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


@chat.handle()
async def handle_first_receive(event: GroupMessageEvent):
    message = message_to_text(event.get_message())

    if not message:
        await chat.finish("昂，怎么了嘛")
    elif message in {"在嘛", "在吗"}:
        await chat.finish("在的呢")

    chat_response = await client.chat.completions.create(
        model="Qwen/Qwen2-0.5B-Instruct",
        messages=[
            {"role": "system", "content": f"你的名字叫小扎，是一个18岁可爱机器人"},
            {"role": "user", "content": message},
        ],
        temperature=0.7,
        top_p=0.8,
        max_tokens=512,
        extra_body={
            "repetition_penalty": 1.05,
        },
    )
    reply : Message = Message()
    reply.append(MessageSegment.reply(event.message_id))
    reply.append(chat_response.choices[0].message.content) # type: ignore
    await chat.finish(reply)
