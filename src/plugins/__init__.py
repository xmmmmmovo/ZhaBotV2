from nonebot import get_driver, on_command, logger, export
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment
from nonebot.permission import Permission, SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER, GROUP_MEMBER

from pymongo.results import InsertOneResult, UpdateResult

from src.permission import Admin
from src.rules import not_to_me
from src.db import admin_collection, plugin_collection
from src.model.admin import append_admin_model, new_admin_model, remove_admin_model, find_admin_model
from src.model.plugin import find_plugin_model, Plugin, update_plugin_model