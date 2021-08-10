# import nonebot

from src.imports import *

from .config import Config
from .data_source import fetch_sx_data

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("sx")
export().name = "缩写"
export().description = "能不能好好说话"

sx = on_command("sx", rule=not_to_me(), permission=auth, priority=95)


@sx.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.get_plaintext()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    data = await fetch_sx_data(args)
    if data:
        await sx.finish(f"{data[0]['name']}:\n" + "; ".join(data[0]["trans"]))
    else:
        await sx.finish("还没有此缩写的数据捏")
