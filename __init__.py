import os
import random
from nonebot import on_command
from nonebot.typing import T_State
from hashlib import md5
# from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
# 前面这行是旧版真寻使用的，如果您是旧版请解除前面一行注释并注释掉下面一行
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from hashlib import md5
from .data_source import getData, buildMessage
from utils.utils import get_message_img

__zx_plugin_name__ = "动漫人物查询"
__plugin_usage__ = """
usage：
    看看这个是什么番/Gal又是什么人物？
    指令：
        动漫识别 [图片] --搜索并返回一个动漫人物
        多可能动漫识别 [图片] --返回多个人物
        游戏识别 [图片] --搜索并返回一个游戏人物
        多可能游戏识别 [图片] --返回多个人物
""".strip()
__plugin_des__ = "来看看这是什么人物吧！"
__plugin_cmd__ = ["人物查询"]
__plugin_version__ = 0.1
__plugin_author__ = "misaki"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["人物查询"],
}
__plugin_block_limit__ = {
    "rst": "请再次尝试识别命令"
}

f1 = on_command("动漫识别", priority=5, block=True)
f2 = on_command("多可能动漫识别", priority=5, block=True)
f3 = on_command("游戏识别", priority=5, block=True)
f4 = on_command("多可能游戏识别", priority=5, block=True)


@f1.got("img_url", prompt="请给出带有人物的图片")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    state["img_url"] = img_url
    result = await getData(state["img_url"][0], "anime", 0)
    message = buildMessage(result, 0, "anime")
    if len(result['data']) == 0:
        await f1.send("抱歉图片中未识别到动漫人物")
        return
    await f1.send("感谢使用AnimeTrace动漫查询引擎，您的图片预测结果是\n" + str(message) + "共预测到" + str(
        len(result['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!")
    removeTemp(state["img_url"][0])


@f2.got("img_url", prompt="请给出带有人物的图片")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    state["img_url"] = img_url
    result = await getData(state["img_url"][0], "anime", 1)
    if len(result['data']) == 0:
        await f2.send("抱歉图片中未识别到动漫人物")
        return
    message = buildMessage(result, 1, "anime")
    await bot.send_group_forward_msg(group_id=event.group_id, messages=message) if isinstance(event,
                                                                                              GroupMessageEvent) else await bot.send_private_forward_msg(
        user_id=event.user_id, messages=message)
    removeTemp(state["img_url"][0])


@f3.got("img_url", prompt="请给出带有人物的图片")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    state["img_url"] = img_url
    result = await getData(state["img_url"][0], "game", 0)
    message = buildMessage(result, 0, "game")
    if len(result['data']) == 0:
        await f1.send("抱歉图片中未识别到游戏人物")
        return
    await f1.send("感谢使用AnimeTrace动漫查询引擎，您的图片预测结果是\n" + str(message) + "共预测到" + str(
        len(result['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!")
    removeTemp(state["img_url"][0])


@f4.got("img_url", prompt="请给出带有人物的图片")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    state["img_url"] = img_url
    result = await getData(state["img_url"][0], "game", 1)
    if len(result['data']) == 0:
        await f2.send("抱歉图片中未识别到游戏人物")
        return
    message = buildMessage(result, 1, "game")
    await bot.send_group_forward_msg(group_id=event.group_id, messages=message) if isinstance(event,
                                                                                              GroupMessageEvent) else await bot.send_private_forward_msg(
        user_id=event.user_id, messages=message)
    removeTemp(state["img_url"][0])


def removeTemp(img):
    try:
        os.remove(md5(img.encode("utf-8")).hexdigest() + ".png")
    except:
        return
