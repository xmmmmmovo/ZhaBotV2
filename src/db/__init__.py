# import nonebot
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection, AgnosticDatabase, AgnosticClient
from nonebot import get_driver
from nonebot.log import logger

from .config import Config

driver = get_driver()
global_config = driver.config
config = Config(**global_config.dict())

db: AgnosticDatabase = AsyncIOMotorClient(
        config.mongo_url, serverSelectionTimeoutMS=3)['bot']

user_collection: AgnosticCollection = db.get_collection("user")
plugin_collection: AgnosticCollection = db.get_collection("plugin")
admin_collection: AgnosticCollection = db.get_collection("admin")
shot_collection: AgnosticCollection = db.get_collection("shot")
group_collection: AgnosticCollection = db.get_collection("group")
horserace_collection: AgnosticCollection = db.get_collection("horserace")

# user_collection: AgnosticCollection = None
# plugin_collection: AgnosticCollection = None
# admin_collection: AgnosticCollection = None
# shot_collection: AgnosticCollection = None
# group_collection: AgnosticCollection = None
# horserace_collection: AgnosticCollection = None
