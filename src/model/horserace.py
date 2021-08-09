from src.db import horserace_collection
from typing import Dict, List


async def find_or_insert_horse_race_model(group_id: int) -> Dict:
    record = await horserace_collection.find_one({"group_id": int(group_id)})
    if record is None:
        record = {
            "group_id": int(group_id),
            "has_started": False
        }
        await horserace_collection.insert_one(record)
    return record


async def init_horse_race_game(group_id: int):
    await horserace_collection.update_one({
        "group_id": group_id
    }, {
        "$set": {
        }
    })
