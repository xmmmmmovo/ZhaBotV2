from nonebot import get_driver, on_command, logger
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment
from nonebot.permission import Permission

from .config import Config
from .data_source import fetch_city_data, fetch_weather_data, fetch_air_data
from src.common.rules import not_to_me
from os import getcwd

global_config = get_driver().config
config = Config(**global_config.dict())

weather = on_command("天气", rule=not_to_me(), permission=Permission(), priority=5)

WEATHER_ICON_DIR = f"{getcwd()}/store/weather-icon/"


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: dict):
    city = state["city"]
    city_list = await fetch_city_data(config.weather_api_key, city)
    if city_list is None or city_list["code"] == "403" or city_list["code"] == "402":
        await weather.finish("请求API失败！请联系管理员！")
    if city_list["code"] == "204" or city_list["code"] == "404":
        await weather.finish("无您想要的地区信息！")
    logger.debug(city_list)
    state["location"] = city_list["location"]
    if len(city_list["location"]) == 1 or \
            city_list["location"][0]["name"] != city_list["location"][1]["name"]:
        state["city_idx"] = 0
    else:
        await weather.send("\n".join(
            map(lambda e: f"{e[0]}: {e[1]['adm1']}/{e[1]['adm2']}/{e[1]['name']}", enumerate(city_list["location"]))))


@weather.got("city_idx", prompt="请输入你想要获取的城市编号")
async def handle_city_list(bot: Bot, event: Event, state: dict):
    idx = int(state["city_idx"])
    city_list = state["location"]
    if idx < 0 or idx >= len(city_list):
        await weather.finish("请输入正确的编号！")
    city_id = city_list[idx]["id"]
    city_name = city_list[idx]["name"]

    reply = Message()
    status_now = await fetch_weather_data(config.weather_api_key, city_id, "now")
    if status_now is None:
        reply.append("获取当前天气失败！\n")
    else:
        reply.append(f"******{city_name}天气如下******\n")
        reply.append(f"天气：{status_now['now']['text']}")
        reply.append(MessageSegment.image(f"file:///{WEATHER_ICON_DIR}{status_now['now']['icon']}.png"))
        reply.append("\n")
        reply.append(f"体感温度：{status_now['now']['feelsLike']}℃ 湿度：{status_now['now']['humidity']}%\n")
        reply.append(f"风力等级：{status_now['now']['windScale']}级\n")

    air_now = await fetch_air_data(config.weather_api_key, city_id)
    if air_now is None:
        reply.append("获取当前空气质量失败！\n")
    else:
        reply.append(f"空气质量：{air_now['now']['category']} 空气质量指数：{air_now['now']['aqi']}\n")
        reply.append(f"PM2.5：{air_now['now']['pm2p5']} PM10：{air_now['now']['pm10']}\n")
        reply.append(f"空气主要污染物：{air_now['now']['primary']}\n")

    status_tomorrow = fetch_weather_data(config.weather_api_key, city_id, "3d")
    if status_now is None:
        reply.append("获取明日天气失败！\n")
    else:
        tom = status_tomorrow["daily"][1]
        reply.append(f"******明日天气******\n")
        reply.append(f"白天天气：{tom['textDay']}")
        reply.append(MessageSegment.image(f"file:///{WEATHER_ICON_DIR}{tom['iconDay']}.png"))
        reply.append("\n")
        reply.append(f"夜间天气：{tom['textNight']}")
        reply.append(MessageSegment.image(f"file:///{WEATHER_ICON_DIR}{tom['iconNight']}.png"))
        reply.append("\n")
        reply.append(f"最高温度：{tom['tempMax']}℃ 最低温度：{tom['tempMin']}℃ 湿度：{tom['humidity']}%\n")
        reply.append(f"白天风力等级：{tom['windScaleDay']}级 夜间风力等级：{tom['windScaleNight']}级\n")
    await weather.finish(reply)
