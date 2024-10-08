import datetime

from src.imports import *
import cn2an

from src.core.resource import res_wrapper
from src.utils.timeutils import check_time_valid

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = Auth("bans")

__plugin_meta__ = PluginMetadata(
    name="bans",
    description="禁言",
    usage="用于特殊用途的禁言",
    type="application",
    config=Config,
    extra={},
)

simple = auth.auth_permission()
time_to_seconds = {"小时": 60*60, "天": 60*60*24, "分钟": 60, "秒": 1, "秒钟": 1}

sleep = on_startswith("来一份精致睡眠套餐", rule=allow_all(),
                      permission=simple, priority=11)
ban = on_regex(r"来一份(?P<time>.*?)(?P<type>[小时,分钟,秒,秒钟,天]+)的?禁言", rule=allow_all(),
               permission=simple, priority=12)
unban = on_command("unban", rule=private_call(),
                   permission=SUPERUSER, priority=10)

SLEEP_TOO_EARLY_VOICE = res_wrapper("voice/LiYongle.mp3")


@sleep.handle()
async def handle_first_receive(bot: Bot, event: Event):
    now = datetime.datetime.now()
    td_9pm = now.replace(hour=21, minute=0, second=0, microsecond=0)
    td_10am = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if now < td_9pm and now > td_10am:
        await sleep.finish(MessageSegment.record(SLEEP_TOO_EARLY_VOICE))

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
async def handle_first_receive(bot: Bot, event: PrivateMessageEvent, msg: Message = CommandArg()):
    await bot.set_group_ban(group_id=msg.extract_plain_text().strip(),
                            user_id=event.user_id, duration=0)
    await unban.finish("解禁成功")
