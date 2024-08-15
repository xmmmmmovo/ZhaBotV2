from pypinyin import pinyin
from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("pinyin")
simple = auth.auth_permission()

__plugin_meta__ = PluginMetadata(
    name="pinyin",
    description="拼音",
    usage="拼音识字",
    type="application",
    config=Config,
    extra={},
)

pinyinp = on_command("pinyin", aliases={
    "拼音"}, rule=not_to_me(), permission=simple, priority=10)


@pinyinp.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    data = pinyin(args.extract_plain_text().strip())
    if data:
        await pinyinp.finish(" ".join(map(lambda l: '暂无数据' if l[0] == '' else l[0], data)))
    else:
        await pinyinp.finish("还没有此词的拼音捏")
