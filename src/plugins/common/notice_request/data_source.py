from nonebot import require

op_sql = require("mysql").op_sql


async def insert_qq_group(group_id, status):
    return await op_sql("insert into qq_group(group_id, plugin_status) "
                        "values (%s, %s)", (group_id, status))


async def delete_qq_group(group_id):
    return await op_sql("delete from qq_group "
                        "where group_id = %s", (group_id))
