# import nonebot
from src.imports import *
import cn2an

from src.utils.timeutils import check_time_valid

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = init_plugin(export(), "bans", "禁言", "用于特殊用途的禁言")
simple = auth.auth_permission()
time_to_seconds = {"小时": 60*60, "天": 60*60*24, "分钟": 60, "秒": 1, "秒钟": 1}

sleep = on_startswith("来一份精致睡眠套餐", rule=allow_all(),
                      permission=simple, priority=92)
ban = on_regex(r"来一份(?P<time>.*?)(?P<type>[小时,分钟,秒,秒钟,天]+)的?禁言", rule=allow_all(),
               permission=simple, priority=92)
unban = on_command("unban", rule=private_call(),
                   permission=SUPERUSER, priority=92)


@sleep.handle()
async def handle_first_receive(bot: Bot, event: Event):
    await bot.set_group_ban(group_id=event.group_id,
                            user_id=event.user_id, duration=60 * 60 * config.sleep_time)
    await sleep.finish("ok！好好睡觉!")


@ban.handle()
async def handle_first_receive(bot: Bot, event: Event, md: dict = Arg("_matched_dict")):
    type = md["type"]
    if md["time"] == "半":
        time = 0.5
    else:
        time = int(cn2an.cn2an(md["time"], "smart"))
    valid = check_time_valid(time, type)
    if valid:
        await bot.set_group_ban(group_id=event.group_id,
                                user_id=event.user_id, duration=time * time_to_seconds.get(type))
        await ban .finish("已经成功禁言")
    else:
        await ban.finish("输入了错误的时间长度(可能过长或者格式错误)")


@unban.handle()
async def handle_first_receive(bot: Bot, event: PrivateMessageEvent):
    await bot.set_group_ban(group_id=event.get_plaintext().strip(),
                            user_id=event.user_id, duration=0)
    await unban.finish("解禁成功")
