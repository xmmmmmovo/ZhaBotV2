from asyncio import sleep
from decimal import Decimal
from random import randint

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import get_driver, require, on_command, on_startswith, logger
from re import split

from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.permission import SUPERUSER, GROUP, GROUP_ADMIN, GROUP_OWNER

from .config import Config
from .data_source import reset_help_count, records, Record, start_head, insert_help_count, \
    select_one_help_count_by_qq, decrease_help_count, events, tools_def
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("permission").NOT_ANONYMOUS_GROUP
fetch_user_sign_status = require("dao").fetch_user_sign_status
insert_user = require("dao").insert_user
fetch_user_money_status = require("economic").fetch_user_money_status
increase_user_money = require("economic").increase_user_money
scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

reset_help_count_handler = on_command("resethc", rule=not_to_me(), permission=SUPERUSER, priority=7)
stop_race = on_command("stoprace", aliases={"停止赛马"}, rule=not_to_me(), permission=GROUP_ADMIN | GROUP_OWNER, priority=7)
bet_horse = on_command("押马", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
chocolate = on_command("巧克力", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
hyper = on_command("兴奋剂", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
banana = on_command("香蕉皮", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
pary = on_command("祈祷", rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
start_race = on_command("startrace", aliases={"开始赛马"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
begging = on_command("begging", aliases={"救济金"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
shop = on_command("shop", aliases={"商品列表", "商品目录"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=7)
horse_ready = on_command("horseready", aliases={"赛马", "准备赛马"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP,
                         priority=7)


@scheduler.scheduled_job("cron", day="*", hour="0", minute="0", id="reset_help_count_task", kwargs={})
async def run_every_day_reset_help_count(**kwargs):
    await reset_help_count(config.help_count)


@reset_help_count_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    ret = await reset_help_count(config.help_count)
    await reset_help_count_handler.finish("已成功重置" if ret else "重置失败")


@horse_ready.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    record = records.get(event.group_id)
    if record is None:
        records[event.group_id] = record = Record(
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
        record.is_start = False
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
        money = Decimal(state["remain"]) \
            if state["money"] in config.stud_list \
            else (Decimal(state["money"]))
    except:
        await bet_horse.finish("金钱输入格式错误！请重新输入")
    horse = int(state["horse"])
    if money > Decimal(state["remain"]) or money < Decimal(0):
        await bet_horse.finish("没有足够的金钱！可尝试输入'。救济金'领取")

    record: Record = state["record"]
    record.user_list[event.user_id] = [horse - 1, money]
    logger.debug(records[event.group_id])
    await bet_horse.finish(f"成功押注{horse}号马{money}{config.money_unit}")


@chocolate.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    pass


@hyper.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    pass


@banana.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    pass


@pary.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    pass


@start_race.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    # 游戏主函数
    record: Record = records.get(event.group_id)
    if record is None:
        await start_race.finish("游戏还未准备，请'.赛马'来准备")
    if record.is_start:
        await start_race.finish("游戏已经开始！")
    # if len(record.user_list) < 3:
    #     await start_race.finish('赛马比赛至少需要3人！')
    logger.debug("开始赛马~")

    record.is_start = True
    await game_main(record)
    record.is_start = False
    await end_game(event, record)


async def init_slide(record: Record):
    for k in range(len(record.slides)):
        record.slides[k] = config.slide * config.slide_length


async def final_check(record: Record):
    n_rank = len(record.rank) + 1

    if n_rank > 3:
        return False

    for (k, h_iter) in enumerate(record.horses):
        if h_iter == 0:
            h = record.rank.get(k)
            if h is None:
                record.rank[k] = n_rank

    return True


async def game_main(record: Record):
    # 游戏主体
    while record.is_start and await final_check(record):
        await init_slide(record)
        logger.debug(record)
        await sleep(4)
        event_num = randint(0, len(events))
        if event_num != 0:
            await events[event_num](start_race, record)

        # 下面是马跑路相关
        # 和检查是否小于0函数
        for (k, h_iter) in enumerate(record.horses):
            record.horses[k] -= randint(0, 2)

            if record.horses[k] < 0:
                record.horses[k] = 0

            if record.horses[k] > 14:
                record.horses[k] = 14

            h_iter = record.horses[k]

            record.slides[k] = record.slides[k][:h_iter] + \
                               config.horse_char + \
                               record.slides[k][h_iter + 1:]

        # 下面是输出跑道状态
        await start_race.send(
            '\n'.join(
                f'{k + 1} {s_iter}' for (k, s_iter)
                in enumerate(record.slides)
            )
        )


async def calcu_results(record: Record):
    """
    计算结果
    :param record:
    :return: 奖金值
    """
    logger.debug('开始计算')
    every_house_cnt = [0, 0, 0, 0, 0]
    player_num = len(record.user_list)
    for p in record.user_list.values():
        every_house_cnt[p[0]] += 1
    logger.debug(every_house_cnt)
    for qq, bet in record.user_list.items():
        if bet[0] in record.rank.keys():
            persons = every_house_cnt[bet[0]]
            # 根据获胜的人数和游玩的人数来进行判断倍率
            if persons <= (player_num - persons + 1):
                record.user_list[qq].append(
                    Decimal(config.odd[record.rank[bet[0]]]) * bet[1]
                )
            else:
                record.user_list[qq].append(
                    Decimal(
                        (1 + ((config.odd[record.rank[bet[0]]] - 1)
                              * (persons / player_num))
                         )
                    ) * bet[1]
                )
        else:
            # 奖励变成负数
            record.user_list[qq].append(-bet[1])
    logger.debug(record)


async def update_money(event: Event, record: Record):
    logger.debug(record.user_list)
    for k, v in record.user_list.items():
        await increase_user_money(k, event.group_id, v[2])


async def end_game(event: Event, record: Record):
    """
    比赛结束后的结算函数
    :param event:
    :param record:
    :return:
    """
    logger.debug('游戏结束')
    res = '本场赛马已结束!\n'
    res += '\n'.join(f'第{v}名：{k + 1}号马！' for k, v in record.rank.items())
    res += '\n现在开始结算...'
    await start_race.send(res)
    # 下面是清算相关函数
    await calcu_results(record)
    await update_money(event, record)
    records.pop(event.group_id)
    await start_race.finish('已结算！')


@shop.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    await shop.finish('\n'.join(tools_def))
