from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = init_plugin(export(), "qa", "Question and Answer", "用于问答")

simple = auth.auth_permission()

create_question = on_command(
    "创建问题", rule=not_to_me, permission=simple, priority=89)
update_question = on_command(
    "", rule=not_to_me, permission=simple, priority=89)
list_question = on_command("", rule=not_to_me, permission=simple, priority=89)
delete_question = on_command(
    "", rule=not_to_me, permission=simple, priority=89)
index_quesiton = on_startswith(
    "", rule=not_to_me, permission=simple, priority=89)


@create_question.handle()
async def handle_first_receive(bot: Bot, event: Event):
    pass
