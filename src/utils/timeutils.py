from sqlalchemy import false


def check_time_valid(time: int, type: str) -> bool:
    if type == "秒" or type == "秒钟":
        return time < (60*60*24*30 - 1)
    if type == "分钟":
        return time < (60*24*30 - 1)
    if type == "小时":
        return time < (24*30 - 1)
    if type == "天":
        return time < (30 - 1)
    return False
