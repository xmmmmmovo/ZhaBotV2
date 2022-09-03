from src.imports import *

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = init_plugin(export(), "qa", "问答", "用于问答")

simple = auth.auth_permission()
admin = auth.admin_auth_permission()

create_question = on_command(
    "创建问题", rule=not_to_me(), permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | admin, priority=10)
update_question = on_command(
    "更新问题", rule=not_to_me(), permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | admin, priority=10)
list_question = on_command("列出问题", rule=not_to_me(),
                           permission=simple, priority=10)
delete_question = on_command(
    "删除问题", rule=not_to_me(), permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | admin, priority=10)
index_quesiton = on_startswith(
    "#", rule=not_to_me(), permission=simple, priority=10)


@create_question.handle()
async def handle_first_receive(bot: Bot, event: Event):
    pass
