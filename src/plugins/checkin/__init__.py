from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("checkin")
simple = auth.auth_permission()
export().name = "签到"
export().description = "签到功能"

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

check_in = on_command("签到", rule=not_to_me(), permission=simple, priority=96)
check_rank = on_command("签到排名", rule=not_to_me, permission=simple, priority=96)


@check_in.handle()
async def handle_first_receive(matcher: Matcher, event: Event, args: Message = CommandArg(), user: dict = Arg("user"), group: dict = Arg("group")):
    sign_money = randint(config.sign_in_money_lower_limit,
                         config.sign_in_money_upper_limit)
    if user["has_signed"] == True:
        await check_in.finish(MessageSegment.at(event.user_id) + "您今日已签过到，请勿重复签到！每天5:00刷新")
    await user_collection.update_one(*update_user_model(event.user_id, event.group_id, sign_money, True, 1))
    await group_collection.update_one(*update_inc_rank(event.group_id))
    await check_in.finish(MessageSegment.at(event.user_id) + f"签到成功！今日排名第{int(group['rank'])}名，已连续签到{int(user['days']) + 1}天！\n本次签到获得金钱：{sign_money}{config.money_unit}")


@check_rank.handle()
async def handle_first_receive(matcher: Matcher, event: Event, args: Message = CommandArg(), user: dict = Arg("user"), group: dict = Arg("group")):
    pass


@scheduler.scheduled_job("cron", day="*", hour="5", minute="0", id="reset_signed_task", kwargs={})
async def run_every_day_reset_signed(**kwargs):
    await user_collection.update_many({"has_signed": False}, {"$set": {"days": 0}})
    await user_collection.update_many({}, {"$set": {"has_signed": False}})
    await group_collection.update_many({}, {"$set": {"rank": 1}})