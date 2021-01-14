import httpx
from nonebot import get_driver, on_message, logger, export
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment
from nonebot.permission import Permission

from src.common.rules import not_to_me
from .config import Config
from ujson import loads
from urllib.parse import urlparse

from .data_source import fetch_bilibili_search, num_to_nlps

global_config = get_driver().config
config = Config(**global_config.dict())

bilibili_share = on_message(rule=not_to_me(), permission=Permission(), priority=100)

headers = {
    "Referer": "https://www.bilibili.com/",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.70"
}
BILIBILI_SPACE_BASE = "https://space.bilibili.com/"


@bilibili_share.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if any(msg.type == "json" for msg in event.message):
        msg = ""
        for m in event.message:
            if m.type == "json":
                msg = m
        msg = loads(msg.data["data"])
        logger.debug(msg)
        if msg["app"] != "com.tencent.miniapp_01" and msg["desc"] == "哔哩哔哩":
            await bilibili_share.finish()
        reply = Message()
        reply.append(MessageSegment.image("http://" + msg["meta"]["detail_1"]["preview"]))
        reply.append("\n")
        reply.append(f"标题：{msg['meta']['detail_1']['desc']}")
        resp = await fetch_bilibili_search(msg['meta']['detail_1']['desc'])
        if resp is None or resp['code'] == '-400' or int(resp['data']['numResults']) < 1:
            url = urlparse(msg['meta']['detail_1']['qqdocurl'])
            reply.append(f"url:{url.scheme}://{url.netloc}{url.path}\n")
            reply.append("其他信息获取失败！请联系管理！")
        else:
            result = resp['data']['result']
            for rd in result:
                if len(rd['data']) != 0:
                    reply.append(f"url：{rd['data'][0]['arcurl']}\n")
                    reply.append(f"bv号：{rd['data'][0]['bvid']}\n")
                    reply.append(f"UP主：{rd['data'][0]['author']}({BILIBILI_SPACE_BASE}{rd['data'][0]['mid']})\n")
                    reply.append(f"简介：{rd['data'][0]['description']}\n")
                    reply.append(f"观看数量：{num_to_nlps(int(rd['data'][0]['play']))}\n")
        await bilibili_share.finish(reply)
