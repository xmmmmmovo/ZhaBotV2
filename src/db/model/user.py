from src.db import user_collection


def new_user_model(qq: int, group_id: int, money, has_signed):
    return {
        "qq": int(qq),
        "group_id": int(group_id),
        "money": float(money),
        "has_signed": bool(has_signed)
    }


def find_user_model(qq, group_id):
    return {"qq": int(qq),
            "group_id": int(group_id)}


def update_user_model(qq, group_id, money: float, has_signed: bool):
    return {
        "qq": qq,
        "group_id": group_id
    }, {
        "$set": {
            "has_signed": bool(has_signed)
        },
        "$inc": {
            "money": float(money)
        }
    }


async def update_user_money_model(qq, group_id, money: float):
    return await user_collection.update_one({
        "qq": int(qq),
        "group_id": int(group_id)
    }, {
        "$inc": {
            "money": round(float(money), 2)
        }
    })


def update_user_signed_model(qq, group_id, has_signed: bool):
    return {
        "qq": int(qq),
        "group_id": int(group_id)
    }, {
        "$set": {
            "has_signed": bool(has_signed)
        }
    }
