import asyncio
from typing import Optional

from nonebot import get_driver, export, logger
import aiomysql

from .config import Config

driver = get_driver()
global_config = driver.config
config = Config(**global_config.dict())

pool: Optional[aiomysql.Pool] = None
mysql_opened = False


@driver.on_startup
async def connect_to_mysql():
    global pool, mysql_opened
    if config.mysql_host is not None:
        pool = await aiomysql.create_pool(host=config.mysql_host,
                                          port=int(config.mysql_port),
                                          user=config.mysql_user,
                                          password=config.mysql_password,
                                          db=config.mysql_db, charset="utf8")
        mysql_opened = True
        logger.info("connect to mysql")


@driver.on_shutdown
async def free_db():
    global pool, mysql_opened
    if mysql_opened:
        pool.close()
        await pool.wait_closed()
        mysql_opened = False
        logger.info("disconnect to mysql")


# _PoolContextManager

async def op_sql(self, query, params=None):
    '''
    单条数据的操作，insert，update，delete
    :param query:包含%s的sql字符串，当params=None的时候，不包含%s
    :param params:一个元祖，默认为None
    :return:如果执行过程没有crash，返回True，反之返回False
    '''
    async with pool.require() as conn:
        async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
            try:
                await cur.execute(query, params)
                await conn.commit()
                ret = True
            except BaseException as e:
                await conn.rollback()  # 如果这里是执行的执行存储过程的sql命令，那么可能会存在rollback的情况，所以这里应该考虑到
                logger.info("[sql_query] - %s" % query)
                logger.info("[sql_params] - %s" % (params,))
                logger.exception(e)
                ret = False
    return ret


async def select_one(self, query, params=None):
    '''
    查询数据表的单条数据
    :param query: 包含%s的sql字符串，当params=None的时候，不包含%s
    :param params: 一个元祖，默认为None
    :return: 如果执行未crash，并以包含dict的列表的方式返回select的结果，否则返回错误代码001
    '''
    async with pool.require() as conn:
        async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
            try:
                await self.cur.execute(query, params)
                ret = await self.cur.fetchone()
            except BaseException as e:
                logger.info("[sql_query] - %s" % query)
                logger.info("[sql_params] - %s" % (params,))
                logger.exception(e)
                ret = None
    return ret


async def select_all(self, query, params=None):
    '''
    查询数据表的单条数据
    :param query:包含%s的sql字符串，当params=None的时候，不包含%s
    :param params:一个元祖，默认为None
    :return:如果执行未crash，并以包含dict的列表的方式返回select的结果，否则返回错误代码001
    '''
    async with pool.require() as conn:
        async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
            try:
                await self.cur.execute(query, params)
                # await self.cur.scroll(0, "absolute")  # 光标回到初始位置，感觉这里得这句有点多余
                ret = await self.cur.fetchall()
            except BaseException as e:
                logger.info("[sql_query] - %s" % query)
                logger.info("[sql_params] - %s" % params)
                logger.exception(e)
                ret = None
    return ret


async def insert_many(self, query, params):
    '''
    向数据表中插入多条数据
    :param query:包含%s的sql字符串，当params=None的时候，不包含%s
    :param params:一个内容为元祖的列表
    :return:如果执行过程没有crash，返回True，反之返回False
    '''
    async with pool.require() as conn:
        async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
            try:
                await self.cur.executemany(query, params)
                await self.conn.commit()
                ret = True
            except BaseException as e:
                await self.conn.rollback()
                logger.info("[sql_query] - %s" % query)
                logger.info("[sql_params] - %s" % params)
                logger.exception(e)
                ret = False
    return ret


export().pool = pool
export().op_sql = op_sql
export().select_one = select_one
export().select_all = select_all
export().insert_many = insert_many
