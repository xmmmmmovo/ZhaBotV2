from random import randint

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import get_driver, on_command, logger, require
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("src.plugins.permission").NOT_ANONYMOUS_GROUP
fetch_user_sign_status = require("src.plugins.dao").fetch_user_sign_status
insert_user = require("src.plugins.dao").insert_user
update_user = require("src.plugins.dao").update_user
reset_user_signed = require("src.plugins.dao").reset_user_signed
scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

check_in = on_command("签到", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=3)


@check_in.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    if str(event.message).strip():
        await check_in.finish("11")

    user_status = await fetch_user_sign_status(event.user_id, event.group_id)
    sign_money = randint(config.sign_in_money_down, config.sign_in_money_up)

    logger.debug(user_status)

    if user_status is None:
        succ = await insert_user(event.user_id, event.group_id, sign_money, int(True))
    else:
        if user_status["has_signed"] == True:
            await check_in.finish(MessageSegment.at(event.user_id) + "您今日已签过到，请勿重复签到！")
        succ = await update_user(event.user_id, event.group_id, sign_money, int(True))

    logger.debug(succ)
    if succ:
        await check_in.finish(MessageSegment.at(event.user_id) + f"您已签到成功！获得金钱：{sign_money}{config.money_unit}")
    else:
        await check_in.finish(MessageSegment.at(event.user_id) + "对不起，签到失败，请重新签到或者联系管理！")


@scheduler.scheduled_job("cron", day="*", hour="0", minute="0", id="reset_signed_task", kwargs={})
async def run_every_day_reset_signed(**kwargs):
    await reset_user_signed(int(False))
