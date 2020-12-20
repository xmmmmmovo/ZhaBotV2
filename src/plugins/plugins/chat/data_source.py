import random
import string
import time
from hashlib import md5
from typing import Optional, Dict
from urllib.parse import quote
import httpx

CHAT_API = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
ALL_STR = string.ascii_letters + string.digits


async def calcu_sign(raw: str):
    ans = md5()
    ans.update(raw.encode(encoding='utf-8'))
    return ans.hexdigest().upper()


async def call_tencent_api(qq: int, content: str, id: str, key: str) -> Optional[Dict]:
    rand_str = ''.join(random.sample(ALL_STR, 20))  # 随机字符串
    time_pin = int(time.time())  # 时间戳

    raw = "app_id=" + id + \
          "&nonce_str=" + rand_str + \
          "&question=" + quote(content.replace(' ', '。')) + \
          "&session=" + str(qq) + \
          "&time_stamp=" + str(time_pin)

    sign = await calcu_sign(raw + "&app_key=" + key)
    raw += '&sign=' + sign
    async with httpx.AsyncClient() as client:
        resp = await client.get(CHAT_API + "?" + raw)
        if resp.status_code != 200:
            return None
        return resp.json()