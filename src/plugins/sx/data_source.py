from aiocache import cached
import httpx

NBNHHSH_URL = "https://lab.magiconch.com/api/nbnhhsh/guess"
headers = {
    'origin': 'https://lab.magiconch.com',
    'referer': 'https://lab.magiconch.com/nbnhhsh/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}


@cached(ttl=24*60*60)
async def fetch_sx_data(sx: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(NBNHHSH_URL, headers=headers, data={"text": sx})
        if resp.status_code == 200:
            json = resp.json()
            return json if json else []
        return []
