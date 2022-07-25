# import nonebot
from src.imports import *
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

admin = Admin()

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
plugin_status = on_command("plugins", aliases={'菜单', '帮助'}, rule=not_to_me(),
                           permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | GROUP_MEMBER, priority=1)


@add_admin.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    msg = event.get_message()
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
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    msg = event.get_message()
    add_people = []
    dict = await admin_collection.find_one(find_admin_model(event.group_id))
    if dict is None:
        await remove_admin.finish("删除成功！")
    
    admin_list = dict["qqlist"]
    for seg in msg:  # type: MessageSegment
        seg: MessageSegment
        if seg.type == "at" and seg.data["qq"] != "all" and seg.data["qq"] not in admin_list and \
                (await bot.get_group_member_info(group_id=event.group_id, user_id=seg.data["qq"]))["role"] not in {
            "owner", "admin"}:
            # if seg.type == "at":
            add_people.append(seg.data["qq"])
    if len(add_people) == 0:
        await remove_admin.finish("没有人被删除!")
    res = await admin_collection.update_one(*remove_admin_model(add_people, event.group_id))
    await remove_admin.finish("删除成功！")


@withdraw.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    pass


@enable.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    args = event.get_plaintext().strip()
    if args:
        state["name"] = args.split(" ")


@enable.got("name", prompt="插件名")
async def handle_plugin(matcher: Matcher, args: Message = CommandArg()):
    names = state["name"]
    plugins_names = plugins.keys()
    if len(names) == 1 and names[0] == "all":
        names = plugins_names
    else:
        names = filter(lambda name: name in plugins_names, names)
    res = await update_plugin_model(event.group_id, names, True)
    await enable.finish("开启成功！")


@disable.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    args = event.get_plaintext().strip()
    if args:
        state["name"] = args.split(" ")


@disable.got("name", prompt="插件名")
async def handle_plugin(matcher: Matcher, args: Message = CommandArg()):
    names = state["name"]
    plugins_names = plugins.keys()
    if len(names) == 1 and names[0] == "all":
        names = plugins_names
    else:
        names = filter(lambda name: name in plugins_names, names)
    res = await update_plugin_model(event.group_id, names, False)
    await disable.finish("关闭成功！")


@admin_list.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
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
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    res = await find_plugin_model(event.group_id)
    mbuilder = Message("插件开启情况如下：\n")
    index = 0
    for (name, plugin) in plugins.items():
        if plugin.export.get("name") == None:
            continue
        index += 1
        mbuilder.append(
            f"{index}.{plugin.export.get('name'):5}({name:5}):{plugin.export.get('description'):10}"
            f"{'️🔵' if (res is not None and bool(res.get(name))) else '⚫':^1}\n")
    mbuilder.append("注：.enable .disable开关插件")
    await plugin_status.finish(mbuilder)
