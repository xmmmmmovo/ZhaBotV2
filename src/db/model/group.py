from typing import Dict, List


def new_group_model(group_id: int):
    return{
        "group_id": group_id,
        "rank": 1,
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