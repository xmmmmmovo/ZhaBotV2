import httpx
from aiocache import cached

BILIBILI_SEARCH_URL = "http://api.bilibili.com/x/web-interface/search/all/v2"


@cached(ttl=24 * 60 * 60)
async def fetch_bilibili_search(title: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(BILIBILI_SEARCH_URL, params={"keyword": title})
        if resp.status_code != 200:
            return None
        resp_json = resp.json()
        return resp_json


def num_to_nlps(num) -> str:
    '''
    递归实现，精确为最大单位值 + 小数点后三位
    '''

    def strofsize(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strofsize(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 3), units[level])
