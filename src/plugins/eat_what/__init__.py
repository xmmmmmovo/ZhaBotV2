from nonebot import get_driver, on_command, require, logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import Permission

from .config import Config
from src.common.rules import not_to_me

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS = require("src.plugins.permission").NOT_ANONYMOUS

today_food = on_command("eat_what", aliases={"吃什么"}, rule=not_to_me(), permission=NOT_ANONYMOUS, priority=6)
add_food = on_command("add_food", aliases={"加吃的"}, rule=not_to_me(), permission=NOT_ANONYMOUS, priority=6)


@today_food.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        pass


@add_food.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip().split(" ")
    logger.debug(args)
    if args[0] == "":
        return
    elif len(args) == 1:
        state["hall"] = args[0]
    elif len(args) == 2:
        state["hall"] = args[0]
        state["food"] = args[1]


@add_food.got("hall", prompt="请输入食堂名称")
async def handle_hall(bot: Bot, event: Event, state: dict):
    if not state["hall"]:
        await add_food.reject()


@add_food.got("food", prompt="请输入食物名称")
async def handle_food(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        state["food"] = args
    else:
        await add_food.reject()
