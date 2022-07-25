# import nonebot
from src.model.horserace import *
from src.imports import *
from src.utils.msgutils import is_number
from .config import Config
from .data_source import *
from re import split
from asyncio import sleep

from src.utils.mathutils import rfloat

global_config = get_driver().config
config = Config(**global_config.dict())

auth = init_plugin(export(), "horserace", "赛马", "赛马比赛")
simple = auth.auth_permission()
admin = auth.admin_auth_permission()

bet_horse = on_command(
    "押马", aliases={"压马"}, rule=not_to_me(), permission=simple, priority=93)
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


@horse_ready.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    record = await find_race_model(event.group_id)
    if record is None:
        await init_horse_race_game(event.group_id, config.horse_num, config.slide_length)
        await horse_ready.finish(start_head)
    elif not record["has_started"]:
        await horse_ready.finish("本局赛马已经开始准备咯"
                                 "请输入开始赛马进行游戏吧！")


@bet_horse.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    record = await find_race_model(event.group_id)
    user = state["user"]

    if record is None:
        await bet_horse.finish("还未有人准备开始赛马!")

    if record["has_started"]:
        await bet_horse.finish("赛马比赛已经开始，无法下注！")

    msg = event.get_plaintext().strip()
    args = split("[,，]", msg)

    if len(args) == 0:
        return
    elif len(args) == 1:
        state["horse"] = args[0]
    elif len(args) == 2:
        state["horse"] = args[0]
        state["money"] = args[1]


@bet_horse.got("horse", prompt="请输入想要押马的编号")
async def handle_key(matcher: Matcher, args: Message = CommandArg()):
    horse = 0
    try:
        horse = int(state["horse"])
    except:
        await bet_horse.finish("马编号输入格式错误！请重新输入")

    if horse < 1 or horse > config.horse_num:
        await bet_horse.finish("没有此编号马！请重新输入")


@bet_horse.got("money", prompt="请输入押注钱数")
async def handle_key(matcher: Matcher, args: Message = CommandArg()):
    money = state["money"]
    if is_number(money):
        money = rfloat(state["user"]["money"]) \
            if state["money"] in config.stud_list \
            else rfloat(state["money"])
    else:
        await bet_horse.finish("金钱输入格式错误！请重新输入")
    horse = int(state["horse"])
    if money > float(state["user"]["money"]) or money < 0:
        await bet_horse.finish("没有足够的金钱！")

    await update_bet_money(event.group_id, event.user_id, money * 0.99, horse)
    await bet_horse.finish(f"成功押注{horse}号马{money}{config.money_unit}")


async def final_check(record: dict, group_id: int):
    rank: Dict[int, int] = record["rank"]
    horses: List[int] = record["horses"]
    n_rank = len(rank) + 1

    if n_rank > 3:
        return False

    for (k, h) in enumerate(horses):
        if h == 0:
            tmp = rank.get(str(k))
            if tmp is None:
                await update_rank_status(group_id, k, n_rank)

    return True


@start_race.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    await sleep(1)
    record = await find_race_model(event.group_id)
    if record is None:
        await bet_horse.finish("还未有人准备开始赛马!")

    await update_game_status(event.group_id)

    def update(idx, pos) -> str:
        if event_num != 5:
            pos -= randint(1, 3)

        if pos < 0:
            pos = 0
        if pos > config.slide_length - 1:
            pos = config.slide_length - 1
        horses[idx] = pos
        if pos == 0:
            return config.horse_char + (config.slide * (config.slide_length - 1))
        if status == -1 or (status == 1 and idx not in suf_list):
            return config.slide * pos + config.horse_char + config.slide * (config.slide_length - 1 - pos)
        if event_num == 1:
            return config.slide * (pos - 2) + "👨‍🎤🔪" + config.horse_char + config.slide * (
                config.slide_length - 1 - pos)
        if event_num == 2:
            return config.slide * (pos - 2) + "🐴🌹" + config.horse_char + config.slide * (
                config.slide_length - 1 - pos)
        if event_num == 3:
            return config.slide * (pos - 2) + "🧊" + config.slide + config.horse_char + config.slide * (
                config.slide_length - 1 - pos)
        if event_num == 4:
            return config.slide * pos + config.horse_char + "💨" + config.slide * (
                config.slide_length - 2 - pos)
        return config.slide * pos + config.horse_char + config.slide * (config.slide_length - 1 - pos)

    while await final_check(record, event.group_id):
        horses: List[int] = record["horses"]

        event_num = randint(0, len(events))
        status = -1
        if event_num != 0:

            status, suf_list = await events[event_num](start_race, horses)
        await start_race.send("\n".join(f"{i + 1} {update(i, pos)}" for (i, pos) in enumerate(horses)))
        record = await update_in_game_vars(event.group_id, horses)
        await sleep(4)
    record = await find_race_model(event.group_id)
    rank = record["rank"]
    user_list = record["user_list"]
    res = "本场赛马已结束!\n"
    res += "\n".join(f"第{v}名：{int(k) + 1}号马！" for k, v in rank.items())
    res += '\n现在开始结算...'
    await start_race.send(res)

    # 开始结算
    every_house_cnt = [0] * config.horse_num
    player_num = len(user_list)
    for p in user_list.values():
        every_house_cnt[p[0]] += 1
    for qq, bet in user_list.items():
        if str(bet[0]) in rank.keys():
            persons = every_house_cnt[bet[0]]
            # 根据获胜的人数和游玩的人数来进行判断倍率
            if persons <= (player_num - persons + 1):
                user_list[qq].append(
                    rfloat(config.odd[rank[str(bet[0])]]) * bet[1]
                )
            else:
                user_list[qq].append(
                    rfloat(
                        (1 + ((config.odd[rank[str(bet[0])]] - 1)
                              * (persons / player_num))
                         )
                    ) * bet[1]
                )
        else:
            # 奖励变成负数
            user_list[qq].append(-bet[1])
    for (qq, v) in user_list.items():
        await update_user_money_model(qq, event.group_id, v[2])
    await remove_horserace_model(event.group_id)
    await start_race.finish("已结算!")


@shop.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    await shop.finish('\n'.join(tools_def))
