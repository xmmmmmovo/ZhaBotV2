# import nonebot

from src.imports import *

from .config import Config
from .data_source import fetch_sx_data

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("sx")
simple = auth.auth_permission()

__plugin_meta__ = PluginMetadata(
    name="sx",
    description="缩写",
    usage="能不能好好说话",
    type="application",
    config=Config,
    extra={},
)

sx = on_command(
    "sx", aliases={"缩写"}, rule=not_to_me(), permission=simple, priority=10
)

@sx.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    data = await fetch_sx_data(args.extract_plain_text().strip())
    if data and "trans" in data[0]:
        await sx.finish(f"{data[0]['name']}:\n" + "; ".join(data[0]["trans"]))
    else:
        await sx.finish("还没有此缩写的数据捏")
