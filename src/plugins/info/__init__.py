# import nonebot
from nonebot import rule
from src.imports import *
from .config import Config
from src.rules import poke, group_poke
import psutil
from nonebot.matcher import Matcher

global_config = get_driver().config
config = Config(**global_config.dict())

info = on_command("info", rule=private_call(),
                  permission=SUPERUSER, priority=91)
poke = on_message(poke(), permission=SUPERUSER, priority=91)


async def server_data_handler(bot: Bot, matcher: Matcher):
    per_cpu_status = psutil.cpu_percent(interval=1, percpu=True)
    memory_status = psutil.virtual_memory().percent
    disk_usages = {
        d.mountpoint: psutil.disk_usage(d.mountpoint) for d in psutil.disk_partitions()
    }
    data = []

    data.append("CPU:")
    for index, per_cpu in enumerate(per_cpu_status):
        data.append(f"  core{index + 1}: {int(per_cpu):02d}%")

    data.append(f"Memory: {int(memory_status):02d}%")
    data.append("Disk:")
    for k, v in disk_usages.items():
        data.append(f"  {k}: {int(v.percent):02d}%")

    await matcher.finish(message="\n".join(data))

info.handle()(server_data_handler)
poke.handle()(server_data_handler)

test = on_command('test', rule=not_to_me(), permission=SUPERUSER, priority=91)

@test.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    import os
    await test.finish(MessageSegment.image(f'file:///{os.getcwd()}/data/weather-icon/100.png'))
    
