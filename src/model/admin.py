from typing import List


def find_admin_model(group_id: int):
    return {
        "group_id": group_id
    }


def new_admin_model(qqlist: List[int], group_id: int):
    return {
        "qqlist": qqlist,
        "group_id": group_id
    }


def append_admin_model(qqlist: List[int], group_id: int):
    return {
               "group_id": group_id
           }, {
               "$addToSet": {
                   "qqlist": {
                       "$each": qqlist
                   }
               }
           }


def remove_admin_model(qqlist: List[int], group_id: int):
    return {
               "group_id": group_id
           }, {
               "$pullAll": {
                   "qqlist": qqlist
               }
           }
