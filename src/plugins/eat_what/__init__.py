from nonebot import get_driver, on_command, require, logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import Permission

from .config import Config
from src.common.rules import not_to_me
from .data_source import fetch_hall_list

global_config = get_driver().config
config = Config(**global_config.dict())

NOT_ANONYMOUS_GROUP = require("src.plugins.permission").NOT_ANONYMOUS_GROUP

today_food = on_command("eat_what", aliases={"吃什么"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=6)
add_food = on_command("add_food", aliases={"加吃的"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=6)
hall = on_command("hall", aliases={"食堂"}, rule=not_to_me(), permission=NOT_ANONYMOUS_GROUP, priority=6)


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
        rows = await fetch_hall_list(event.group_id)
        await add_food.send("本群食堂列表:\n" + "\n".join(f"{k}: {v['hallname']}" for k, v in enumerate(rows)))
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


@hall.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    rows = await fetch_hall_list(event.group_id)
    await hall.finish("本群食堂列表:\n" + "\n".join(f"{k}: {v['hallname']}" for k, v in enumerate(rows)))
