# import nonebot
from src.model.horserace import *
from src.imports import *
from src.utils.msgutils import is_number
from .config import Config
from .data_source import *
from re import split
from asyncio import sleep

global_config = get_driver().config
config = Config(**global_config.dict())

auth = init_plugin(export(), "horserace", "赛马", "赛马比赛")
simple = auth.auth_permission()
admin = auth.admin_auth_permission()

bet_horse = on_command("押马", rule=not_to_me(), permission=simple, priority=93)
chocolate = on_command("巧克力", rule=not_to_me(), permission=simple, priority=93)
hyper = on_command("兴奋剂", rule=not_to_me(), permission=simple, priority=93)
banana = on_command("香蕉皮", rule=not_to_me(), permission=simple, priority=93)
pary = on_command("祈祷", rule=not_to_me(), permission=simple, priority=93)
start_race = on_command("startrace", aliases={
                        "开始赛马"}, rule=not_to_me(), permission=simple, priority=93)
shop = on_command("shop", aliases={"商品列表", "商品目录"},
                  rule=not_to_me(), permission=simple, priority=93)
horse_ready = on_command("horseready", aliases={"赛马", "准备赛马"}, rule=not_to_me(), permission=simple,
                         priority=93)


start_head = """赛马(beta0.1)
押这只马人数<=押其他马人数+1时：
奖励=赔率x下注金额
押这只马人数>押其他马人数+1时：
奖励=[100%+(赔率-100%)x（押其它马的人数/押马总人数）]x下注金额
输入 押马 x,y（x为数字，y为押金，如：押马 1,2）来选择您觉得会胜出的马，一人只能押一只
输入 开始赛马 开始比赛
注意：开始比赛后不能再选马
注意：只有前三只到达终点的马会根据名次获得获胜奖励（排名并列的情况下可能超过三只）
"""


@horse_ready.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    record = await find_race_model(event.group_id)
    if record is None:
        await init_horse_race_game(event.group_id, config.horse_num, config.slide_length)
        await horse_ready.finish(start_head)
    elif record["has_started"] == False:
        await horse_ready.finish("本局赛马已经开始准备咯"
                                 "请输入开始赛马进行游戏吧！")


@bet_horse.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    record = await find_race_model(event.group_id)
    user = state["user"]

    if record is None:
        await bet_horse.finish("还未有人准备开始赛马!")

    if record.is_start:
        await bet_horse.finish("赛马比赛已经开始，无法下注！")

    msg = event.get_plaintext().strip()
    args = split(",|，", msg)

    if len(args) == 0:
        return
    elif len(args) == 1:
        state["horse"] = args[0]
    elif len(args) == 2:
        state["horse"] = args[0]
        state["money"] = args[1]


@bet_horse.got("horse", prompt="请输入想要押马的编号")
async def handle_key(bot: Bot, event: GroupMessageEvent, state: dict):
    try:
        horse = int(state["horse"])
    except:
        await bet_horse.finish("马编号输入格式错误！请重新输入")

    if horse < 1 or horse > config.horse_num:
        await bet_horse.finish("没有此编号马！请重新输入")


@bet_horse.got("money", prompt="请输入押注钱数")
async def handle_key(bot: Bot, event: GroupMessageEvent, state: dict):
    money = state["money"]
    if is_number(money):
        money = float(state["user"]["money"]) \
            if state["money"] in config.stud_list \
            else (state["money"])
    else:
        await bet_horse.finish("金钱输入格式错误！请重新输入")
    horse = int(state["horse"])
    if money > float(state["user"]["money"]) or money < 0:
        await bet_horse.finish("没有足够的金钱！")

    await update_bet_money(event.group_id, event.user_id, money, horse)
    await bet_horse.finish(f"成功押注{horse}号马{money}{config.money_unit}")


def final_check(record: dict):

    rank: Dict[int, int] = record["rank"]
    horses: List[int] = record["horses"]

    for (k, h) in enumerate(horses):
        if h == 0:
            pass

    if len(record["rank"]) + 1 > 3:
        return False
    return False


@start_race.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    record = await find_race_model(event.group_id)
    if record is None:
        await bet_horse.finish("还未有人准备开始赛马!")

    await update_game_status(event.group_id)
    while final_check(record):
        sleep(4)
        pass


@shop.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    await shop.finish('\n'.join(tools_def))
