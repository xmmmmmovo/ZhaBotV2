# import nonebot
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection, AgnosticDatabase, AgnosticClient
from nonebot import get_driver, Driver

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())
driver: Driver = get_driver()

client: AgnosticClient = AsyncIOMotorClient(config.mongo_url)
db: AgnosticDatabase = client.bot

user_collection: AgnosticCollection = db.get_collection("user")
plugin_collection: AgnosticCollection = db.get_collection("plugin")
admin_collection: AgnosticCollection = db.get_collection("admin")
shot_collection: AgnosticCollection = db.get_collection("shot")
group_collection: AgnosticCollection = db.get_collection("group")
