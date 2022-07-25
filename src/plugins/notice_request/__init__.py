from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

request_handler = on_request(block=True)
notice_handler = on_notice(block=True)


@request_handler.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    # if config.request_on:
    #     flag = str(event.id)
    #     if event.type == "friend":
    #         await bot.set_friend_add_request(flag=flag, approve=True)
    #     elif event.type == "group":
    #         # succ = await insert_qq_group(event.group_id, template)
    #         await bot.set_group_add_request(flag=flag, sub_type=event.sub_type, approve=True)
    pass


@notice_handler.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    pass
