from asyncio import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import get_driver, require, on_command, on_startswith, logger
from re import split

from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.permission import SUPERUSER, GROUP, GROUP_ADMIN, GROUP_OWNER

from .config import Config
from .data_source import reset_help_count, records, Record, start_head, select_user_order_by_money, insert_help_count, \
    select_one_help_count_by_qq, decrease_help_count
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("permission").NOT_ANONYMOUS_GROUP
fetch_user_sign_status = require("dao").fetch_user_sign_status
insert_user = require("dao").insert_user
fetch_user_money_status = require("dao").fetch_user_money_status
increase_user_money = require("dao").increase_user_money
scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

reset_help_count_handler = on_command("resethc", rule=not_to_me(), permission=SUPERUSER, priority=7)
stop_race = on_command("stoprace", aliases={"停止赛马"}, rule=not_to_me(), permission=GROUP_ADMIN | GROUP_OWNER, priority=7)
bet_horse = on_command("押马", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
start_race = on_command("startrace", aliases={"开始赛马"}, rule=not_to_me(), permission=GROUP_ADMIN | GROUP_OWNER,
                        priority=7)
begging = on_command("begging", aliases={"救济金"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
shop = on_command("shop", aliases={"商品列表"}, rule=not_to_me(), permission=GROUP, priority=7)
rank = on_command("rank", aliases={"排名", "排行"}, rule=not_to_me(), permission=GROUP, priority=7)
horse_ready = on_command("horseready", aliases={"赛马", "准备赛马"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP,
                         priority=7)


@scheduler.scheduled_job("cron", day="*", hour="0", minute="0", id="reset_signed_task", kwargs={})
async def run_every_day_reset_signed(**kwargs):
    await reset_help_count(config.help_count)


@reset_help_count_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    ret = await reset_help_count(config.help_count)
    await reset_help_count_handler.finish("已成功重置" if ret else "重置失败")


@horse_ready.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    group_id = event.group_id
    record: Record = records.get(group_id)
    if record is None:
        records[group_id] = Record(
            user_list={},
            tools=[],
            rank={},
            horses=[config.slide_length - 1 for _ in range(config.horse_num)],
            slides=['' for _ in range(config.horse_num)],
            is_start=False
        )
        await horse_ready.finish(start_head)

    if not record.is_start:
        await horse_ready.finish("本局赛马已经开始准备咯"
                                 "请输入开始赛马进行游戏吧！")


@rank.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    u_list = await select_user_order_by_money(event.group_id)
    group_list = await bot.get_group_member_list(group_id=event.group_id)

    group_dict = {}
    for u in group_list:
        group_dict[u['user_id']] = u['card'] \
            if u['card'] != '' else u['nickname']

    ans = '江江江江！本群土豪排名公布~\n'
    cnt = 0

    user_id = event.user_id
    for u in u_list:
        if group_dict.get(u['qq']) is None:
            continue

        cnt += 1

        if cnt > 20:
            if event.sub_type != "anonymous" and user_id == u['qq']:
                ans += f"你是第{cnt}名 现有财产{u['money']}$"
                break
            continue

        ans += f"第{cnt}名: {group_dict[u['qq']]} 现有财产:{u['money']}$\n"

    await rank.finish(ans)


@begging.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    res = await fetch_user_sign_status(event.user_id, event.group_id)
    if res is None:
        succ = await insert_user(event.user_id, event.group_id, 0, int(False))
        if not succ:
            await begging.finish("救济金领取失败！")
    res = await fetch_user_money_status(event.user_id, event.group_id)

    help_count_res = await select_one_help_count_by_qq(event.user_id)
    if help_count_res is None:
        succ = await insert_help_count(event.user_id, config.help_count)
        if not succ:
            await begging.finish("救济金领取失败！")
        help_count_res = await select_one_help_count_by_qq(event.user_id)

    if help_count_res["help_count"] > 0:
        if res["money"] == 0:
            succ = await increase_user_money(event.user_id, event.group_id, config.help_money)
            if not succ:
                await begging.finish("救济金领取失败！")
            succ = await decrease_help_count(event.user_id)
            if not succ:
                await begging.finish("救济金领取失败！")
            await begging.finish(f'已成功为您发放救济金20{config.money_unit}！'
                                 f'当前剩余救济金次数：{help_count_res["help_count"] - 1}')
        else:
            await begging.finish('您的资产并不为0，不能领取救济金！')
    else:
        await begging.finish('您今天的救济金次数已用尽！')


@stop_race.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    group_id = event.group_id
    record = records.get(group_id)  # 查找是否有原来的游戏信息

    if record is None:
        await stop_race.finish("赛马还没开始呢")

    if record.is_start:
        records.pop(event.group_id)
        await stop_race.finish("已停止赛马")
    else:
        await stop_race.finish("赛马还没开始呢")


@bet_horse.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    record: Record = records.get(event.group_id)
    state["record"] = record

    if record is None:
        await bet_horse.finish("还未有人准备开始赛马!")

    if record.is_start:
        await bet_horse.finish("赛马比赛已经开始，无法下注！")

    msg = str(event.message).strip()
    logger.debug(msg)

    res = await fetch_user_money_status(event.user_id, event.group_id)
    if res is None:
        succ = await insert_user(event.user_id, event.group_id, 0, int(False))
        if not succ:
            await bet_horse.finish("押马失败！")
        money = 0.0
    else:
        money = res["money"]
    args = split(",|，", msg)
    state["remain"] = money

    if len(args) == 0:
        return
    elif len(args) == 1:
        state["horse"] = args[0]
    elif len(args) == 2:
        state["horse"] = args[0]
        state["money"] = args[1]


@bet_horse.got("horse", prompt="请输入想要押马的编号")
async def handle_city(bot: Bot, event: Event, state: dict):
    try:
        horse = int(state["horse"])
    except:
        await bet_horse.finish("马编号输入格式错误！请重新输入")

    if horse < 1 or horse > config.horse_num:
        await bet_horse.finish("没有此编号马！请重新输入")


@bet_horse.got("money", prompt="请输入押注钱数")
async def handle_city(bot: Bot, event: Event, state: dict):
    logger.debug(state["money"])
    try:
        money = state["remain"] \
            if state["money"] in config.stud_list \
            else (state["money"])
    except:
        await bet_horse.finish("金钱输入格式错误！请重新输入")
    horse = int(state["horse"])
    if money > float(state["remain"]):
        await bet_horse.finish("没有足够的金钱！可尝试输入'。救济金'领取")

    record: Record = state["record"]
    record.user_list[event.user_id] = [horse - 1, money]
    logger.debug(records[event.group_id])
    await bet_horse.finish(f"成功押注{horse}号马{money}{config.money_unit}")


@start_race.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    # 游戏主函数
    record: Record = records.get(event.group_id)
    if record is None:
        await start_race.finish("游戏还未准备，请'.赛马'来准备")
    if record.is_start:
        await start_race.finish("游戏已经开始！")

    record.is_start = True
    await game_main(record)


async def init_slide(record: Record):
    for k in range(len(record.slides)):
        record.slides[k] = config.slide * config.slide_length


async def game_main(record: Record):
    while True:
        await init_slide(record)
        logger.debug(record)
        await sleep(4)

        pass
