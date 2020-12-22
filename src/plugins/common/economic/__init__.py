from nonebot import get_driver, on_command, logger, require, export
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.permission import GROUP

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("permission").NOT_ANONYMOUS_GROUP
insert_user = require("dao").insert_user
op_sql = require("mysql").op_sql
select_one = require("mysql").select_one
select_all = require("mysql").select_all

my_money = on_command("money", aliases={"我的资产", "我的财产", "余额"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP,
                      priority=97)
rank = on_command("rank", aliases={"排名", "排行"}, rule=not_to_me(), permission=GROUP, priority=97)


@my_money.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    data = await fetch_user_money_status(event.user_id, event.group_id)
    if data == None:
        succ = await insert_user(event.user_id, event.group_id, 0, int(False))
        if not succ:
            await my_money.finish("获取数据失败！请联系管理员！")
        await my_money.finish(MessageSegment.at(event.user_id) + f"您当前的资产为：{0}{config.money_unit}")
    else:
        await my_money.finish(MessageSegment.at(event.user_id) + f"您当前的资产为：{data['money']}{config.money_unit}")


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


async def increase_user_money(qq, qq_group_id, money):
    return await op_sql("update `user` set `money`=`money`+%s "
                        "where `qq`=%s and `qq_group_id`=%s",
                        (money, qq, qq_group_id))


async def fetch_user_money_status(qq, qq_group_id):
    return await select_one("select `money` from `user` "
                            "where `qq` = %s and `qq_group_id` = %s",
                            (qq, qq_group_id))


async def select_user_order_by_money(group_id):
    return await select_all("select * from user "
                            "where qq_group_id = %s "
                            "order by money desc", (group_id))


export().increase_user_money = increase_user_money
export().fetch_user_money_status = fetch_user_money_status
export().select_user_order_by_money = select_user_order_by_money
