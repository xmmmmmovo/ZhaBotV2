from src.db import horserace_collection
from typing import Dict, List


async def find_race_model(group_id: int):
    return await horserace_collection.find_one({"group_id": int(group_id)})


async def init_horse_race_game(group_id: int, horse_num: int, slide_length: int):
    return await horserace_collection.update_one({
        "group_id": group_id
    }, {
        "$set": {
            "has_started": False,
            "rank": {},
            "user_list": {},
            "horses": [slide_length] * horse_num
        }
    }, upsert=True)


async def update_bet_money(group_id: int, qq: int, money: float, horse: int):
    return await horserace_collection.update_one({
        "group_id": group_id
    }, {
        "$set": {
            f"user.{qq}": {
                "money": round(money, 2),
                "horse": horse
            }
        }
    })


async def update_game_status(group_id: int):
    return await horserace_collection.update_one({
        "group_id": group_id
    }, {
        "$set": {
            "has_started": True
        }
    })


async def update_in_game_vars(group_id: int):
    return await horserace_collection.update_one({
        "group_id": group_id
    })
