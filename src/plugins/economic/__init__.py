# import nonebot
from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("economic")
export().name = "经济"
export().description = "查询金钱和转账"

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

mymoney = on_command("money", aliases={"我的资产", "我的财产", "余额"}, rule=not_to_me(), permission=auth,
                     priority=97)
rank = on_command("rank", aliases={"排名", "排行"}, rule=not_to_me(), permission=auth, priority=97)

pay = on_command("pay", rule=not_to_me(), permission=auth, priority=97)

borrow = on_command("borrow", rule=not_to_me(), permission=auth, priority=97)


@mymoney.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    res = await user_collection.find_one(find_user_model(event.sender.user_id, event.group_id))
    money = 0
    if res is None:
        await user_collection.insert_one(new_user_model(event.sender.user_id, event.group_id, 0, False))
    else:
        money = res.get("money")
    await mymoney.finish(MessageSegment.at(event.user_id) + f"您当前的资产为：{money}{config.money_unit}")


@pay.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    pass


@borrow.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    pass


@rank.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    u_list = user_collection.find({"group_id": event.group_id}).sort("money", -1)
    group_list = await bot.get_group_member_list(group_id=event.group_id)

    group_dict = {}
    for u in group_list:
        group_dict[u['user_id']] = u['card'] \
            if u['card'] != '' else u['nickname']

    ans = '江江江江！本群土豪排名公布~\n'
    cnt = 0

    user_id = event.user_id
    for u in await u_list.to_list(None):
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
