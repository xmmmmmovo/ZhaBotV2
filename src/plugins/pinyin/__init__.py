from pypinyin import pinyin
from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("pinyin")
simple = auth.auth_permission()
export().name = "拼音"
export().description = "拼音识字"


pinyinp = on_command("pinyin", aliases={
                    "拼音"}, rule=not_to_me(), permission=simple, priority=90)


@pinyinp.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    args = str(event.get_plaintext()).strip()
    data = pinyin(args)
    if data:
        await pinyinp.finish(" ".join(map(lambda l: '暂无数据' if l[0] == '' else l[0], data)))
    else:
        await pinyinp.finish("还没有此词的拼音捏")
