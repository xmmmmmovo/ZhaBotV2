from typing import Dict, List
from src.db import group_collection


def new_group_model(group_id: int):
    return{
        "group_id": group_id,
        "rank": 1,
        "ban_time": 1
    }


def find_group_model(group_id: int):
    return {
        "group_id": group_id
    }


def update_inc_rank(group_id: int):
    return {
        "group_id": group_id
    }, {
        "$inc": {
            "rank": 1
        }
    }


async def update_inc_ban_time(group_id: int):
    return await group_collection.update_one({
        "group_id": group_id
    }, {
        "$inc": {
            "ban_time": 1
        }
    })


async def reset_ban_time():
    return await group_collection.update_many({}, {
        "$set": {
            "ban_time": 1
        }
    })
