#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("nonebot_plugin_status")
nonebot.load_plugin("src.plugins.mysql")
nonebot.load_plugin("src.plugins.chat")
nonebot.load_plugin("src.plugins.echo")
nonebot.load_plugin("src.plugins.hitokoto")
nonebot.load_plugin("src.plugins.horserace")
nonebot.load_plugin("src.plugins.weather")
nonebot.load_plugin("src.plugins.schedule")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.run()
