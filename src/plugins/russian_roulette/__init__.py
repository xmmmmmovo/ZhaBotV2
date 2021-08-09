# import nonebot
from itertools import groupby
from random import randint, seed

from src.imports import *
from src.model.group import *
from src.model.shot import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("russian_roulette")
export().name = "俄罗斯轮盘"
export().description = "一夜暴富"

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

start = on_command("gun", rule=not_to_me(), permission=auth, priority=94)
shot = on_command("ping", rule=not_to_me(), permission=auth, priority=94)

# TODO：超时取消本次俄罗斯轮盘
# TODO: 增加决斗功能


@start.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    record = await find_or_insert_shot_model(event.group_id)
    logger.debug(record)
    if record["has_started"] == False:
        k = randint(0, 5)
        await init_shot_game(event.group_id, k)
        await start.finish(f"已开始俄罗斯轮盘，规则：\n"
                           "每位人员都可以.ping/。ping，如果被pong了将会损失10%(管理员和群主是30%)的资产(少于30的会直接清0但是不会禁言)并分配给前面所有参与的人员\n"
                           f"复活时间{state['group']['ban_time']}min(禁言1min)")
    else:
        await start.finish("本轮已经开始了咯，请'.ping/。ping'")


@shot.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    user = state["user"]
    record = await find_shot_model(event.group_id)
    if record is None:
        await shot.finish("本轮已结束，请'。gun'重新开始")

    k = int(record["k"])
    idx = int(record["idx"])

    if k == idx:
        money = float(user["money"])
        if money < 30:
            money = 30
        else:
            if event.sender.role == "admin" or event.sender.role == "owner":
                money = float(user["money"]) * 0.3
            else:
                money = float(user["money"]) * 0.1
                bot.set_group_ban(group_id=event.group_id,
                                  user_id=event.user_id, duration=60 * int(state['group']['ban_time']))

        await update_user_money_model(event.user_id, event.group_id, -money)
        qqs = record["qqs"]
        if len(qqs) != 0:
            each_money = money / len(qqs)
            for qq in qqs:
                await update_user_money_model(qq["qq"], event.group_id, each_money)

        await update_inc_ban_time(event.group_id)
        await remove_shot_reocrd(event.group_id)
        await shot.send(f"pong! " + MessageSegment.face(169) + f"\n你被干掉了! 并损失了{money}{config.money_unit}!")
        statistics = {
            gres[0]: len(list(gres[1])) for gres in groupby(qqs, lambda qq: qq["nickname"])
        }
        logger.debug(statistics)
        await shot.finish("本场结算：\n" + "\n".join(map(lambda t: f"{t[0]}: {t[1] * each_money}", statistics.items())))
    else:
        await update_shot_idx(event.group_id, {"qq": event.user_id, "nickname": event.sender.nickname})
        await shot.finish("pa~")


@scheduler.scheduled_job("cron", day="*", hour="0", minute="0", id="reset_ban_time_task", kwargs={})
async def run_every_day_reset_ban_time(**kwargs):
    await reset_ban_time()