from typing import Optional

import httpx
from nonebot import export

HITOKOTO_URL = 'https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=g&encode=text'


async def fetch_hitokoto_str() -> Optional[str]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(HITOKOTO_URL)
        if resp.status_code != 200:
            return None
        return resp.text