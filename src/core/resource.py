from os import getcwd

from nonebot.adapters.onebot.v11.message import MessageSegment


def res_wrapper(path: str) -> str:
    return f'file:///{getcwd()}/assets/{path}'


def img_msgseg_wrapper(path: str) -> MessageSegment:
    return MessageSegment.image(res_wrapper(path))
