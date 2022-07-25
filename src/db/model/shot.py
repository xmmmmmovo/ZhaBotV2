from typing import Dict, List
from src.db import shot_collection


async def find_or_insert_shot_model(group_id: int) -> Dict:
    record = await shot_collection.find_one({"group_id": int(group_id)})
    if record is None:
        record = {
            "group_id": int(group_id),
            "has_started": False
        }
        await shot_collection.insert_one(record)
    return record


async def find_shot_model(group_id: int) -> Dict:
    return await shot_collection.find_one({
        "group_id": group_id
    })


async def init_shot_game(group_id: int, k: int):
    record = await shot_collection.update_one({
        "group_id": group_id
    }, {
        "$set": {
            "k": int(k),
            "idx": int(0),
            "has_started": True,
            "qqs": []
        }
    })

async def update_shot_idx(group_id: int, qq: Dict):
    return await shot_collection.update_one({
        "group_id": group_id
    }, {
        "$inc": {
            "idx": int(1)
        },
        "$push": {
            "qqs": qq
        }
    })


async def remove_shot_reocrd(group_id: int):
    return await shot_collection.delete_one({"group_id": group_id})
