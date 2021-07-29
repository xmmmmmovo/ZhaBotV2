from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("signin")
export().name = "签到"
export().description = "签到功能"

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

check_in = on_command("签到", rule=not_to_me(), permission=auth, priority=96)


@check_in.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    user_status = await user_collection.find_one(find_user_model(event.user_id, event.group_id))
    sign_money = randint(config.sign_in_money_lower_limit, config.sign_in_money_upper_limit)

    if user_status is None:
        await user_collection.insert_one(new_user_model(event.user_id, event.group_id, sign_money, True))
    else:
        if user_status["has_signed"] == True:
            await check_in.finish(MessageSegment.at(event.user_id) + "您今日已签过到，请勿重复签到！")
        await user_collection.update_one(*update_user_model(event.user_id, event.group_id, sign_money, True))

    await check_in.finish(MessageSegment.at(event.user_id) + f"您已签到成功！获得金钱：{sign_money}{config.money_unit}")


@scheduler.scheduled_job("cron", day="*", hour="6", minute="30", id="reset_signed_task", kwargs={})
async def run_every_day_reset_signed(**kwargs):
    await user_collection.update_many({}, {"$set": {"has_signed": False}})
