# import nonebot
from src.model.horserace import find_or_insert_horse_race_model
from src.imports import *
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

auth = init_plugin(export(), "horserace", "赛马", "赛马比赛")


bet_horse = on_command("押马", rule=not_to_me(), permission=auth, priority=93)
chocolate = on_command("巧克力", rule=not_to_me(), permission=auth, priority=93)
hyper = on_command("兴奋剂", rule=not_to_me(), permission=auth, priority=93)
banana = on_command("香蕉皮", rule=not_to_me(), permission=auth, priority=93)
pary = on_command("祈祷", rule=not_to_me(), permission=auth, priority=93)
start_race = on_command("startrace", aliases={
                        "开始赛马"}, rule=not_to_me(), permission=auth, priority=93)
begging = on_command("begging", aliases={
                     "救济金"}, rule=not_to_me(), permission=auth, priority=93)
shop = on_command("shop", aliases={"商品列表", "商品目录"},
                  rule=not_to_me(), permission=auth, priority=93)
horse_ready = on_command("horseready", aliases={"赛马", "准备赛马"}, rule=not_to_me(), permission=auth,
                         priority=93)


@horse_ready.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: dict):
    record = await find_or_insert_horse_race_model(event.group_id)
    if record["has_started"] == False:
        pass
    else:
        await horse_ready.finish("本局赛马已经开始准备咯"
                                 "请输入开始赛马进行游戏吧！")
