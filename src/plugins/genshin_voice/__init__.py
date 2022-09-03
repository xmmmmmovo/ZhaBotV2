from typing import Any, Tuple
from nonebot.params import RegexGroup
import httpx
import cn2an
from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

auth = Auth("genshin_voice")
simple = auth.auth_permission()
export().name = "原神语句生成"
export().description = "实验性功能"

gs_regex = r"^我想要(派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏)(发送|说)(.+)$"
gs_cmd = on_regex(gs_regex, rule=not_to_me(),
                  permission=simple, priority=12)

API_URL = "http://233366.proxy.nscc-gz.cn:8888"


async def get_voice(msg: str, name: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_URL, params={"speaker": name, "text": msg})
        if resp.status_code != 200:
            await gs_cmd.finish('对方貌似现在不方便呢 请过段时间再试试吧')
        voice = resp.content
        return MessageSegment.record(voice)


@gs_cmd.handle()
async def _(bot: Bot, event: Event, matched: Tuple[Any, ...] = RegexGroup()):
    name, msg = matched[0], matched[2]
    if name == "":
        await gs_cmd.finish("未获取到角色名！")
    reply_msg = await get_voice(msg=cn2an.transform(msg, "an2cn"), name=name)
    await gs_cmd.finish(message=reply_msg)
