from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import get_driver, require, on_command
from dataclasses import dataclass

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER

from .config import Config
from .data_source import reset_help_count
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

reset_help_count_handler = on_command("resethc", rule=not_to_me(), permission=SUPERUSER)


@scheduler.scheduled_job("cron", day="*", hour="0", minute="0", id="reset_signed_task", kwargs={})
async def run_every_day_reset_signed(**kwargs):
    await reset_help_count(config.help_count)


@reset_help_count_handler.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    ret = await reset_help_count(config.help_count)
    await reset_help_count_handler.finish("已成功重置" if ret else "重置失败")
