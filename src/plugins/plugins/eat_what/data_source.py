from nonebot import require

select_all = require("mysql").select_all
op_sql = require("mysql").op_sql
select_one = require("mysql").select_one


async def fetch_hall_list(qq_group_id):
    return select_all("select hallname from `hall` "
                      "where qq_group_id = %s", (qq_group_id))


async def fetch_hall_id(qq_group_id, hallname):
    return select_one("select id from `hall` "
                      "where qq_group_id = %s and hallname=%s", (qq_group_id, hallname))


async def insert_hall(qq_group_id, hallname):
    return op_sql("insert into hall (hallname, qq_group_id) "
                  "values (%s, %s)", (qq_group_id, hallname))
