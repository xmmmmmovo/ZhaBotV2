import asyncio
from dataclasses import dataclass
from time import sleep
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection, AgnosticDatabase,AgnosticClient


client: AgnosticClient = AsyncIOMotorClient(
    "mongodb://192.168.0.107:27017")
db: AgnosticDatabase = client.bot
mongo_collection: AgnosticCollection = db.get_collection("mongo")


@dataclass
class User():
    name: str


async def main():
    user = await mongo_collection.insert_one(User("aaa").__dict__)
    print(type(user))
    print(await mongo_collection.find_one({"_id": user.inserted_id}))

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

loop.close()
