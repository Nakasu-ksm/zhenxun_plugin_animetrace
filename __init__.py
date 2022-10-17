import random
from configs.path_config import IMAGE_PATH, TEMP_PATH
from nonebot import on_command
from nonebot.typing import T_State
#from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
#前面这行是旧版真寻使用的，如果您是旧版请解除前面一行注释并注释掉下面一行
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from services.log import logger
from utils.http_utils import AsyncHttpx
import json
from utils.utils import get_message_img

__zx_plugin_name__ = "动漫人物查询"
__plugin_usage__ = """
usage：
    看看这个是什么番又是什么人物？
    指令：
        人物查询 [图片] --搜索只返回一个人物
        多可能人物查询 [图片] --返回多个人物
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

single = on_command("动漫识别", aliases={"人物识别"}, priority=5, block=True)

probl = on_command("多可能动漫查询", aliases={"多可能人物查询"}, priority=5, block=True)
@single.got("img_url", prompt="请给出带有人物的图片")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    state["img_url"] = img_url
    await AsyncHttpx.download_file(state["img_url"][0], "1.png")
    files = {
        'image': open("1.png", 'rb')
    }
    content = await AsyncHttpx.post("https://aiapiv2.animedb.cn/detect", data=None, files=files)
    content = json.loads(content.text)
    if (len(content['data']) == 0):
        await single.send("抱歉图片中未识别到动漫人物")
        return
    char = ""
    for i in content['data']:
        message = "人物:" + i['name'] + "--来自动漫《" + i['cartoonname'] + "》" + "\n"
        char += message

    await single.send("感谢使用AnimeTrace动漫查询引擎，您的图片预测结果是\n" + str(char) + "共预测到" + str(len(content['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!")


def link(string, name="越谷 小鞠"):
    return {
        "type": "node",
        "data": {
            "name": f"{name}",
            "uin": f"1398087940", #这里可以自定义
            "content": string,
        },
    }
@probl.got("img_url", prompt="请给出带有人物的图片")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    state["img_url"] = img_url
    await AsyncHttpx.download_file(state["img_url"][0], "1.png")

    files = {
        'image': open("1.png", 'rb')
    }
    content = await AsyncHttpx.post("https://aiapiv2.animedb.cn/detect?force_one=1", data=None, files=files)
    # logger.info(content.text)
    content = json.loads(content.text)
    if (len(content['data']) == 0):
        await probl.send("抱歉图片中未识别到动漫人物")
        return
    char = ""
    count = 0
    message_list = []

    message_list.append(link("感谢使用AnimeTrace动漫查询引擎，这是您的动漫图片预测结果"))
    for i in content['data']:
        count += 1
        message = f"第{count}个人物:" + i['char'][0]['name'] + "--来自动漫《" + i['char'][0]['cartoonname'] + "》" + "\n"
        if (len(i['char']) != 1):
            for idx, d in enumerate(i['char']):
                if (idx == 0):
                    continue
                message += "--其他可能性"
                message += "-" + d['name'] + "--来自动漫《" + d['cartoonname'] + "》" + "\n"
        char += message
        message_list.append(link(char, i['char'][0]['name']))
        char = ""
    message_list.append(link("共预测到" + str(len(content['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!"))
    await bot.send_group_forward_msg(group_id=event.group_id, messages=message_list)
