from src.db import horserace_collection
from typing import Any, Dict, List
from pymongo import ReturnDocument
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
            f"user_list.{qq}": [
                horse - 1,
                round(money, 2)
            ]
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


async def update_in_game_vars(group_id: int, horses: List[int]):
    return await horserace_collection.find_one_and_update({
        "group_id": group_id
    }, {
        "$set": {
            "horses": horses
        }
    }, return_document=ReturnDocument.AFTER)


async def update_rank_status(group_id: int, horse: int, rank: int):
    return await horserace_collection.update_one({
        "group_id": group_id
    }, {
        "$set": {
            f"rank.{horse}": rank
        }
    })


async def remove_horserace_model(group_id: int):
    await horserace_collection.delete_one({"group_id": group_id})
