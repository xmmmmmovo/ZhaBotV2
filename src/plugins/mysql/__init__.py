import asyncio

from nonebot import get_driver, export
import aiomysql

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

loop = asyncio.get_event_loop()

pool = aiomysql.create_pool(loop=loop, host=config.mysql_url,
                            port=int(config.mysql_port),
                            user=config.mysql_user,
                            password=config.mysql_password,
                            db=config.mysql_db)
export().pool = pool
