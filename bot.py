#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from loguru import logger
import nonebot
from nonebot.adapters.onebot.v11.adapter import Adapter

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_from_toml("pyproject.toml")
nonebot.run()
