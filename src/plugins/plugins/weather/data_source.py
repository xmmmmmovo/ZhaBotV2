from typing import Dict, Optional

import httpx
from aiocache import cached
from nonebot import logger, export
from nonebot.adapters.cqhttp import Message, MessageSegment

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


async def get_weather_message(key: str, city_name: str, city_id: str, WEATHER_ICON_DIR: str) -> Message:
    reply_today = Message()
    status_now = await fetch_weather_data(key, city_id, "now")
    logger.debug(status_now)
    if status_now is None or status_now["code"] != "200":
        reply_today.append("获取当前天气失败！\n")
    else:
        reply_today.append(f"******{city_name}天气如下******\n")
        reply_today.append(f"天气：{status_now['now']['text']}")
        reply_today.append(MessageSegment.image(f"file:///{WEATHER_ICON_DIR}{status_now['now']['icon']}.png"))
        reply_today.append("\n")
        reply_today.append(f"体感温度：{status_now['now']['feelsLike']}℃ 湿度：{status_now['now']['humidity']}%\n")
        reply_today.append(f"风力等级：{status_now['now']['windScale']}级\n")
    return reply_today


async def get_air_message(key: str, city_id: str) -> Message:
    reply_today = Message()
    air_now = await fetch_air_data(key, city_id)
    if air_now is None or air_now["code"] != "200":
        reply_today.append("获取当前空气质量失败！\n")
    else:
        reply_today.append(f"空气质量：{air_now['now']['category']} 空气质量指数：{air_now['now']['aqi']}\n")
        reply_today.append(f"PM2.5：{air_now['now']['pm2p5']} PM10：{air_now['now']['pm10']}\n")
        reply_today.append(f"空气主要污染物：{air_now['now']['primary']}\n")
    return reply_today


async def get_tomorrow_weather_message(key: str, city_name: str, city_id: str, WEATHER_ICON_DIR: str) -> Message:
    reply_tomorrow = Message()
    status_tomorrow = await fetch_weather_data(key, city_id, "3d")
    if status_tomorrow is None or status_tomorrow["code"] != "200":
        reply_tomorrow.append("获取明日天气失败！\n")
    else:
        tom = status_tomorrow["daily"][1]
        reply_tomorrow.append(f"******{city_name}明日天气******\n")
        reply_tomorrow.append(f"白天天气：{tom['textDay']}")
        reply_tomorrow.append(MessageSegment.image(f"file:///{WEATHER_ICON_DIR}{tom['iconDay']}.png"))
        reply_tomorrow.append("\n")
        reply_tomorrow.append(f"夜间天气：{tom['textNight']}")
        reply_tomorrow.append(MessageSegment.image(f"file:///{WEATHER_ICON_DIR}{tom['iconNight']}.png"))
        reply_tomorrow.append("\n")
        reply_tomorrow.append(f"最高温度：{tom['tempMax']}℃ 最低温度：{tom['tempMin']}℃ 湿度：{tom['humidity']}%\n")
        reply_tomorrow.append(f"白天风力等级：{tom['windScaleDay']}级 夜间风力等级：{tom['windScaleNight']}级\n")
    return reply_tomorrow
