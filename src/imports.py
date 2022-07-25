from random import randint

from nonebot import get_driver, on_command, export, on_request, on_notice, require, on_message, on_regex, on_startswith, on_shell_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.permission import Permission, SUPERUSER
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER, GROUP_MEMBER
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.log import logger

from pymongo.results import InsertOneResult, UpdateResult

from src.permission import Admin, Auth
from src.rules import not_to_me, allow_all, private_call
from src.db import group_collection, admin_collection, user_collection
from src.db.model.admin import append_admin_model, new_admin_model, remove_admin_model, find_admin_model
from src.db.model.user import find_user_model, new_user_model, update_user_model, update_user_money_model
from src.db.model.group import update_inc_rank
from src.db.model.plugin import find_plugin_model, update_plugin_model
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.utils.pluginutils import *
