from nonebot import get_driver, export

from .config import Config

driver = get_driver()
global_config = driver.config
config = Config(**global_config.dict())



async def _start_sqlite_pools():

    pass


driver.on_startup(_start_sqlite_pools)
