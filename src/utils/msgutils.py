from typing import Iterable, List
from nonebot.adapters.onebot.v11 import Message


def message_to_text(msg: Message) -> str:
    return "".join(map(lambda msg: str(msg).strip(), filter(
        lambda msg: msg.is_text(), msg)))


def message_to_args(msg: Message) -> Iterable[str]:
    return map(lambda msg: str(msg).strip(), filter(
        lambda msg: msg.is_text(), msg))


def message_to_at_list(msg: Message) -> Iterable[int]:
    return map(lambda msg: msg.data["qq"], filter(
        lambda msg: msg.type == "at" and msg.data["qq"] != "all", msg))


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
