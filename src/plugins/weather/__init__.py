from src.imports import *

from .config import Config
from .data_source import fetch_city_data, get_weather_message, get_air_message, \
    get_tomorrow_weather_message

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("weather")
simple = auth.auth_permission()
export().name = "天气"
export().description = "用来查天气的"

weather = on_command("天气", rule=not_to_me(), permission=simple, priority=98)


@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    arg = args.extract_plain_text().strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if arg:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(matcher: Matcher, city: str = ArgPlainText("city")):
    city_list = await fetch_city_data(config.weather_api_key, city)
    if city_list is None or city_list["code"] == "403" or city_list["code"] == "402":
        await weather.finish("请求API失败！请联系管理员！")
    if city_list["code"] == "204" or city_list["code"] == "404":
        await weather.finish("无您想要的地区信息！")
    matcher.set_arg("location", city_list["location"])
    if len(city_list["location"]) == 1 or \
            city_list["location"][0]["name"] != city_list["location"][1]["name"]:
        matcher.set_arg("city_idx", 0)
    else:
        await weather.send("\n".join(
            map(lambda e: f"{e[0]}: {e[1]['adm1']}/{e[1]['adm2']}/{e[1]['name']}", enumerate(city_list["location"]))))


@weather.got("city_idx", prompt="请输入你想要获取的城市编号")
async def handle_city_list(matcher: Matcher,
                           city_idx: str = Arg("city_idx"),
                           city_list: list = Arg("location")):
    idx = int(city_idx)
    if idx < 0 or idx >= len(city_list):
        await weather.finish("请输入正确的编号！")
    city_id = city_list[idx]["id"]
    city_name = city_list[idx]["name"]

    reply_today = Message()
    reply_today.extend(await get_weather_message(config.weather_api_key, city_name, city_id))
    reply_today.extend(await get_air_message(config.weather_api_key, city_id))
    await weather.send(reply_today)
    await weather.finish(
        await get_tomorrow_weather_message(config.weather_api_key, city_name, city_id))
