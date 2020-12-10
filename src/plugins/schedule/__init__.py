from nonebot import get_driver, require, logger, get_bots
from nonebot.adapters.cqhttp import Bot, Message

from .config import Config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from time import localtime, strftime

global_config = get_driver().config
config = Config(**global_config.dict())

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler
fetch_hitokoto_str = require("src.plugins.hitokoto").fetch_hitokoto_str
fetch_city_data = require("src.plugins.weather").fetch_city_data
get_weather_message = require("src.plugins.weather").get_weather_message
get_air_message = require("src.plugins.weather").get_air_message


@scheduler.scheduled_job("cron", day="*", hour="7", minute="30", id="morning_task",
                         kwargs={"morning_groups": config.morning_groups,
                                 "key": config.weather_api_key})
async def run_every_2_hour(**kwargs):
    logger.debug("开始晨间早报~")
    bots = get_bots()
    for bot in bots.values():
        for groups in kwargs['morning_groups']:
            msg = Message()
            msg.append("早安！大家！是时候迎接新升的太阳了！\n")
            msg.append(strftime('今天是%Y年%m月%d日 现在时间%H:%M\n', localtime()))
            city_list = await fetch_city_data(kwargs["key"], groups["place"])
            if city_list is None or city_list["code"] == "403" or city_list["code"] == "402":
                msg.append("请求天气API失败！请联系管理员！")
            if city_list["code"] == "204" or city_list["code"] == "404":
                msg.append("无您想要的地区天气！")

            location = city_list["location"][int(groups["idx"])]
            id = location["id"]
            msg.extend(await get_weather_message(kwargs["key"], groups["place"], id))
            msg.extend(await get_air_message(kwargs["key"], id))
            msg.append(f"一言：{await fetch_hitokoto_str()}")
            logger.debug(msg)
            await bot.send_group_msg(group_id=groups["id"], message=msg)
