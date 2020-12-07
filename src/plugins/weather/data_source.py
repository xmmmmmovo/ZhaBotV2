from typing import Dict, Optional

import httpx
from aiocache import cached
from nonebot import logger

CITY_LOOKUP_URL = "https://geoapi.qweather.com/v2/city/lookup"
WEATHER_API_URL = 'https://devapi.qweather.com/v7/weather/'
RAIN_API_URL = 'https://devapi.qweather.com/v7/minutely/5m'
AIR_API_URL = 'https://devapi.qweather.com/v7/air/now'


@cached(ttl=8 * 60 * 60)
async def fetch_city_data(key: str, location: str) -> Optional[Dict]:
    """
    获取城市信息
    :param key:
    :param location:
    :return: Dict或者None
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(CITY_LOOKUP_URL, params={"location": location, "key": key})
        if resp.status_code != 200:
            return None
        resp_json = resp.json()
        return resp_json


@cached(ttl=1 * 60 * 60)
async def fetch_weather_data(key: str, id: str, date: str) -> Optional[Dict]:
    """
    获取天气数据
    :param key:
    :param id:地区id
    :param date:
    :return:
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(WEATHER_API_URL + date, params={"location": id, "key": key})
        if resp.status_code != 200:
            return None
        resp_json = resp.json()
        return resp_json


@cached(ttl=1 * 60 * 60)
async def fetch_air_data(key: str, id: str) -> Optional[Dict]:
    """
    获取空气数据
    :param key:
    :param id:
    :return:
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(AIR_API_URL, params={"location": id, "key": key})
        if resp.status_code != 200:
            return None
        resp_json = resp.json()
        return resp_json


@cached(ttl=30 * 60)
async def fetch_rain_data(key: str, id: str) -> Optional[Dict]:
    """
    获取下雨数据
    :param key:
    :param id:
    :return:
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(RAIN_API_URL, params={"location": id, "key": key})
        if resp.status_code != 200:
            return None
        resp_json = resp.json()
        return resp_json
