from nonebot import require

select_all = require("mysql").select_all


async def fetchall_group():
    return await select_all("select `group_id`, `plugin_status` "
                            "from qq_group")
