from datetime import datetime

# import nonebot
from src.core.resource import file_path_wrapper, res_wrapper
from src.imports import *
from .config import Config

from nonebot.plugin import _plugins
from nonebot import get_bot
from ujson import dump

global_config = get_driver().config
config = Config(**global_config.dict())

admin = Admin()
scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

add_admin = on_command("addadmin", rule=not_to_me(),
                       permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN, priority=1)
remove_admin = on_command("removeadmin", rule=not_to_me(),
                          permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN, priority=1)
enable = on_command("enable", rule=not_to_me(),
                    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | admin, priority=1)
disable = on_command("disable", rule=not_to_me(),
                     permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | admin, priority=1)
withdraw = on_command("withdraw", rule=not_to_me(),
                      permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | GROUP_MEMBER | admin, priority=1)
admin_list = on_command("adminlist", rule=not_to_me(),
                        permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | GROUP_MEMBER, priority=1)
plugin_status = on_command("plugins", aliases={'插件状态'}, rule=not_to_me(),
                           permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | GROUP_MEMBER, priority=1)
help = on_command("help", aliases={'菜单', '帮助'}, rule=not_to_me(),
                  permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | GROUP_MEMBER, priority=1)
backup = on_command("backup", rule=not_to_me(),
                    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | admin, priority=1)


@add_admin.handle()
async def handle_first_receive(bot: Bot, event: Event, msg=CommandArg()):
    add_people = []
    dict = await admin_collection.find_one(find_admin_model(event.group_id))
    for seg in msg:  # type: MessageSegment
        seg: MessageSegment
        if seg.type == "at" and seg.data["qq"] != "all" and \
            (await bot.get_group_member_info(group_id=event.group_id, user_id=seg.data["qq"]))["role"] not in {
                "owner", "admin"}:
            # if seg.type == "at":
            add_people.append(seg.data["qq"])
    if len(add_people) == 0:
        await add_admin.finish("没有人被添加!")

    if dict is None:
        res = await admin_collection.insert_one(new_admin_model(add_people, event.group_id))
    else:
        admin_list = dict["qqlist"]
        res = await admin_collection.update_one(*append_admin_model(add_people, event.group_id))
    await add_admin.finish("添加成功！")


@remove_admin.handle()
async def handle_first_receive(bot: Bot, event: Event, msg=CommandArg()):
    remove_people = []
    admin_dict = await admin_collection.find_one(find_admin_model(event.group_id))
    if admin_dict is None:
        await remove_admin.finish("删除成功！")
    admin_list = admin_dict["qqlist"]
    for seg in msg:  # type: MessageSegment
        seg: MessageSegment
        if seg.type == "at" and seg.data["qq"] != "all" and seg.data["qq"] in admin_list and \
            (await bot.get_group_member_info(group_id=event.group_id, user_id=seg.data["qq"]))["role"] not in {
                "owner", "admin"}:
            remove_people.append(seg.data["qq"])
    if len(remove_people) == 0:
        await remove_admin.finish("没有人被删除!")
    res = await admin_collection.update_one(*remove_admin_model(remove_people, event.group_id))
    await remove_admin.finish("删除成功！")


@withdraw.handle()
async def handle_first_receive(event: Event, msg: Message = CommandArg()):
    # TODO:不知道是不是bug
    logger.debug(str(msg))
    logger.debug(str(event.get_message()))
    for m in msg:
        logger.debug(str(m))

    for m in event.get_message():
        logger.debug(str(m))
    pass


@enable.handle()
async def handle_first_receive(matcher: Matcher, event: Event, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()
    if args:
        matcher.set_arg("name", args.split(" "))


@enable.got("name", prompt="插件名")
async def handle_plugin(event: Event, names: list = Arg("name")):
    plugins_names = _plugins.keys()
    if len(names) == 1 and names[0] == "all":
        names = plugins_names
    else:
        names = filter(lambda name: name in plugins_names, names)
    res = await update_plugin_model(event.group_id, names, True)
    await enable.finish("开启成功！")


@disable.handle()
async def handle_first_receive(matcher: Matcher, event: Event, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()
    if args:
        matcher.set_arg("name", args.split(" "))


@disable.got("name", prompt="插件名")
async def handle_plugin(event: Event, names: list = Arg("name")):
    plugins_names = _plugins.keys()
    if len(names) == 1 and names[0] == "all":
        names = plugins_names
    else:
        names = filter(lambda name: name in plugins_names, names)
    res = await update_plugin_model(event.group_id, names, False)
    await disable.finish("关闭成功！")


@admin_list.handle()
async def handle_first_receive(bot: Bot, event: Event):
    res = await admin_collection.find_one(find_admin_model(event.group_id))
    mbuilder = Message("管理列表如下：\n")
    members = await bot.get_group_member_list(group_id=event.group_id)
    filter_members = filter(
        lambda member: (member["role"] in {"admin", "owner"}) or (
            False if res is None else str(member["user_id"]) in res[
                "qqlist"]),
        members)
    for (index, member) in enumerate(filter_members):
        mbuilder.append(f"{index + 1}: {member['nickname']}\n")
    mbuilder.append("注：.addadmin .removeadmin添加删除管理员")
    await admin_list.finish(mbuilder)


@plugin_status.handle()
async def handle_first_receive(bot: Bot, event: Event):
    res = await find_plugin_model(event.group_id)
    mbuilder = Message("插件开启情况如下：\n")
    index = 0
    for (name, plugin) in _plugins.items():
        if plugin.export.get("name") == None:
            continue
        index += 1
        mbuilder.append(
            f"{index}.{plugin.export.get('name'):^5}({name:^5}):{plugin.export.get('description'):^10}"
            f"{'️🔵' if (res is not None and bool(res.get(name))) else '⚫':^1}\n")
    mbuilder.append("注：.enable .disable开关插件 需要管理权限")
    await plugin_status.finish(mbuilder)


@help.handle()
async def handle_first_receive():
    await help.finish(MessageSegment.share("https://bot.fivezha.cn/guide/", "小扎机器人使用说明",
                                           "如果查看插件状态请使用\"。plugins\"或者\"。插件状态\"",
                                           res_wrapper("misc/avatar.jpg")))


async def backup_to_json(bot: Bot, group_id, group_name):
    users = await get_group_member_list_cached(bot, group_id)
    with open(file_path_wrapper(f"data/{group_id}.json"), 'w', encoding="utf-8") as f:
        dump({
            "group_name": group_name,
            "group_members": list(map(lambda u: {
                "QQ": u["user_id"],
                "昵称": u["nickname"],
                "群名片": u["card"],
                "加群时间": datetime.utcfromtimestamp(u["join_time"]).strftime("%Y-%m-%d %H:%M:%S"),
                "最后发言时间": datetime.utcfromtimestamp(u["last_sent_time"]).strftime("%Y-%m-%d %H:%M:%S"),
                "等级": u["level"],
                "是否管理": u["role"],
                "是否不良记录": u["unfriendly"],
                "专属头衔": u["title"]
            }, users))
        }, f, ensure_ascii=False)


@backup.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent):
    await backup_to_json(bot, event.group_id, (await bot.get_group_info(group_id=event.group_id, no_cache=False))["group_name"])
    await backup.finish("备份成功！")


@scheduler.scheduled_job("cron", day="*", hour="0", minute="0", id="backup_group_members_task", kwargs={})
async def backup_cron():
    logger.info("start backup group members!")
    bot: Bot = get_bot()
    g_list = await bot.get_group_list()
    for group in g_list:
        await backup_to_json(bot, group["group_id"], group["group_name"])
