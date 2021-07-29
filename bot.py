#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from loguru import logger
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
