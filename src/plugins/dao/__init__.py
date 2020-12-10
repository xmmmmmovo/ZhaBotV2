from nonebot import get_driver, export

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

from nonebot import require

select_one = require("src.plugins.mysql").select_one
op_sql = require("src.plugins.mysql").op_sql


async def fetch_user_sign_status(qq, qq_group_id):
    return await select_one("select `has_signed` from `user` "
                            "where `qq` = %s and `qq_group_id` = %s",
                            (qq, qq_group_id,))


async def insert_user(qq, qq_group_id, money, has_signed):
    return await op_sql("insert into `user` (`qq`, `qq_group_id`, `money`, `has_signed`) "
                        "values (%s, %s, %s, %s)",
                        (str(qq), str(qq_group_id), money, has_signed))


async def update_user(qq, qq_group_id, money, has_signed):
    return await op_sql("update `user` set `money`=`money`+%s, `has_signed`=%s "
                        "where `qq`=%s and `qq_group_id`=%s",
                        (money, has_signed, qq, qq_group_id))


async def reset_user_signed(has_signed):
    return await op_sql("update `user` set `has_signed`=%s", (has_signed))


export().fetch_user_sign_status = fetch_user_sign_status
export().insert_user = insert_user
export().update_user = update_user
export().reset_user_signed = reset_user_signed
