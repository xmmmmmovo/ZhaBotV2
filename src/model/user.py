import money as money


def new_user_model(qq, group_id, money, has_signed):
    return {
        "qq": qq,
        "group_id": group_id,
        "money": money,
        "has_signed": has_signed
    }


def find_user_model(qq, group_id):
    return {"qq": qq, "group_id": group_id}


def update_user_model(qq, group_id, money: float, has_signed: bool):
    return {
               "qq": qq,
               "group_id": group_id
           }, {
               "$set": {
                   "has_signed": has_signed
               },
               "$inc": {
                   "money": money,
               }
           }


def update_user_money_model(qq, group_id, money):
    return {
               "qq": qq,
               "group_id": group_id
           }, {
               "$set": {
                   "money": money,
               }
           }


def update_user_signed_model(qq, group_id, has_signed: bool):
    return {
               "qq": qq,
               "group_id": group_id
           }, {
               "$set": {
                   "has_signed": has_signed,
               }
           }
