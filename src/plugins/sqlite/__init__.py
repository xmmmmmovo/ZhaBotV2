from databases import Database
from nonebot import get_driver, export

from .config import Config

driver = get_driver()
global_config = driver.config
config = Config(**global_config.dict())

dsn = f'sqlite:///./store/{config.bot_sql}'

database = Database(dsn)
export().database = database
