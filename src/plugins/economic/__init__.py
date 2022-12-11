# import nonebot
from datetime import date, datetime, timedelta

from src.imports import *
from src.utils.msgutils import message_to_args, message_to_at_list, message_to_text

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("economic")
simple = auth.auth_permission()
export().name = "经济"
export().description = "查询金钱和转账"

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

mymoney = on_command("money", aliases={"我的资产", "我的财产", "余额"}, rule=not_to_me(), permission=simple,
                     priority=10)
rank = on_command("rank", aliases={"排名", "排行", "排行榜"},
                  rule=not_to_me(), permission=simple, priority=10)

pay = on_command("pay", aliases={"转账"},
                 rule=not_to_me(), permission=simple, priority=10)

borrow = on_command("borrow", rule=not_to_me(), permission=simple, priority=10)

help_money = on_command("救济金", rule=not_to_me(), permission=simple, priority=10)

addmoney = on_command("addmoney",
                      rule=not_to_me(), permission=SUPERUSER, priority=10)


@mymoney.handle()
async def handle_first_receive(event: Event, user: dict = Arg("user")):
    money = user.get("money")
    await mymoney.finish(MessageSegment.at(event.user_id) + f"您当前的资产为：{round(money, 2)}{config.money_unit}")


@pay.handle()
async def handle_first_receive(event: Event, user: dict = Arg("user"), args: Message = CommandArg()):
    ats = message_to_at_list(args)
    needs = message_to_args(args)
    idx = 0
    user["money"] = float(user["money"])
    for (at, need) in zip(ats, needs):
        fneed = float(need)
        if fneed < 0:
            await pay.finish('请支付正确的金额！')
        if user["money"] < fneed:
            await pay.finish(f"金钱不足以支付剩下的人！已支付{idx}人!")
        idx += 1
        await update_user_money_model(event.user_id, event.group_id, -fneed)
        res = await user_collection.find_one(find_user_model(at, event.group_id))
        if res is None:
            await user_collection.insert_one(new_user_model(at, event.group_id, need, False))
        else:
            await update_user_money_model(at, event.group_id, fneed)
        user["money"] -= fneed
    await pay.finish("转账成功！")

@help_money.handle()
async def handle_first_receive(event: Event, user: dict = Arg("user")):
    user["money"] = float(user["money"])
    if user["money"] < 5:
        await update_user_money_model(event.get_user_id(), event.group_id, 30)
        await help_money.finish("已为您发放30$救济金！")
    else :
        await help_money.finish("您还有很多钱, 不能领取救济金捏")

@addmoney.handle()
async def handle_first_receive(event: Event, args: Message = CommandArg()):
    ats = message_to_at_list(args)
    needs = message_to_args(args)
    idx = 0
    for (at, need) in zip(ats, needs):
        fneed = float(need)
        res = await user_collection.find_one(find_user_model(at, event.group_id))
        if res is None:
            await user_collection.insert_one(new_user_model(at, event.group_id, need, False))
        else:
            await update_user_money_model(at, event.group_id, fneed)
    await pay.finish("转账成功！")


@borrow.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    # user = state["user"]
    # ats = message_to_at_list(event.get_message())
    # needs = message_to_args(event.get_message())
    # idx = 0
    # for (at, need) in zip(ats, needs):
    #     fneed = float(need)
    #     if float(user["money"]) < fneed:
    #         await pay.finish(f"金钱不足以借贷剩下的人！已支付{idx}人!")
    #     idx += 1
    #     await user_collection.update_one(*update_user_money_model(event.user_id, event.group_id, -fneed))
    #     res = await user_collection.find_one(find_user_model(at, event.group_id))
    #     if res is None:
    #         await user_collection.insert_one(new_user_model(at, event.group_id, need, False))
    #     else:
    #         await user_collection.update_one(*update_user_money_model(at, event.group_id, fneed))

    #     def return_money_callback(bet:float, qq:int):
    #         pass

    #     scheduler.add_job(return_money_callback, "date", run_date=datetime.now() + timedelta(days=3))
    #     user["money"] -= fneed
    # await pay.finish("借贷成功！")
    return


@rank.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent):
    u_list = user_collection.find(
        {"group_id": event.group_id}).sort("money", -1)
    group_list = await get_group_member_list_cached(bot, event.group_id)

    group_dict = {}
    for u in group_list:
        group_dict[u['user_id']] = u['card'] \
            if u['card'] != '' else u['nickname']

    ans = '江江江江！本群土豪排名公布~\n'
    cnt = 0

    user_id = event.user_id
    for u in await u_list.to_list(None):
        if group_dict.get(int(u['qq'])) is None:
            continue

        cnt += 1

        if cnt > 20:
            if event.sub_type != "anonymous" and user_id == u['qq']:
                ans += f"你是第{cnt}名 现有财产{round(u['money'],2)}$"
                break
            continue

        ans += f"第{cnt}名: {group_dict[int(u['qq'])]} 现有财产:{round(u['money'],2)}$\n"

    await rank.finish(ans)
