from random import randint

from nonebot import get_driver, on_command, logger, export, on_request, on_notice, require, on_message
from nonebot.plugin import plugins
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment
from nonebot.permission import Permission, SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER, GROUP_MEMBER
from nonebot.adapters.cqhttp.event import GroupMessageEvent

from pymongo.results import InsertOneResult, UpdateResult

from src.permission import Admin, Auth
from src.rules import not_to_me
from src.db import group_collection, shot_collection, admin_collection, plugin_collection, user_collection
from src.model.admin import append_admin_model, new_admin_model, remove_admin_model, find_admin_model
from src.model.user import find_user_model, new_user_model, update_user_model, update_user_money_model
from src.model.group import update_inc_rank
from src.model.plugin import find_plugin_model, update_plugin_model
from apscheduler.schedulers.asyncio import AsyncIOScheduler
