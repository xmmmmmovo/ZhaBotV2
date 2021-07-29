from typing import Iterable

from nonebot import logger


def find_plugin_model(group_id):
    return {
        "group_id": group_id
    }


def update_plugin_model(group_id: int, plugins: Iterable[str], status: bool):
    return {
               "group_id": group_id
           }, {
               "$set": {
                   key: status for key in plugins
               }
           }
